from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_auth_standard_user(page):
    steps = LoginSteps(page)

    steps.open_login_page().login("standard_user", "secret_sauce")
    expect(page).to_have_url(CatalogPage.URL)


def test_auth_logout_standard_user(page):
    login_steps = LoginSteps(page)
    login_catalog = CatalogSteps(page)

    login_steps.open_login_page().login("standard_user", "secret_sauce")
    expect(page).to_have_url(CatalogPage.URL)

    login_catalog.logout()

def test_auth_logout_visual_user(page):
    login_steps = LoginSteps(page)
    login_catalog = CatalogSteps(page)

    login_steps.open_login_page().login("visual_user", "secret_sauce")
    expect(page).to_have_url(CatalogPage.URL)

    login_catalog.logout()

def test_auth_invalid_locked_out_user(page):
    login_steps = LoginSteps(page)
    error_text = login_steps.open_login_page().login("locked_out_user", "secret_sauce").login_page.get_error_text()

    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"