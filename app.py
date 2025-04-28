import os
from datetime import datetime, timezone, timedelta
import pytz

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Operation Types
DEPOSIT = 1
WITHDRAW = 2
DAILY_WITHDRAW_LIMIT = 10
DAILY_WITHDRAW_LIMIT_VALUE = 500

def reach_daily_withdraws(extrato, today_utc):
    withdraws_made = 0
    withdraws_values = 0

    for statement in extrato:
        operation_withdraw = statement['operation_type'] == WITHDRAW

        if operation_withdraw and statement['operation_date'].date() == today_utc.date():
            withdraws_made += 1
            withdraws_values += statement['value']

    return withdraws_made, withdraws_values
        

def filter_users(cpf, users):
    filtered_users = [user for user in users if user['cpf'] == cpf]
    return filtered_users[0] if filtered_users else None


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


def deposit_option(saldo, extrato, today_utc, /):
    value = float(input("How much do you want to deposit? R$").replace(',', '.'))

    if value > 0 and type(value) == float:
        saldo += value

        extrato.append({
            "operation_index": len(extrato) + 1,
            "operation_date": today_utc,
            "operation_type": DEPOSIT,
            "value": value
        })

        print(f"\nSuccess!")
        print(f"Current balance: R${saldo:.2f}".replace('.', ','))
    else:
        print("Invalid operation: The value must be greater than 0.")

    return saldo, extrato


def withdraw_option(*, saldo, extrato, today_utc, limite):
    withdraws_made, withdraws_values = reach_daily_withdraws(extrato, today_utc)
    exceded_withdraws = withdraws_made >= DAILY_WITHDRAW_LIMIT

    if exceded_withdraws:
        print("You've exceeded the daily withdraws limit.")
    else:
        value = float(input("How much do you want to withdraw? R$").replace(',', '.'))

        if value > saldo:
            print("Invalid operation: The amount exeeds the balance limit.")
        elif value > limite:
            print("Invalid operation: The amount exeeds the daily withdraw limit")
        elif value > 0:
            saldo -= value
            limite -= value
            
            extrato.append({
                "operation_index": len(extrato) + 1,
                "operation_date": today_utc,
                "operation_type": WITHDRAW,
                "value": value
            })

            withdraws_made, withdraws_values = reach_daily_withdraws(extrato, today_utc)

            print(f"\nSuccess!")
            print(f"Withdraws left: {DAILY_WITHDRAW_LIMIT - withdraws_made}")
            print(f"Amount available for withdraw: {DAILY_WITHDRAW_LIMIT_VALUE - withdraws_values}")
            print(f"Current balance: R${saldo:.2f}".replace('.', ','))
        else:
            print("Invalid operation: The value must be greater than 0")
            
    return saldo, extrato, limite


def create_user_option(users):
    cpf = input("Enter your CPF (only numbers): ")
    user = filter_users(cpf, users)

    if user:
        print("There is already a user with this CPF.")
        return
    
    name = input("Insert your full name: ")
    birthday = input("Inform your birthday(dd-mm-yyyy): ")
    address = input("Inform your address(street, number - neighborhood - city): ")

    users.append({"name": name, "birthday": birthday, "cpf": cpf, "address": address})

    print("Success creating new user!")

def create_account_option():
    account = {}

    print("Success creating the account")
    return account

def list_accounts_option():
    account_list = []
    
    for account in account_list:
        print("")

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
    
    show_menu(today_utc, timezone=timezone_brasil)

    while(True):
        opcao = input("\nSelect an option ([m] - Menu): ").upper()

        if opcao == "D":
            saldo, extrato = deposit_option(saldo, extrato, today_utc)
            
        elif opcao == "W":
            saldo, extrato, limite = withdraw_option(
                saldo=saldo, 
                extrato=extrato, 
                today_utc=today_utc, 
                limite=limite)
            
        elif opcao == "S":
            statement_option(saldo, extrato=extrato, timezone=timezone_brasil)
            
        elif opcao == "M":
            show_menu(today_utc, timezone=timezone_brasil)

        elif opcao == "N":
            today_utc = next_day(today_utc)
            show_menu(today_utc, timezone=timezone_brasil)

        elif opcao == "NU":
            create_user_option(users)
            
        elif opcao == "NA":
            create_account_option()
            
        elif opcao == "LA":
            list_accounts_option()
            
        elif opcao == "Q":
            break
        else:
            print("Invalid operation. Select a valid option.")

main()