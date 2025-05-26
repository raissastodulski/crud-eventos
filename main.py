from compartilhado import GerenciadorBD, MenuPrincipal
import os

def principal():
    # Obter o diretório atual onde está o script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Criar o caminho completo para o banco de dados
    caminho_bd = os.path.join(diretorio_atual, "crud-eventos.db")
    
    print(f"Inicializando aplicação...")
    print(f"Diretório atual: {diretorio_atual}")
    print(f"Caminho do banco: {caminho_bd}")
    
    # Criar o gerenciador de banco de dados
    gerenciador_bd = GerenciadorBD(caminho_bd)
    
    # Verificar se a inicialização foi bem-sucedida
    if gerenciador_bd.conn is None or gerenciador_bd.cursor is None:
        print("❌ Falha na inicialização do banco de dados. Encerrando aplicação.")
        return
    
    # Criar e executar o menu principal
    menu = MenuPrincipal(gerenciador_bd)
    
    try:
        print("🚀 Sistema de Gerenciamento de Eventos iniciado com sucesso!")
        menu.executar()
    except KeyboardInterrupt:
        print("\n⚠️  Aplicação finalizada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Um erro ocorreu: {e}")
        import traceback
        print("Detalhes do erro:")
        traceback.print_exc()
    finally:
        # Garantir que a conexão seja fechada
        if gerenciador_bd:
            gerenciador_bd.fechar()
        print("👋 Aplicação finalizada.")

if __name__ == "__main__":
    principal()