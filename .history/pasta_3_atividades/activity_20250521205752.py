import datetime
import sqlite3


# Global variable for database connection (will be set by the caller)
gerenciador_bd = None


def menu():
    print("-----MODULO DE ATIVIDADE-----")

    print("\n >>> Menu de Atividade <<<\n")
    print("1 - Criar Atividade")
    print("2 - Visualizar Atividade")
    print("3 - Editar Atividade")
    print("4 - Excluir Atividade")
    print("5 - Encerra o Programa")
    
def criar_atividade():
    nome = input("\nDigite o nome da atividade: ")
    facilitador = input("Digite o nome do responsável da atividade: ")
    horario_str = input("Digite a hora que começa a atividade (hh:mm): ")
    horario = datetime.datetime.strptime(horario_str, "%H:%M").strftime("%H:%M")
    vagas = int(input("Digite a quantidade de vagas: "))
    
    # Get event ID if needed
    id_evento = None
    mostrar_eventos()
    try:
        id_evento = int(input("Digite o ID do evento para esta atividade (ou 0 para nenhum): "))
        if id_evento == 0:
            id_evento = None
    except ValueError:
        print("ID inválido. Atividade será criada sem vínculo com evento.")
        id_evento = None
    
    try:
        if gerenciador_bd and gerenciador_bd.conn:
            cursor = gerenciador_bd.conn.cursor()
            cursor.execute("""
            INSERT INTO atividades (nome, facilitador, hora_inicio, vagas, id_evento)
            VALUES (?, ?, ?, ?, ?)
            """, (nome, facilitador, horario, vagas, id_evento))
            gerenciador_bd.conn.commit()
            print(f"\nA atividade {nome} foi cadastrada com sucesso!\n")
        else:
            print("Erro: Conexão com banco de dados não disponível.")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar atividade: {e}")

# Função auxiliar para mostrar eventos disponíveis
def mostrar_eventos():
    if gerenciador_bd and gerenciador_bd.conn:
        cursor = gerenciador_bd.conn.cursor()
        cursor.execute("SELECT id, titulo FROM eventos")
        eventos = cursor.fetchall()
        if eventos:
            print("\nEventos disponíveis:")
            for evento in eventos:
                print(f"ID: {evento[0]}, Título: {evento[1]}")
            print()
        else:
            print("\nNenhum evento cadastrado.\n")
    else:
        print("Erro: Conexão com banco de dados não disponível.")

def visualizar_atividade():
    try:
        if gerenciador_bd and gerenciador_bd.conn:
            cursor = gerenciador_bd.conn.cursor()
            cursor.execute("""
            SELECT a.id, a.nome, a.facilitador, a.hora_inicio, a.vagas, e.titulo
            FROM atividades a
            LEFT JOIN eventos e ON a.id_evento = e.id
            """)
            atividades = cursor.fetchall()
            
            if atividades:
                print("\n----Atividades Cadastradas----")
                for atividade in atividades:
                    print(f"ID: {atividade[0]}")
                    print(f"Nome: {atividade[1]}")
                    print(f"Responsável: {atividade[2]}")
                    print(f"Horário: {atividade[3]}")
                    print(f"Vagas: {atividade[4]}")
                    if atividade[5]:
                        print(f"Evento: {atividade[5]}")
                    print("-" * 25)
            else:
                print("Nenhuma atividade cadastrada ainda.\n")
        else:
            print("Erro: Conexão com banco de dados não disponível.")
    except sqlite3.Error as e:
        print(f"Erro ao recuperar atividades: {e}")

def editar_atividade():
    try:
        if gerenciador_bd and gerenciador_bd.conn:
            # Mostrar atividades primeiro
            visualizar_atividade()
            
            # Solicitar ID da atividade
            id_atividade = int(input("\nDigite o ID da atividade que deseja editar: "))
            
            # Verificar se a atividade existe
            cursor = gerenciador_bd.conn.cursor()
            cursor.execute("SELECT * FROM atividades WHERE id = ?", (id_atividade,))
            atividade = cursor.fetchone()
            
            if atividade:
                print("\nCampos disponíveis para edição:")
                print("1. Nome")
                print("2. Facilitador")
                print("3. Horário de Início")
                print("4. Vagas")
                print("5. Evento")
                
                opcao = int(input("\nDigite a opção do campo que deseja editar: "))
                
                if opcao == 1:
                    novo_valor = input("Digite o novo nome da atividade: ")
                    cursor.execute("UPDATE atividades SET nome = ? WHERE id = ?", (novo_valor, id_atividade))
                    campo = "nome"
                elif opcao == 2:
                    novo_valor = input("Digite o novo nome do facilitador: ")
                    cursor.execute("UPDATE atividades SET facilitador = ? WHERE id = ?", (novo_valor, id_atividade))
                    campo = "facilitador"
                elif opcao == 3:
                    horario_str = input("Digite o novo horário (hh:mm): ")
                    horario = datetime.datetime.strptime(horario_str, "%H:%M").strftime("%H:%M")
                    cursor.execute("UPDATE atividades SET hora_inicio = ? WHERE id = ?", (horario, id_atividade))
                    campo = "horário"
                elif opcao == 4:
                    vagas = int(input("Digite a nova quantidade de vagas: "))
                    cursor.execute("UPDATE atividades SET vagas = ? WHERE id = ?", (vagas, id_atividade))
                    campo = "vagas"
                elif opcao == 5:
                    # Mostrar eventos disponíveis
                    mostrar_eventos()
                    id_evento = int(input("Digite o ID do novo evento (ou 0 para nenhum): "))
                    if id_evento == 0:
                        id_evento = None
                    cursor.execute("UPDATE atividades SET id_evento = ? WHERE id = ?", (id_evento, id_atividade))
                    campo = "evento"
                else:
                    print("Opção inválida!")
                    return
                
                gerenciador_bd.conn.commit()
                print(f"\nCampo {campo} atualizado com sucesso!\n")
            else:
                print(f"\nAtividade com ID {id_atividade} não encontrada.\n")
        else:
            print("Erro: Conexão com banco de dados não disponível.")
    except ValueError:
        print("Erro: Digite um número válido.")
    except sqlite3.Error as e:
        print(f"Erro ao editar atividade: {e}")

def excluir_atividade():
    try:
        if gerenciador_bd and gerenciador_bd.conn:
            # Mostrar atividades primeiro
            visualizar_atividade()
            
            # Solicitar ID da atividade
            id_atividade = int(input("\nDigite o ID da atividade que deseja excluir: "))
            
            # Verificar se a atividade existe
            cursor = gerenciador_bd.conn.cursor()
            cursor.execute("SELECT nome FROM atividades WHERE id = ?", (id_atividade,))
            atividade = cursor.fetchone()
            
            if atividade:
                confirmacao = input(f"Tem certeza que deseja excluir a atividade '{atividade[0]}'? (S/N): ").upper()
                if confirmacao == 'S':
                    cursor.execute("DELETE FROM atividades WHERE id = ?", (id_atividade,))
                    gerenciador_bd.conn.commit()
                    print(f"\nAtividade '{atividade[0]}' excluída com sucesso!\n")
                else:
                    print("\nOperação cancelada.\n")
            else:
                print(f"\nAtividade com ID {id_atividade} não encontrada.\n")
        else:
            print("Erro: Conexão com banco de dados não disponível.")
    except ValueError:
        print("Erro: Digite um número válido.")
    except sqlite3.Error as e:
        print(f"Erro ao excluir atividade: {e}")

# Only run this when the module is executed directly, not when imported
if __name__ == "__main__":
    while True:
        menu()
        opcao = int(input("\nDigite a opção desejada: "))
        if(opcao == 1):
            criar_atividade()   
        elif(opcao == 2):
            visualizar_atividade()
        elif (opcao == 3):
            editar_atividade()
        elif (opcao == 4 ):
            excluir_atividade()
        elif (opcao == 5):
            import compartilhado.menu_principal as menuPrincipal
            menuPrincipal.executar()
            break
        else:
            print("\nOpção inválida! Digite novamente. \n")