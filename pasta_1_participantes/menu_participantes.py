import os
from .crud_participantes import CrudParticipantes

class MenuParticipantes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_participantes = CrudParticipantes(gerenciador_bd)
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE PARTICIPANTES =====")
        print("1. Adicionar participante")
        print("2. Ver todos os participantes")
        print("3. Ver detalhes do participante")
        print("4. Atualizar participante")
        print("5. Excluir participante")
        print("6. Buscar participantes")
        print("0. Voltar ao menu principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            self.limpar_tela()
            
            if escolha == '1':
                self.crud_participantes.adicionar_participante()
            elif escolha == '2':
                self.crud_participantes.visualizar_participantes()
            elif escolha == '3':
                self.crud_participantes.detalhes_participante()
            elif escolha == '4':
                self.crud_participantes.atualizar_participante()
            elif escolha == '5':
                self.crud_participantes.excluir_participante()
            elif escolha == '6':
                self.crud_participantes.buscar_participantes()

            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida.")
            input("\nPressione Enter para continuar...")
