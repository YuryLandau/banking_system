from abc import ABC, abstractmethod
from models import Account

class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @property
    @abstractmethod
    def date(self):
        return self._date

    @abstractmethod
    def register(self, account: Account):
        
        pass
        