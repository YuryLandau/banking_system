from decimal import Decimal

from models import Account, Withdraw

class CheckingAccount(Account):
    def __init__(self, number, client, limit: Decimal = Decimal(500.2), withdraw_limit: int = 3):
        super().__init__(number, client)

        self._limit = limit
        self._withdraw_limit = withdraw_limit

    def sacar(self, value: Decimal):
        withdraw_count = len([transaction for transaction in self.history.transactions if transaction['operation_type'] == Withdraw.__name__])

        limit_exceeded = value > self._limit
        withdraw_exceeded = withdraw_count >= self._withdraw_limit

        if limit_exceeded:
            print("Invalid Operation: The withdrawal amount exceeds the account limit.")
        
        elif withdraw_exceeded:
            print("Invalid Operation: The withdrawal limit has been reached.")
        
        else:
            # Chama o método sacar da classe pai
            return super().withdraw(value)
        
        return False
    
    def __str__(self):
        return f"""
Agência: {self._bank_branch}
Número: {self.number}
Cliente: {self.client.name}
Saldo atual: {self.balance:.2f}
        """