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
        print("0. Voltar ao menu principal")
        print("===================================")
        return input("Digite sua escolha: ")   
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            self.limpar_tela()
            
            if escolha == '1':
                self.crud_evento.criar_evento()
            elif escolha == '2':
                self.crud_evento.visualizar_eventos()
            elif escolha == '3':
                self.crud_evento.ver_detalhe_evento()
            elif escolha == '4':
                self.crud_evento.atualizar_evento()
            elif escolha == '5':
                self.crud_evento.excluir_evento()
            elif escolha == '6':
                self.crud_evento.buscar_evento()
                
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                print("❌ Escolha inválida. Tente novamente.")
            
            input("\nPressione Enter para continuar...")
