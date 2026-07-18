import sys
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.api_client import register_random_user  # noqa: E402


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для прогона тестов: chrome или firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запустить браузер в headless-режиме",
    )


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture
def driver(request, browser_name):
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        driver_ = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver_ = webdriver.Firefox(options=options)
        driver_.set_window_size(1920, 1080)
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}. Используйте chrome или firefox.")

    yield driver_

    # прикрепляем скриншот к Allure-отчёту, если тест упал
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        allure.attach(
            driver_.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )

    driver_.quit()


@pytest.fixture
def authorized_user():
    """Регистрирует нового пользователя через API и отдаёт его данные и
    токены тесту, не открывая форму логина в браузере."""
    return register_random_user()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат каждой фазы теста в item, чтобы фикстура driver
    могла узнать, упал ли тест, и приложить скриншот к Allure-отчёту."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)
        with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
            f.write(f"browser={config.getoption('--browser')}\n")
            f.write("site=https://stellarburgers.education-services.ru\n")
