import os
from .crud_participantes import CrudParticipantes

class MenuParticipantes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_participantes = CrudParticipantes(gerenciador_bd)
    
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
                self.limpar_tela()
                self.crud_participantes.adicionar_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '2':
                self.limpar_tela()
                self.crud_participantes.visualizar_participantes()
                input("\nPressione Enter para continuar...")
            elif escolha == '3':
                self.limpar_tela()
                self.crud_participantes.detalhes_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '4':
                self.limpar_tela()
                self.crud_participantes.atualizar_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '5':
                self.limpar_tela()
                self.crud_participantes.excluir_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '6':
                self.limpar_tela()
                self.crud_participantes.buscar_participantes()
                input("\nPressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
