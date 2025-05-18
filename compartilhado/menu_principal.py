from .banco_dados import GerenciadorBD
from pasta_0_modelos.menu_eventos import MenuEventos
from pasta_1_participantes.menu_participantes import MenuParticipantes
from pasta_3_atividades.menu_atividades import MenuAtividades
from pasta_4_inscricoes.menu_inscricoes import MenuInscricoes
import os

class MenuPrincipal:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        # Inicializar os submenus
        self.menu_eventos = MenuEventos(gerenciador_bd)
        self.menu_participantes = MenuParticipantes(gerenciador_bd)
        self.menu_atividades = MenuAtividades(gerenciador_bd)
        self.menu_inscricoes = MenuInscricoes(gerenciador_bd)
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu principal"""
        self.limpar_tela()
        print("\n===== SISTEMA DE GERENCIAMENTO =====")
        print("1. Gerenciamento de Eventos")
        print("2. Gerenciamento de Participantes")
        print("3. Gerenciamento de Atividades")
        print("4. Gerenciamento de Inscrições")
        print("0. Sair")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa o menu principal"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                # Submenu de Eventos
                self.menu_eventos.executar()
            elif escolha == '2':
                # Submenu de Participantes
                self.menu_participantes.executar()
            elif escolha == '3':
                # Submenu de Atividades
                self.menu_atividades.executar()
            elif escolha == '4':
                # Submenu de Inscrições
                self.menu_inscricoes.executar()
            elif escolha == '0':
                print("Saindo da aplicação. Até mais!")
                self.gerenciador_bd.fechar()
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")