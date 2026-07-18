# Stellar Burgers — автотесты (Selenium + pytest + Allure)

Автотесты для https://stellarburgers.education-services.ru

## Стек
- Python 3.10+
- Selenium WebDriver
- pytest
- allure-pytest
- Page Object

## Структура проекта

```
stellar_burgers_tests/
├── pages/
│   ├── base_page.py        # общие методы для всех страниц
│   ├── main_page.py        # страница "Конструктор" (главная)
│   └── feed_page.py        # страница "Лента заказов"
├── utils/
│   ├── api_client.py       # регистрация/логин пользователя через API (без UI)
│   └── js_dnd.py           # JS-эмуляция drag&drop (react-dnd HTML5 backend)
├── tests/
│   ├── conftest.py         # фикстуры: драйвер, браузер, allure environment
│   ├── test_constructor.py # тесты раздела "Конструктор"
│   └── test_feed.py        # тесты раздела "Лента заказов"
├── requirements.txt
├── pytest.ini
└── README.md
```

## Установка

```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Нужны установленные Google Chrome и Mozilla Firefox, а также драйверы
(проект использует Selenium Manager, идущий в комплекте с Selenium 4.6+,
так что chromedriver/geckodriver подтягиваются автоматически — ничего
скачивать вручную не нужно).

## Запуск тестов

Запуск на Chrome (по умолчанию):
```bash
pytest --alluredir=allure-results
```

Запуск на конкретном браузере:
```bash
pytest --browser=chrome --alluredir=allure-results
pytest --browser=firefox --alluredir=allure-results
```

Запуск на обоих браузерах одной командой (используется `pytest-parallel`-стиль
через переменную окружения либо два последовательных запуска — самый
надёжный вариант, чтобы отчёты не путались, — два прогона в разные папки):
```bash
pytest --browser=chrome  --alluredir=allure-results/chrome
pytest --browser=firefox --alluredir=allure-results/firefox
```

## Просмотр Allure-отчёта

```bash
allure serve allure-results
# или для конкретного браузера:
allure serve allure-results/chrome
```

(Требуется установленный Allure Commandline: `brew install allure` /
`scoop install allure` / см. https://allurereport.org/docs/install/)

## Важное замечание про локаторы

Сайт — React SPA, собранный `create-react-app`: большая часть CSS-классов
захэширована сборщиком (`Modal_modal__xxxxx` и т.п.) и может меняться
между релизами. Поэтому локаторы в POM сознательно построены на
максимально стабильных признаках вместо хэшированных классов:

- ингредиенты ищутся по `alt` у `<img>` (совпадает с названием ингредиента)
  и по структуре карточки, а не по хэш-классам;
- модальное окно ищется через корневой узел портала модалок (`#modals`
  / первый `div` с ролью диалога), кнопка закрытия — по SVG-иконке `icon-close`
  внутри модалки;
- счётчики "Выполнено за всё время" / "Выполнено за сегодня" ищутся по
  соседству с их текстовыми подписями (xpath `following-sibling`), а не
  по классам;
- добавление ингредиента в заказ реализовано через drag&drop, который
  react-dnd (HTML5Backend) не воспринимает через `ActionChains` — поэтому
  используется JS-эмуляция событий `dragstart/dragenter/dragover/drop`
  (см. `utils/js_dnd.py`), это стандартный обходной путь для react-dnd.

Перед первым реальным прогоном рекомендуется свериться с текущей вёрсткой
сайта в DevTools и при необходимости поправить 2-3 локатора в `pages/*.py` —
их вынесено в начало каждого класса единым блоком именно для удобства такой
правки.

## Тестовый пользователь

Для сценария "Лента заказов" (оформление заказа требует авторизации) тест
сам регистрирует нового пользователя через API перед прогоном
(`utils/api_client.py: register_random_user`), а затем прокидывает
полученные токены в браузер (cookie `accessToken` + `localStorage.refreshToken`)
без прохождения формы логина. Пользователь не удаляется автоматически
после теста (публичного API для мягкого удаления аккаунта в проекте нет);
для проекта-задания это ожидаемо и безопасно.
