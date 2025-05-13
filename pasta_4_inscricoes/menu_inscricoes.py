import os

class MenuInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de inscrições"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE INSCRIÇÕES =====")
        print("1. Adicionar Inscrição")
        print("2. Ver Todas as Inscrições")
        print("3. Ver Detalhes da Inscrição")
        print("4. Atualizar Inscrição")
        print("5. Excluir Inscrição")
        print("6. Buscar Inscrições")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu de inscrições"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                print("\nAdicionar Inscrição (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '2':
                print("\nVer Todas as Inscrições (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '3':
                print("\nVer Detalhes da Inscrição (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '4':
                print("\nAtualizar Inscrição (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '5':
                print("\nExcluir Inscrição (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '6':
                print("\nBuscar Inscrições (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")