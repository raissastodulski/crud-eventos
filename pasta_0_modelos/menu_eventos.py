import os
from .crud_eventos import CrudEventos

class MenuEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_eventos = CrudEventos(gerenciador_bd)
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de eventos"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE EVENTOS =====")
        print("1. Adicionar Novo Evento")
        print("2. Ver Todos os Eventos")
        print("3. Ver Detalhes do Evento")
        print("4. Atualizar Evento")
        print("5. Excluir Evento")
        print("6. Buscar Eventos")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa a interface do menu"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                self.limpar_tela()
                self.crud_eventos.adicionar_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '2':
                self.limpar_tela()
                self.crud_eventos.ver_todos_eventos()
                input("\nPressione Enter para continuar...")
            elif escolha == '3':
                self.limpar_tela()
                self.crud_eventos.ver_detalhes_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '4':
                self.limpar_tela()
                self.crud_eventos.atualizar_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '5':
                self.limpar_tela()
                self.crud_eventos.excluir_evento()
                input("\nPressione Enter para continuar...")
            elif escolha == '6':
                self.limpar_tela()
                self.crud_eventos.buscar_eventos()
                input("\nPressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")