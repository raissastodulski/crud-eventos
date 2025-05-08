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

def editar()

while True:

    menu()

    opcao = int(input("\nDigite a opção desejada: "))
    if(opcao == 1):
        criar()    
    elif (opcao == 3):
        
    elif (opcao == 5):
        print("Programa encerrado")
        break
    else:
        print("\nOpção inválida! Digite novamente. \n")