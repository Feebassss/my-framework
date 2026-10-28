import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session

from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDepositAccount:
    def test_account_deposit_valid(self, api_manager: ApiManager, deposit_account_request, db_session: Session):
        create_user_req, deposit_account_req = deposit_account_request
        response = api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)
        assert response.balance == deposit_account_req.amount

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db.balance == deposit_account_req.amount, "Баланс в БД не совпадает с суммой пополения"


    def test_account_deposit_400(self, api_manager, deposit_account_request_400, db_session: Session):
        create_user_req, deposit_account_req = deposit_account_request_400
        api_manager.user_steps.deposit_account_400(create_user_req, deposit_account_req)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет не существует"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 400"


    def test_account_deposit_401(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request_401, db_session: Session):
        create_user_req, deposit_account_req = deposit_account_request_401
        api_manager.user_steps.deposit_account_401(deposit_account_req)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет не существует"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 401"