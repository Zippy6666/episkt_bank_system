from app import app, TransactionResultMessage
from models import Account
from sqlalchemy.sql.expression import func
import unittest


class BankSysTest(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()

    def test_mega_transfer(self):
        ...

    def test_mega_withdrawal(self):
        ...
    
    def test_negative_transaction(self):
        with app.app_context():
            account = Account.query.order_by(func.random()).first()
        
        response = self.test_client.post('/kontobild', data={'id': str(account.id), 'belopp': '-10'})
        self.assertEqual(response.status_code, 200)

        error_msg = TransactionResultMessage.LESS_THAN_ZERO.value

        self.assertIn(error_msg, response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()