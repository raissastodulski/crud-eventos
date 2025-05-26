import os
import sys
from .crud_atividades import CrudAtividades


class MenuAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_atividades = CrudAtividades(gerenciador_bd)

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE ATIVIDADES =====")
        print("1. Adicionar nova atividade")
        print("2. Ver todas as atividades")
        print("3. Ver detalhes da atividade")
        print("4. Atualizar atividade")
        print("5. Excluir atividade")
        print("6. Buscar atividades")
        print("0. Voltar ao menu principal")
        print("======================================")
        return input("Digite sua escolha: ")

    def executar(self):
        while True:
            escolha = self.exibir_menu()

            if escolha == "1":
                self.limpar_tela()
                self.crud_atividades.adicionar_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == "2":
                self.limpar_tela()
                self.crud_atividades.ver_todas_atividades()
                input("\nPressione Enter para continuar...")
            elif escolha == "3":
                self.limpar_tela()
                self.crud_atividades.ver_detalhes_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == "4":
                self.limpar_tela()
                self.crud_atividades.atualizar_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == "5":
                self.limpar_tela()
                self.crud_atividades.excluir_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == "6":
                self.limpar_tela()
                self.crud_atividades.buscar_atividade()
                input("\nPressione Enter para continuar...")
            elif escolha == "0":
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
