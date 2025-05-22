import os
from pasta_4_inscricoes.crud_inscricoes import CrudInscricoes

class MenuInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_inscricoes = CrudInscricoes(gerenciador_bd)
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de inscrições"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE INSCRIÇÕES =====")
        print("1. Adicionar Inscrição")
        print("2. Ver Todas as Inscrições")
        print("3. Ver Inscrições por Evento")
        print("4. Ver Inscrições por Participante")
        print("5. Cancelar Inscrição")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu de inscrições"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                self.limpar_tela()
                self.crud_inscricoes.adicionar_inscricao()
                input("\nPressione Enter para continuar...")
            elif escolha == '2':
                self.limpar_tela()
                self.crud_inscricoes.ver_todas_inscricoes()
                input("\nPressione Enter para continuar...")
            elif escolha == '3':
                self.limpar_tela()
                self.crud_inscricoes.ver_inscricoes_por_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '4':
                self.limpar_tela()
                self.crud_inscricoes.ver_inscricoes_por_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '5':
                self.limpar_tela()
                self.crud_inscricoes.cancelar_inscricao()
                input("\nPressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
