import pytest
from sqlalchemy.orm import Session

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self, api_manager, db_session: Session):
        # Позиитвное создание пользователя - статус 200
        create_user_request = CreateUserRequest(username="dsafddd123", password="Pas!sw0rd", role="ROLE_USER")
        response = api_manager.admin_steps.create_user(create_user_request)


        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username

    @pytest.mark.parametrize(
        "username, password",
        [
            ("Александр", "Pas!sw0rd"), # кириллица
            ("YT", "Pas!sw0rd"), # минимум 3 символа
            ("qwertqwertqwerty1", "Pas!sw0rd"), # максимум 15 символов
            ("Ytro", "Pas!s"), # менее 8 символов
            ("Ytro", "Password!"), # без цифры
            ("Ytro", "Pas02321wrd"), # без спец. символов
            ("Ytro", "paas!swo01r") # без заглавной буквы
        ]
    )

    def test_create_user_invalid_400(self, username, password, api_manager, db_session: Session):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_400(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан - ошибка"


    def test_create_user_invalid_401(self, api_manager, db_session: Session):
        create_user_request = CreateUserRequest(username="Alex22s00022", password="Pass!sw0rd", role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_401(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан - ошибка"