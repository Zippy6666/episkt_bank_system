from app import app, TransactionResultMessage, load_user, get_user
from models import Account
from sqlalchemy.sql.expression import func
from flask_login import login_user
import unittest


class BankSysTest(unittest.TestCase):
    def setUp(self):
        app.testing=True
        self.test_client = app.test_client(use_cookies=True)

    def test_mega_transfer(self):
        ...

    def test_mega_withdrawal(self):
        ...
    
    def test_negative_transaction(self):
        # Load an admin user
        user = get_user("stefan.holmberg@systementor.se")
        # load_user(user.id)
        login_user(user)

        # Get a random account
        account = Account.query.order_by(func.random()).first()


        response = self.test_client.post("/kontobild", data=dict(id=account.id, belopp=-10))
        self.assertEqual(response.status_code, 200)

        error_msg = TransactionResultMessage.LESS_THAN_ZERO.value

        self.assertIn(error_msg, response.data.decode('utf-8'))


if __name__ == '__main__':
    with app.test_request_context():
        unittest.main()