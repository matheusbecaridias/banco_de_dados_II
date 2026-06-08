"""
calculadora com operações básicas (- + x %)
"""

while True:

    ope = input(
        "Escolha uma operação: 1.Soma, 2.Subtração, 3.Multiplicação ou 4.Divisão: "
    )
    if ope not in ["1", "2", "3", "4"]:
        print("Operação Inválida")
    else:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))

        if ope == "1":
            res = num1 + num2
            print(f"O resultado é {res}")
        elif ope == "2":
            res = num1 - num2
            print(f"O resultado é {res}")
        elif ope == "3":
            res = num1 * num2
            print(f"O resultado é {res}")
        elif ope == "4":
            if num2 != 0:
                res = num1 / num2
                print(f"O resultado é {res}")
            else:
                print(
                    "Dividir um número por zero é uma operação impossível, não tendo um resultado definido ou existente na matemática convencional"
                )

        continuar = input("\nDeseja continuar? (s/n): ")
        if continuar.lower() != "s":
            print("Encerrando calculadora.")
            break
