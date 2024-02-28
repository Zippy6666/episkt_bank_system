from app import app, TransactionResultMessage, get_user
from models import Account
from sqlalchemy.sql.expression import func
from flask_login import login_user
import unittest


class BankSysTest(unittest.TestCase):
    def setUp(self):
        app.testing=True
        self.test_client = app.test_client(use_cookies=True)
        login_user( get_user("stefan.holmberg@systementor.se") )

    def test_mega_transfer(self):
        ...

    def test_mega_withdrawal(self):
        ...
    
    def test_negative_transaction(self):
        # Random account to test on
        account = Account.query.order_by(func.random()).first()

        # Post request
        response = self.test_client.post(f"/kontobild?id={account.id}", data={"belopp":"-10"})
        self.assertEqual(response.status_code, 200)

        # Did we get the less than 0 error message?
        self.assertIn(TransactionResultMessage.LESS_THAN_ZERO.value, response.data.decode('utf-8'))


if __name__ == '__main__':
    with app.test_request_context():
        unittest.main()