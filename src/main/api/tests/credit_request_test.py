import pytest
from requests import Session, session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRequest():
    def test_credit_creation(self, api_manager, create_user_request_credit, db_session: Session):
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        id_account = acc.id

        credit_request = CreditRequestRequest(accountId=id_account, amount=7000, termMonths=12)
        response = api_manager.user_steps.credit_request(credit_request, create_user_request_credit)

        assert response.amount == credit_request.amount
        assert response.termMonths == credit_request.termMonths

        credit_from_db = Credit.get_credit_by_account_id(db_session, id_account)
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -credit_request.amount



    def test_account_creation_404(self, api_manager : ApiManager, create_user_request_credit: CreateUserRequest, db_session: Session):
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        id_account = acc.id

        credit_request_1 = CreditRequestRequest(accountId=id_account, amount=7000, termMonths=12)
        api_manager.user_steps.credit_request(credit_request_1, create_user_request_credit)

        credit_request_2 = CreditRequestRequest(accountId=id_account, amount=7000, termMonths=12)
        api_manager.user_steps.credit_request_invalid_404(credit_request_2, create_user_request_credit)

        credit_from_db = Credit.get_credit_by_account_id_all(db_session, id_account)
        assert len(credit_from_db) == 1