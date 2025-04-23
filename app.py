import os
from datetime import datetime, timezone, timedelta
import pytz

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

fuso_brasil = pytz.timezone('America/Sao_Paulo')
today_utc = datetime.now(timezone.utc)

# Operation Types
DEPOSIT = 1
WITHDRAW = 2

saldo = 0
# statement_model = {
#     "operation_index": 1,
#     "operation_date": today_utc,      
#     "operation_type": DEPOSIT,
#     "value": saldo
# }
extrato = []
DAILY_WITHDRAW_LIMIT = 10

def reach_daily_withdraws():
    count_withdraws = 0
    global today_utc

    for statement in extrato:
        operation_withdraw = statement['operation_type'] == WITHDRAW

        if operation_withdraw and statement['operation_date'].date() == today_utc.date():
            count_withdraws += 1

    return count_withdraws
        
def next_day():
     global today_utc
     today_utc += timedelta(days=1)
     return today_utc

def get_actual_date():
    return today_utc

def showMenu():
    global fuso_brasil
    limpar_terminal()
    print(f"""
    {' Welcome to PyBank '.center(55, "-")}
TODAY: {get_actual_date().astimezone(fuso_brasil).strftime('%d/%m/%Y')}

[d] - Deposit
[w] - Withdraw
[s] - Statement
[q] - Exit
[n] - Next Day""")

def deposit_option():
    value = float(input("How much do you want to deposit? R$").replace(',', '.'))
    global saldo

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

def withdraw_option():
    withdraws_made = reach_daily_withdraws()
    exceded_withdraws = withdraws_made >= DAILY_WITHDRAW_LIMIT
    global saldo

    if exceded_withdraws:
        print("You've exceeded the daily withdraws limit.")
    else:
        value = float(input("How much do you want to withdraw? R$").replace(',', '.'))

        if value > saldo:
            print("Invalid operation: The amount exeeds the balance limit.")
        elif value > 0:
            saldo -= value
            
            extrato.append({
                "operation_index": len(extrato) + 1,
                "operation_date": today_utc,
                "operation_type": WITHDRAW,
                "value": value
            })

            withdraws_made = reach_daily_withdraws()

            print(f"\nSuccess!")
            print(f"Withdraws left: {DAILY_WITHDRAW_LIMIT - withdraws_made}")
            print(f"Current balance: R${saldo:.2f}".replace('.', ','))
        else:
            print("Invalid operation: The value must be greater than 0")

def statement_option():
    global extrato
    
    print("")
    print(f" My statements in PyBank ".center(55, "="))
    print(f"\nINDEX".center(5)+" |  "+f"DATE TIME".center(20)+" | "+f"OPERATION".center(10)+" | "+"VALUE(R$)")
    print(f"-".center(55, "-"))

    if not len(extrato):
        print("No transactions recorded")
    for statement in extrato:
        operation_type = ""
        operation_sign = ""
        value_string = f"R${statement['value']:.2f}".replace('.', ',')
        formated_date = f"{statement['operation_date'].astimezone(fuso_brasil).strftime('%d/%m/%Y %H:%M:%S')}"

        if statement['operation_type'] == 1:
            operation_type = "DEPOSIT"
            operation_sign = "+"
        elif statement['operation_type'] == 2:
            operation_type = "WITHDRAW"
            operation_sign = "-"
        
        print(f"{statement['operation_index']:<5} | {formated_date:<21} | {operation_type:<10} | {operation_sign}{value_string}")
    
    print(f"-".center(28, "-"))
    print(f"Current Ballance: R${saldo:.2f}".replace('.', ','))
    print(f"=".center(55, "="))

showMenu()

while(True):
    opcao = input("\nSelect an option ([m] - Menu): ").upper()

    if opcao == "D":
        deposit_option()
        
    elif opcao == "W":
        withdraw_option()
        
    elif opcao == "S":
        statement_option()
        
    elif opcao == "M":
        showMenu()

    elif opcao == "N":
        next_day()
        showMenu()
        
    elif opcao == "Q":
        break
    else:
        print("Invalid operation. Select a valid option.")