from datetime import date
from models.Client import Client

class Individual(Client):
    def __init__(self, name: str, cpf: str, birthday: date, address: str):
        super().__init__(address)
        self.name = name
        self.cpf = cpf
        self.birthday = birthday
