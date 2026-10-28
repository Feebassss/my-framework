import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.fixtures.db_fixture import db_session
from sqlalchemy.orm import Session

@pytest.mark.api
class TestTransferAccount:
    def test_account_transfer(self, api_manager: ApiManager, transfer_account_request, db_session: Session):
        create_user_req, deposit_account_req, transfer_account_req, id_account1, id_account2 = transfer_account_request
        response = api_manager.user_steps.transfer_account(create_user_req, transfer_account_req)

        assert response.fromAccountId == transfer_account_req.fromAccountId
        assert response.toAccountId == transfer_account_req.toAccountId
        expected_balance = deposit_account_req.amount - transfer_account_req.amount
        assert response.fromAccountIdBalance == expected_balance

        account_from_db = Account.get_account_by_id(db_session, id_account1)
        assert account_from_db.balance == expected_balance

        transaction_from_db_1 = Transaction.get_transaction_by_from_account_id(db_session, id_account1)
        assert transaction_from_db_1.from_account_id == transfer_account_req.fromAccountId

        transaction_from_db_2 = Transaction.get_transaction_by_to_account_id(db_session, id_account2)
        assert transaction_from_db_2.to_account_id == transfer_account_req.toAccountId



    def test_account_transfer_401(self, api_manager: ApiManager, transfer_account_request_401, db_session: Session):
        deposit_account_req, transfer_account_req, id_account1, id_account2 = transfer_account_request_401
        api_manager.user_steps.transfer_account_401(transfer_account_req)

        account_from_db = Account.get_account_by_id(db_session, id_account2)
        assert account_from_db.balance == 0

        transaction_from_db_1 = Transaction.get_transaction_by_from_account_id(db_session, id_account2)
        assert transaction_from_db_1 is None