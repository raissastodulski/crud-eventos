import os
from pasta_4_inscricoes.crud_inscricoes import CrudInscricoes

class MenuInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_inscricoes = CrudInscricoes(gerenciador_bd)
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE INSCRIÇÕES =====")
        print("1. Adicionar inscrição")
        print("2. Ver todas as inscrições")
        print("3. Ver inscrições por atividade")
        print("4. Ver inscrições por evento")
        print("5. Ver inscrições por participante")
        print("6. Cancelar inscrição")
        print("0. Voltar ao menu principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
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
                self.crud_inscricoes.ver_inscricoes_por_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == '4':
                self.limpar_tela()
                self.crud_inscricoes.ver_inscricoes_por_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '5':
                self.limpar_tela()
                self.crud_inscricoes.ver_inscricoes_por_participante()
                input("\nPressione Enter para continuar...")
            elif escolha == '6':
                self.limpar_tela()
                self.crud_inscricoes.cancelar_inscricao()
                input("\nPressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
