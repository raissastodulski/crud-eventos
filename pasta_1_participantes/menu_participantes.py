import os

def atualizar_participante(nome_antigo):

    categoria = 0
    for participante in participantes:
        if participante['nome'] == nome_antigo:
            break
    else:
        print(f"Participante com nome '{nome_antigo}' não encontrado.")
        return
    while categoria != 5:
        
        print("Escolha a categoria que você deseja editar")
        print("~"*34)
        print("  Categorias")
        print("~"*34)

        print("1 - Nome")
        print("2 - Email")
        print("3 - CPF")
        print("4 - Telefone")
        print("5 - Sair")
        categoria = int(input("Informe a opção desejada: "))

        if categoria == 1:
            novo_nome = input("Informe o novo nome do usuario:")
            for participante in participantes:
                if participante['nome'] == nome_antigo:
                    participante['nome'] = novo_nome
                    nome_antigo = novo_nome
            
        
        elif categoria == 2:
            novo_email = input("Informe o novo email do usuario:")
            for participante in participantes:
                if participante['nome'] == nome_antigo:
                    participante['email'] = novo_email
            

        elif categoria == 3:
            novo_cpf = input("Informe o novo cpf do usuario:")
            for participante in participantes:
                if participante['nome'] == nome_antigo:
                    participante['cpf'] = novo_cpf
                

        elif categoria == 4:
            novo_telefone = input("Informe o novo telefone do usuario:")
            for participante in participantes:
                if participante['nome'] == nome_antigo:
                    participante['telefone'] = novo_telefone
    

        elif categoria == 5:
            print("Saíndo da edição")
            break

        else:
            print("Opção inválida")

class MenuParticipantes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de participantes"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE PARTICIPANTES =====")
        print("1. Adicionar Participante")
        print("2. Ver Todos os Participantes")
        print("3. Ver Detalhes do Participante")
        print("4. Atualizar Participante")
        print("5. Excluir Participante")
        print("6. Buscar Participantes")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu de participantes"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                print("\nAdicionar Participante (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '2':
                if not participantes:
                    print("Nenhum participante cadastrado.")
                else:
                    print("\nVer Todos os Participantes ")
                    print("-" * 40)
                    for participante in participantes:
                        print(f"Nome: {participante['nome']}")
                        print(f"E-mail: {participante['email']}")
                        print(f"CPF: {participante['cpf']}")
                        print(f"Telefone: {participante['telefone']}")
                        print("-" * 40)
            elif escolha == '3':
                print("\nVer Detalhes do Participante (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '4':
                print("\nAtualizar Participante (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '5':
                print("\nExcluir Participante (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '6':
                print("\nBuscar Participantes (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")