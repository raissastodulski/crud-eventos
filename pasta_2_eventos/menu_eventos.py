import os

from pasta_2_eventos import evento
class MenuEventos:

    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd


    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')   

    
    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE EVENTOS =====")
        print("1. Adicionar Evento")
        print("2. Ver Todos os Eventos")
        print("3. Ver Detalhes do Eventos")
        print("4. Atualizar Eventos")
        print("5. Excluir Eventos")
        print("6. Buscar Eventos")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")   
    
    def executar(self):
        
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                print("\nAdicionar Atividade")
                evento.criar_evento()
                input("Pressione Enter para continuar...")
            elif escolha == '2':
                print("\nVer Todas as Atividades")
                evento.visualizar_eventos()
                input("Pressione Enter para continuar...")
            elif escolha == '3':
                print("\nVer Detalhes da Atividade (em desenvolvimento)")
                evento.ver_detalhe_evento()
                input("Pressione Enter para continuar...")
            elif escolha == '4':
                print("\nAtualizar Atividade")
                evento.atualizar_eventos()
                input("Pressione Enter para continuar...")
            elif escolha == '5':
                print("\nExcluir Atividade ")
                evento.excluir_evento()
                input("Pressione Enter para continuar...")
            elif escolha == '6':
                print("\nBuscar Atividades (em desenvolvimento)")
                evento.buscar_evento()
                input("Pressione Enter para continuar...")
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")