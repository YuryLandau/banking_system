from abc import ABC, abstractmethod
from models import Account

class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass


    @abstractmethod
    def register(self, account: Account):
        
        pass
        