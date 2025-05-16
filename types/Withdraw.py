from types import Account, Transaction
from decimal import Decimal


class Withdraw(Transaction):
    def __init__(self, value: Decimal = Decimal(0.0), account:Account = None):
        super().__init__(account)
        self._value = Decimal(value)

    @property
    def value(self):
        return self._value

    def register(self, account: Account):
        transaction_success = account.withdraw(self._value)

        if transaction_success:
            account.history.add_transaction(self)
            print(f"Withdrawal of R${self._value:.2f} made successfully.".replace('.', ','))