import os
from pasta_4_inscricoes import CrudInscricoes

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
        print("6. Ver detalhes de uma inscrição")
        print("7. Cancelar inscrição")
        print("0. Voltar ao menu principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            self.limpar_tela()
            
            if escolha == '1':
                self.crud_inscricoes.adicionar_inscricao()
            elif escolha == '2':
                self.crud_inscricoes.ver_todas_inscricoes()
            elif escolha == '3':
                self.ver_inscricoes_por_atividade()
            elif escolha == '4':
                self.ver_inscricoes_por_evento()
            elif escolha == '5':
                self.ver_inscricoes_por_participante()
            elif escolha == '6':
                self.ver_detalhes_inscricao()
            elif escolha == '7':
                self.crud_inscricoes.cancelar_inscricao()
                
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
                
            else:
                input("Escolha inválida.")
            input("\nPressione Enter para continuar...")
