from types import Account, Transaction

class Cliente:
    def __init__(self, address, accounts: list[Account] = []):
        self.address = address
        self.accounts = accounts

    def add_account(self, account: Account):
        self.accounts.append(account)
        print(f"Account added: {account}")

    def make_transaction(self, account: Account, transaction: Transaction):
        transaction.register(account)
        print(f"Transaction made: {transaction}")
    