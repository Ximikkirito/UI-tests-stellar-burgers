import uuid
import allure
import requests

API_BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.step("Зарегистрировать нового случайного пользователя через API")
def register_random_user() -> dict:
    """Регистрирует нового пользователя напрямую через API (в обход UI),
    чтобы не засорять тесты формой регистрации и получить токены для
    последующей авторизации в браузере.

    Возвращает dict с ключами: email, password, name, accessToken, refreshToken.
    """
    unique = uuid.uuid4().hex[:12]
    payload = {
        "email": f"stellar.qa.{unique}@yandex.ru",
        "password": "Qa12345!",
        "name": f"qa_{unique}",
    }

    response = requests.post(f"{API_BASE_URL}/auth/register", json=payload, timeout=10)
    response.raise_for_status()
    body = response.json()

    return {
        **payload,
        "accessToken": body["accessToken"],
        "refreshToken": body["refreshToken"],
    }


@allure.step("Удалить тестового пользователя через API")
def delete_user(access_token: str):
    """Удаляет тестового пользователя по окончании теста, если API это
    поддерживает. Ошибки не считаются фатальными для теста."""
    try:
        requests.delete(
            f"{API_BASE_URL}/auth/user",
            headers={"Authorization": access_token},
            timeout=10,
        )
    except requests.RequestException:
        pass
