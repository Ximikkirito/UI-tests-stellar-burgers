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

