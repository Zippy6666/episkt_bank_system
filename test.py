from app import app, TransactionResultMessage, get_user
from models import Account
from sqlalchemy.sql.expression import func
from flask_login import login_user
import unittest


class BankSysTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.test_client()

        # Random account to test on
        self.test_account = Account.query.order_by(func.random()).first()

        login_user(get_user("stefan.holmberg@systementor.se"))

    def test_mega_transfer(self):
        # Another random account to transfer to, that is not self.test_account
        receiving_account = (
            Account.query.filter(Account.id != self.test_account.id)
            .order_by(func.random())
            .first()
        )

        response = self.test_client.post(
            f"/kontobild?id={self.test_account.id}",
            data={
                "belopp": "1000000000",
                "transaction_type": "överför",
                "transfer_accountnr": receiving_account.kontonummer,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            TransactionResultMessage.INSUFFICIENT_FUNDS.value,
            response.data.decode("utf-8"),
        )

    def test_mega_withdrawal(self):
        response = self.test_client.post(
            f"/kontobild?id={self.test_account.id}",
            data={"belopp": "1000000000", "transaction_type": "uttag"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            TransactionResultMessage.INSUFFICIENT_FUNDS.value,
            response.data.decode("utf-8"),
        )

    def test_negative_transaction(self):
        response = self.test_client.post(
            f"/kontobild?id={self.test_account.id}", data={"belopp": "-10"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            TransactionResultMessage.LESS_THAN_ZERO.value, response.data.decode("utf-8")
        )


if __name__ == "__main__":
    with app.test_request_context():
        unittest.main()
