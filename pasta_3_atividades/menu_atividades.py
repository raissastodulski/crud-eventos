import os
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
            self.limpar_tela()

            if escolha == "1":
                self.crud_atividades.adicionar_atividade()
            elif escolha == "2":
                self.crud_atividades.ver_todas_atividades()
            elif escolha == "3":
                self.crud_atividades.ver_detalhes_atividade()
            elif escolha == "4":
                self.crud_atividades.atualizar_atividade()
            elif escolha == "5":
                self.crud_atividades.excluir_atividade()
            elif escolha == "6":
                self.crud_atividades.buscar_atividade()

            elif escolha == "0":
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida.")
            input("\nPressione Enter para continuar...")
