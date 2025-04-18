menu = f"""
    {'Welcome to PyBank'.center(30, "-")}

[d] - Deposit
[w] - Withdraw
[e] - Statement
[q] - Exit
"""

saldo = 5000
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

print(menu)

while(True):
    opcao = input("Select an option: ").upper()

    if opcao == "D":
        print("Deposit")

    elif opcao == "W":
        print("Withdraw")

    elif opcao == "E":
        print("Statement")

    elif opcao == "Q":
        break

    else:
        print("Invalid operation. Select a valid option.")