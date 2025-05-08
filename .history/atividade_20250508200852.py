import datetime

atividades = []


def menu():
    print("------MODULO DE ATIVIDADE-----")

    print("\n >>> Menu de Atividade <<<\n")
    print("1 - Criar Atividade")
    print("2 - Visualizar Atividade")
    print("3 - Editar Atividade")
    print("4 - Excluir Atividade")
    print("5 - Encerra o Programa")

    
def criar():
    nome = input("\nDigite o nome da atividade: ")
    facilitador = input("Digite o nome do responsável da atividade: ")
    horario_str = input("Digite a hora que começa a atividade (hh:mm): ")
    horario = datetime.datetime.strptime(horario_str, "%H:%M").strftime("%H:%M")
    local = input("Digite o local da atividade: ")
    vagas = int(input("Digite a quantidade de vagas: "))

    atividade = {
            "nome":nome,
            "facilitador":facilitador,
            "horario":horario,
            "local": local,
            "vagas":vagas
    }

    atividades.append(atividade)
    print(f"\nA atividade {nome} foi cadastrada com sucesso!\n")

def editar():
    if atividades:
            print("\n--- Editar Atividade ---")
            for i, atividade in enumerate(atividades):
                print(f"{i+1}. Nome: {atividade['nome']}")
                print(f"   Responsável: {atividade['facilitador']}")
                print(f"   Horário: {atividade['horario']}")
                print(f"   Local: {atividade['local']}")
                print(f"   Vagas: {atividade['vagas']}")
            indice_editar = int(input("Digite o número da atividade que deseja excluir: ")) - 1 
            if 0 <= indice_editar < len(atividades):
                atividade = atividades[indice_editar]

                print("\nCampos disponíveis para edição: nome, facilitador, horario, local, vagas\n")
                campo_editar = input("Digite o campo que deseja editar: ").lower()

                if campo_editar in atividade:
                    novo_valor = input(f"Digite o novo valor para {campo_editar}: ")
                atividade[campo_editar] = novo_valor
                print(f"\nCampo {campo_editar} atualizado com sucesso!\n")

while True:

    menu()

    opcao = int(input("\nDigite a opção desejada: "))
    if(opcao == 1):
        criar()    
    elif (opcao == 3):
        editar()
    elif (opcao == 5):
        import cadastramentoEvento
        cadastramentoEvento.m
        break
    else:
        print("\nOpção inválida! Digite novamente. \n")