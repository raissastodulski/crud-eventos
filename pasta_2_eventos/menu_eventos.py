import os
import sys
from .crud_evento import CrudEvento


class MenuEventos:

    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_evento = CrudEvento(gerenciador_bd)

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')   

    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE EVENTOS =====")
        print("1. Adicionar Evento")
        print("2. Ver Todos os Eventos")
        print("3. Ver Detalhes do Evento")
        print("4. Atualizar Evento")
        print("5. Excluir Evento")
        print("6. Buscar Eventos")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")   
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                self.crud_evento.criar_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '2':
                self.crud_evento.visualizar_eventos()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '3':
                self.crud_evento.ver_detalhe_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '4':
                self.crud_evento.atualizar_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '5':
                self.crud_evento.excluir_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '6':
                self.crud_evento.buscar_evento()
                input("\nPressione Enter para continuar...")
                
                
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
                
            else:
                print("❌ Escolha inválida. Tente novamente.")
                input("Pressione Enter para continuar...")
