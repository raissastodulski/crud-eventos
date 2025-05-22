import os
from pasta_3_atividades.atividade import CrudAtividades

class MenuAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_atividades = CrudAtividades(gerenciador_bd)
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de atividades"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE ATIVIDADES =====")
        print("1. Adicionar Atividade")
        print("2. Ver Todas as Atividades")
        print("3. Ver Atividades por Evento")
        print("4. Ver Detalhes da Atividade")
        print("5. Atualizar Atividade")
        print("6. Excluir Atividade")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu de atividades"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                self.limpar_tela()
                self.crud_atividades.adicionar_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == '2':
                self.limpar_tela()
                self.crud_atividades.ver_todas_atividades()
                input("\nPressione Enter para continuar...")
            elif escolha == '3':
                self.limpar_tela()
                self.crud_atividades.ver_atividades_por_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '4':
                self.limpar_tela()
                self.crud_atividades.ver_detalhes_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == '5':
                self.limpar_tela()
                self.crud_atividades.atualizar_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == '6':
                self.limpar_tela()
                self.crud_atividades.excluir_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
