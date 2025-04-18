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

saldo = 5000.00
statement_model = {
    "operation_index": 1,
    "operation_type": DEPOSIT,
    "value": saldo
}
extrato = [statement_model]
numero_saques = 0
LIMITE_SAQUES = 3

print(menu)

while(True):
    opcao = input("\nSelect an option ([m] - Menu): ").upper()

    if opcao == "D":
        valor = float(input("How much you want to deposit? R$").replace(',', '.'))

        if valor > 0:
            saldo += valor

            extrato.append({
                "operation_index": len(extrato) + 1,
                "operation_type": DEPOSIT,
                "value": valor
            })

            print(f"\nSuccess!")
            print(f"Current balance: R${saldo:.2f}".replace('.', ','))

    elif opcao == "W":
        print("Withdraw")

    elif opcao == "E":
        print("")
        print(f"My statements in PyBank".center(35, "-"))
        for statement in extrato:
            operation_type = ""
            value_string = f"{statement['value']:.2f}".replace('.', ',')

            if statement['operation_type'] == 1:
                operation_type = "DEPOSIT"
            elif statement['operation_type'] == 2:
                operation_type = "WITHDRAW"
            
            print(f"{statement['operation_index']} - {operation_type} - R${value_string}")

    elif opcao == "M":
        limpar_terminal()
        print(menu)

    elif opcao == "Q":
        break

    else:
        print("Invalid operation. Select a valid option.")