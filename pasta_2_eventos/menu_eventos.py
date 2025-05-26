import os
from .crud_eventos import CrudEventos


class MenuEventos:

    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_evento = CrudEventos(gerenciador_bd)

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')   

    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE EVENTOS =====")
        print("1. Adicionar evento")
        print("2. Listar eventos")
        print("3. Ver detalhes do evento")
        print("4. Atualizar evento")
        print("5. Excluir evento")
        print("6. Buscar eventos")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")   
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                print("\n--- Adicionar Evento ---")
                self.crud_evento.criar_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '2':
                print("\n--- Ver Todos os Eventos ---")
                self.crud_evento.visualizar_eventos()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '3':
                print("\n--- Ver Detalhes do Evento ---")
                self.crud_evento.ver_detalhe_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '4':
                print("\n--- Atualizar Evento ---")
                self.crud_evento.atualizar_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '5':
                print("\n--- Excluir Evento ---")
                self.crud_evento.excluir_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '6':
                print("\n--- Buscar Eventos ---")
                self.crud_evento.buscar_evento()
                input("\nPressione Enter para continuar...")
                
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
                
            else:
                print("❌ Escolha inválida. Tente novamente.")
                input("Pressione Enter para continuar...")
