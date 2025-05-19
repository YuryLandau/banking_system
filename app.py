import os
from datetime import datetime, timezone, timedelta
import pytz

from models import Deposit, Withdraw, Client

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Operation models
DEPOSIT = 1
WITHDRAW = 2    
DAILY_WITHDRAW_LIMIT = 10
DAILY_WITHDRAW_LIMIT_VALUE = 500
AGENCY = "0001"

def reach_daily_withdraws(extrato, today_utc):
    withdraws_made = 0
    withdraws_values = 0

    for statement in extrato:
        operation_withdraw = statement['operation_type'] == WITHDRAW

        if operation_withdraw and statement['operation_date'].date() == today_utc.date():
            withdraws_made += 1
            withdraws_values += statement['value']

    return withdraws_made, withdraws_values
        

def filter_clients(cpf, clients: list[Client]) -> Client:
    filtered_clients = [client for client in clients if client['cpf'] == cpf]
    return filtered_clients[0] if filtered_clients else None


def get_client_account(client):
    if not client.accounts:
        print("This user does not have an account")
        return None
    
    return client.accounts[0]


def next_day(today_utc):
     today_utc += timedelta(days=1)
     return today_utc


def show_menu(today_utc, *, timezone):
    timezone
    limpar_terminal()
    print(f"""
    {' Welcome to PyBank '.center(55, "-")}
TODAY: {today_utc.astimezone(timezone).strftime('%d/%m/%Y')}

[d] - Deposit
[w] - Withdraw
[s] - Statement
[nu]- New user
[na]- New bank account
[la]- List accounts
[n] - Next day
[q] - Exit""")


def deposit_option(clients):
    cpf = input("Enter your CPF (only numbers): ")
    client = filter_clients(cpf, clients)

    if not client:
        print("Unable to find that user, it may not exist")
        return
    
    value = float(input("How much do you want to deposit? R$").replace(',', '.'))
    transaction = Deposit(value)

    account = get_client_account(client)
    if not account:
        return
    client.make_transaction(account, transaction)


def withdraw_option(clients):
    cpf = input("Enter your CPF (only numbers): ")
    client = filter_clients(cpf, clients)

    if not client:
        print("Unable to find that user, it may not exist")
        return
    
    value = float(input("How much do you want to withdraw? R$").replace(',', '.'))
    transaction = Withdraw(value)

    account = get_client_account(client)
    if not account:
        return
        
    client.make_transaction(account, transaction)


def create_user_option(users):
    cpf = input("Enter your CPF (only numbers): ")
    user = filter_clients(cpf, users)

    if user:
        print("There is already a user with this CPF.")
        return
    
    name = input("Insert your full name: ")
    birthday = input("Inform your birthday(dd-mm-yyyy): ")
    address = input("Inform your address(street, number - neighborhood - city): ")

    users.append({"name": name, "birthday": birthday, "cpf": cpf, "address": address})

    print("Success creating new user!")


def create_account_option(agency, account_number, users ,/):
    cpf = input("Inform user's CPF: ")
    user = filter_clients(cpf, users)

    if user:
        print("Success creating the account")
        return {
            "agency": agency,
            "account_number": account_number,
            "user": user
        }
    
    print("Unable to find that user, it may not exist")


def list_accounts_option(account_list):
    
    for account in account_list:
        print(f"""
Agency: {account['agency']} Number: {account['account_number']}
Client name: {account['user']['name']}
""")


def statement_option(saldo, /, *, extrato, timezone):
    
    # ===== Statement Header
    print("")
    print(f" My statements in PyBank ".center(55, "="))
    print(f"\nINDEX".center(5)+" |  "+f"DATE TIME".center(20)+" | "+f"OPERATION".center(10)+" | "+"VALUE(R$)")
    print(f"-".center(55, "-"))

    # ===== Statement Logic
    if not len(extrato):
        print("No transactions recorded")
    for statement in extrato:
        operation_type = ""
        operation_sign = ""
        value_string = f"R${statement['value']:.2f}".replace('.', ',')
        formated_date = f"{statement['operation_date'].astimezone(timezone).strftime('%d/%m/%Y %H:%M:%S')}"

        if statement['operation_type'] == 1:
            operation_type = "DEPOSIT"
            operation_sign = "+"
        elif statement['operation_type'] == 2:
            operation_type = "WITHDRAW"
            operation_sign = "-"
        
        print(f"{statement['operation_index']:<5} | {formated_date:<21} | {operation_type:<10} | {operation_sign}{value_string:>12}")
    
    # ===== Statement Footer
    print(f"-".center(28, "-"))
    print(f"Current Ballance: R${saldo:.2f}".replace('.', ','))
    print(f"=".center(55, "="))


def main():
    timezone_brasil = pytz.timezone('America/Sao_Paulo')
    today_utc = datetime.now(timezone.utc)
    saldo = 0
    extrato = []
    limite = DAILY_WITHDRAW_LIMIT_VALUE
    users = []

    clients = []
    accounts = []
    
    show_menu(today_utc, timezone=timezone_brasil)

    while(True):
        option = input("\nSelect an option ([m] - Menu): ").upper()

        if option == "D":
            deposit_option(clients)
            
        elif option == "W":
            withdraw_option(clients)
            
        elif option == "S":
            statement_option(saldo, extrato=extrato, timezone=timezone_brasil)
            
        elif option == "M":
            show_menu(today_utc, timezone=timezone_brasil)

        elif option == "N":
            today_utc = next_day(today_utc)
            show_menu(today_utc, timezone=timezone_brasil)

        elif option == "NU":
            create_user_option(users)
            
        elif option == "NA":
            account_number = len(accounts) + 1
            account = create_account_option(AGENCY, account_number, users)

            if account:
                accounts.append(account)
            
        elif option == "LA":
            list_accounts_option(accounts)
            
        elif option == "Q":
            break
        else:
            print("Invalid operation. Select a valid option.")

main()