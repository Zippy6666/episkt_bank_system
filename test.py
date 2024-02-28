from app import app, TransactionResultMessage, get_user
from models import Account
from sqlalchemy.sql.expression import func
from flask_login import login_user
import unittest


class BankSysTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.test_client()
        self.test_account = Account.query.order_by(
            func.random()
        ).first()  # Random account to test
        login_user(get_user("stefan.holmberg@systementor.se"))

    def test_mega_transfer(self):
        # response = self.test_client.post("", data={})
        # self.assertEqual(response.status_code, 200)
        ...

    def test_mega_withdrawal(self):
        # response = self.test_client.post("", data={})
        # self.assertEqual(response.status_code, 200)
        ...

    def test_negative_transaction(self):
        """Test negative transaction.
        Transaction type is not required since the app will immedietly notice that the sum is negative,
        and throw the same error message."""

        # Post request
        response = self.test_client.post(
            f"/kontobild?id={self.test_account.id}", data={"belopp": "-10"}
        )
        self.assertEqual(response.status_code, 200)

        # Did we get the less than 0 error message?
        self.assertIn(
            TransactionResultMessage.LESS_THAN_ZERO.value, response.data.decode("utf-8")
        )


if __name__ == "__main__":
    with app.test_request_context():
        unittest.main()
