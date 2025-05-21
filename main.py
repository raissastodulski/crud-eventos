# Importar do diretório compartilhado
from compartilhado.banco_dados import GerenciadorBD
from compartilhado.menu_principal import MenuPrincipal
import os

def principal():
    """Ponto de entrada principal da aplicação"""
    # Seta o caminho do banco de dados no diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_bd = os.path.join(diretorio_atual, "crud-eventos.db")
    
    # Inicializa o gerenciador de banco de dados
    gerenciador_bd = GerenciadorBD(caminho_bd)
    
    # Inicializa e executa o menu principal
    menu = MenuPrincipal(gerenciador_bd)
    try:
        menu.executar()
    except KeyboardInterrupt:
        print("\nAplicação finalizada pelo usuário.")
    except Exception as e:
        print(f"\nUm erro ocorreu: {e}")
    finally:
        # O fechamento da conexão já ocorre no menu principal
        pass

if __name__ == "__main__":
    principal()
