import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.auth_login_request import AuthLoginRequest

@pytest.mark.api
class TestAuthAdmin:
    def test_auth_admin_valid(self, api_manager):
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(auth_admin_request)

        assert response.user.username == auth_admin_request.username
        assert response.user.role == "ROLE_ADMIN"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("", "123456"),
            ("admin", ""),
        ]
    )

    # негативный тест авторизации на 400 ошибку
    def test_auth_admin_invalid_400(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username=username, password=password)

        api_manager.admin_steps.login_user_invalid400(auth_admin_request)

    @pytest.mark.parametrize(
        "username, password",
        [
            ("admi", "123456"),
            ("admin", "12456"),
        ]
    )

    # негативный тест авторизации на 401 ошибку
    def test_auth_admin_invalid_401(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username=username, password=password)

        api_manager.admin_steps.login_user_invalid401(auth_admin_request)


    def test_auth_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role


    def test_auth_user_invalid(self, create_user_request, api_manager):
        auth_admin_request = AuthLoginRequest(username="max000", password="Pas!sw0rd")
        api_manager.admin_steps.login_user_invalid401(auth_admin_request)