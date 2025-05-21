import os
import sys
sys.path.append('.')
from pasta_3_atividades import atividade

class MenuAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de atividades"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE ATIVIDADES =====")
        print("1. Adicionar Atividade")
        print("2. Ver Todas as Atividades")
        print("3. Ver Detalhes da Atividade")
        print("4. Atualizar Atividade")
        print("5. Excluir Atividade")
        print("6. Buscar Atividades")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu de atividades"""
        # Passar a conexão com o banco de dados para o módulo atividade
        atividade.gerenciador_bd = self.gerenciador_bd
        
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                print("\nAdicionar Atividade")
                atividade.criar_atividade()
                input("Pressione Enter para continuar...")
            elif escolha == '2':
                print("\nVer Todas as Atividades")
                atividade.visualizar_atividade()
                input("Pressione Enter para continuar...")
            elif escolha == '3':
                print("\nVer Detalhes da Atividade (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '4':
                print("\nAtualizar Atividade")
                atividade.editar_atividade()
                input("Pressione Enter para continuar...")
            elif escolha == '5':
                print("\nExcluir Atividade ")
                atividade.excluir_atividade()
                input("Pressione Enter para continuar...")
            elif escolha == '6':
                print("\nBuscar Atividades (em desenvolvimento)")
                input("Pressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")