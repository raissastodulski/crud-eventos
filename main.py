from compartilhado import GerenciadorBD, MenuPrincipal
import os
def principal():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_bd = os.path.join(diretorio_atual, "crud-eventos.db")
    gerenciador_bd = GerenciadorBD(caminho_bd)
    menu = MenuPrincipal(gerenciador_bd)
    try:
        menu.executar()
    except KeyboardInterrupt:
        print("\nAplicação finalizada pelo usuário.")
    except Exception as e:
        print(f"\nUm erro ocorreu: {e}")
    finally:
        pass
if __name__ == "__main__":
    principal()
