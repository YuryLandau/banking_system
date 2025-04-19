import os

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

menu = f"""
    {'Welcome to PyBank'.center(30, "-")}

[d] - Deposit
[w] - Withdraw
[e] - Statement
[q] - Exit"""

# Operation Types
DEPOSIT = 1
WITHDRAW = 2

saldo = 0
# statement_model = {
#     "operation_index": 1,
#     "operation_type": DEPOSIT,
#     "value": saldo
# }
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

print(menu)

while(True):
    opcao = input("\nSelect an option ([m] - Menu): ").upper()

    if opcao == "D":
        value = float(input("How much do you want to deposit? R$").replace(',', '.'))

        if value > 0:
            saldo += value

            extrato.append({
                "operation_index": len(extrato) + 1,
                "operation_type": DEPOSIT,
                "value": value
            })

            print(f"\nSuccess!")
            print(f"Current balance: R${saldo:.2f}".replace('.', ','))
        else:
            print("Invalid operation: The value must be greater than 0.")
    elif opcao == "W":
        exceded_withdraws = numero_saques >= LIMITE_SAQUES

        if exceded_withdraws:
            print("You've exceeded the daily withdraws limit.")

        value = float(input("How much do you want to withdraw? R$").replace(',', '.'))

        if value > saldo:
            print("Invalid operation: The amount exeeds the balance limit.")
        elif value > 0:
            saldo -= value
            
            extrato.append({
                "operation_index": len(extrato) + 1,
                "operation_type": WITHDRAW,
                "value": value
            })

            numero_saques += 1

            print(f"\nSuccess!")
            print(f"Withdraws left: {LIMITE_SAQUES - numero_saques}")
            print(f"Current balance: R${saldo:.2f}".replace('.', ','))
        else:
            print("Invalid operation: The value must be greater than 0")
    elif opcao == "E":
        print("")
        print(f"My statements in PyBank".center(35, "="))
        print(f"\nINDEX".center(5)+" | "+f"OPERATION".center(10)+" | "+"VALUE(R$)")
        print(f"-".center(35, "-"))

        if not len(extrato):
            print("No transactions recorded")
        for statement in extrato:
            operation_type = ""
            operation_sign = ""
            value_string = f"{statement['value']:.2f}".replace('.', ',')

            if statement['operation_type'] == 1:
                operation_type = "DEPOSIT"
                operation_sign = "+"
            elif statement['operation_type'] == 2:
                operation_type = "WITHDRAW"
                operation_sign = "-"
            
            print(f"{statement['operation_index']:<5} | {operation_type:<10} | {operation_sign}R${value_string}")
        
        print(f"Current Ballance: R${saldo:.2f}".replace('.', ','))
        print(f"=".center(35, "="))
    elif opcao == "M":
        limpar_terminal()
        print(menu)
    elif opcao == "Q":
        break
    else:
        print("Invalid operation. Select a valid option.")