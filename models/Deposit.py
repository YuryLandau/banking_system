from datetime import datetime
from models import Account, Transaction
from decimal import Decimal


class Deposit(Transaction):
    def __init__(self, value: Decimal = Decimal(0.0), date: datetime = datetime.now()):
        self._value = Decimal(value)
        self._date = date

    @property
    def value(self):
        return self._value
    
    @property
    def date(self):
        return self._date

    def register(self, account: Account):
        transaction_success = account.deposit(self._value)

        if transaction_success:
            account.history.add_transaction(self)
            print(f"Deposit of R${self._value:.2f} made successfully.".replace('.', ','))