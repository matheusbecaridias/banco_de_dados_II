def chamado():
    tecnico = input("Digite seu nome completo: ")
    equipamento = input("O atendimento é para qual equipamento? ")
    problema = input("Descreva o problema: ")
    prioridade = input("Qual o nível de prioridade? 1.Alto, 2.Médio ou 3.Baixo: ")

    print("\n=== Chamado aberto com sucesso! ===")
    print(f"Técnico: {tecnico}")
    print(f"Equipamento: {equipamento}")
    print(f"Problema: {problema}")
    print(f"Prioridade: {prioridade}")
    return {
        "tecnico": tecnico,
        "equipamento": equipamento,
        "problema": problema,
        "prioridade": prioridade,
    }


def finalizar_chamado():
    print("Função de finalizar chamado ainda não implementada.")
    return None


def ranking_tecnicos():
    print("Função de ranking de técnicos ainda não implementada.")
    return None


def dashboard():
    print("Função de dashboard ainda não implementada.")
    return None


# Programa principal
def main():
    while True:
        print("\n=== Menu principal ===")
        print("1. Abrir chamado")
        print("2. Finalizar chamado")
        print("3. Ranking de técnicos")
        print("4. Dashboard")
        print("5. Sair do sistema")

        entrada = input("Escolha uma opção: ")

        if entrada == "1":
            chamado()
        elif entrada == "2":
            finalizar_chamado()
        elif entrada == "3":
            ranking_tecnicos()
        elif entrada == "4":
            dashboard()
        elif entrada == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Executar o programa
if __name__ == "__main__":
    main()
