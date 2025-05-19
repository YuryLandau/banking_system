from decimal import Decimal
from typing import TypedDict

from models.History import History

class Account:
    def __init__(self, number: int, client):
        self._balance = Decimal(0.0)
        self._number = number
        self._bank_branch = "0001"
        self._client = client
        self._history = History()
    
    @property
    def balance(self) -> Decimal:
        return Decimal(self._balance)
    
    @property
    def number(self):
        return self._number
    
    @property
    def bank_branch(self) -> str:
        return self._bank_branch
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self, value) -> bool:
        balance = self.balance
        excedeeded_balance = Decimal(value) > balance

        if excedeeded_balance:
            print("Invalid Operation: The withdrawal amount exceeds the account balance.")

        elif value > 0:
            self._balance -= Decimal(value)
            print(f"Amount withdrawn: {value}")
            return True

        else:
            print(f"Invalid Operation: The withdrawal amount must be greater than zero.")
        return False

    def deposit(self, value) -> bool:
        if value <= 0:
            print("Invalid Operation: The deposit amount must be greater than zero.")

            return False
        
        self._balance += Decimal(value)
        print(f"Amount deposited: {value}")
        print(f"Current balance: {self._balance}")
        
        return True

    ## ======= Factory Method =======
    @classmethod
    def new_account(cls, number: int, client) -> "Account":
        return cls(number, client)
    
