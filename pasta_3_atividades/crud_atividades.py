from .atividade import Atividade
from .crud_bd_atividades import CrudBdAtividades
from compartilhado.formatador_data import FormatadorData
from compartilhado.gerenciador_bd import GerenciadorBD


class CrudAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_atividade = CrudBdAtividades(gerenciador_bd)

    def listar_eventos_disponiveis(self):
        try:
            self.gerenciador_bd.cursor.execute("SELECT id, nome FROM eventos ORDER BY data_inicio")
            eventos = self.gerenciador_bd.cursor.fetchall()
            return eventos
        except Exception as e:
            print(f"Erro ao listar eventos: {e}")
            return []

    def adicionar_atividade(self):
        print("\n===== ADICIONAR UMA NOVA ATIVIDADE =====")

        eventos = self.listar_eventos_disponiveis()
        if not eventos:
            print("⚠️  Nenhum evento cadastrado. Cadastre um evento primeiro.")
            return False

        print("\nEventos disponíveis:")
        for evento in eventos:
            print(f"{evento[0]} - {evento[1]}")

        while True:
            try:
                id_evento = int(input("\nDigite o ID do evento para esta atividade: "))
                if any(evento[0] == id_evento for evento in eventos):
                    break
                else:
                    print("⚠️  ID de evento inválido. Tente novamente.")
            except ValueError:
                print("⚠️  Digite um número válido.")

        nome = input("\nDigite o nome da atividade: ").strip()
        if not nome:
            print("⚠️  Nome da atividade é obrigatório.")
            return False

        facilitador = input("Digite o nome do facilitador/responsável: ").strip()
        if not facilitador:
            print("⚠️  Nome do facilitador é obrigatório.")
            return False

        local = input("Digite o local da atividade: ").strip()
        if not local:
            print("⚠️  Local da atividade é obrigatório.")
            return False

        hora_inicio = FormatadorData.solicitar_hora_usuario(
            "Digite a hora de início da atividade"
        )

        while True:
            try:
                vagas = int(input("Digite a quantidade de vagas (0 para ilimitado): "))
                if vagas < 0:
                    print("⚠️  Número de vagas não pode ser negativo.")
                    continue
                break
            except ValueError:
                print("⚠️  Digite um número válido.")

        atividade = Atividade(
            nome=nome,
            facilitador=facilitador,
            local=local,
            id_evento=id_evento,
            hora_inicio=hora_inicio,
            vagas=vagas,
        )
        
        resultado = self.crud_atividade.criar_atividade(atividade)
        if resultado:
            print("✅ Atividade criada com sucesso!")
            return True
        else:
            print("❌ Erro ao criar atividade.")
            return False

    def ver_todas_atividades(self):
        print("\n===== TODAS AS ATIVIDADES =====")
        atividades = self.crud_atividade.ler_todas_atividades()
        if not atividades:
            print("⚠️  Nenhuma atividade encontrada.")
            return []
        else:
            for atividade in atividades:
                print(atividade)
                print("-" * 60)
            print(f"\nTotal: {len(atividades)} atividade(s)")
            return atividades

    def ver_detalhes_atividade(self, id_atividade=None):
        print("\n===== DETALHES DA ATIVIDADE =====")
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade: ")
            if not id_atividade.isdigit():
                print("⚠️  ID inválido. Por favor, digite um número.")
                return None
            id_atividade = int(id_atividade)

        atividade = self.crud_atividade.ler_atividade_por_id(id_atividade)
        if atividade:
            print(f"\n📋 Detalhes da Atividade (ID: {atividade.id})")
            print("=" * 50)
            print(f"Nome: {atividade.nome}")
            print(f"Facilitador: {atividade.facilitador}")
            print(f"Local: {atividade.local}")
            print(f"ID do Evento: {atividade.id_evento}")
            print(f"Horário: {atividade.hora_inicio_formatada()}")
            print(f"Vagas: {atividade.vagas if atividade.vagas > 0 else 'Ilimitado'}")
            print("=" * 50)
            
            try:
                self.gerenciador_bd.cursor.execute(
                    "SELECT nome FROM eventos WHERE id=?", (atividade.id_evento,)
                )
                evento_nome = self.gerenciador_bd.cursor.fetchone()
                if evento_nome:
                    print(f"Evento relacionado: {evento_nome[0]}")
            except Exception as e:
                print(f"Erro ao buscar evento relacionado: {e}")
            return atividade
        else:
            print(f"⚠️  Nenhuma atividade encontrada com ID {id_atividade}")
            return None

    def atualizar_atividade(self, id_atividade=None):
        print("\n===== ATUALIZAR ATIVIDADE =====")
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade para atualizar: ")
            if not id_atividade.isdigit():
                print("⚠️  ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)

        atividade = self.crud_atividade.ler_atividade_por_id(id_atividade)
        if not atividade:
            print(f"⚠️  Nenhuma atividade encontrada com ID {id_atividade}")
            return False

        print(f"\n--- Atualizando atividade: {atividade.nome} ---")
        print("(Pressione Enter para manter o valor atual)")

        novo_nome = input(f"Novo nome [{atividade.nome}]: ").strip()
        if novo_nome:
            atividade.nome = novo_nome

        novo_facilitador = input(f"Novo facilitador [{atividade.facilitador}]: ").strip()
        if novo_facilitador:
            atividade.facilitador = novo_facilitador

        novo_local = input(f"Novo local [{atividade.local}]: ").strip()
        if novo_local:
            atividade.local = novo_local

        alterar_evento = input(f"Alterar evento atual (ID: {atividade.id_evento})? (s/n): ").lower()
        if alterar_evento == 's':
            eventos = self.listar_eventos_disponiveis()
            if eventos:
                print("\nEventos disponíveis:")
                for evento in eventos:
                    print(f"{evento[0]} - {evento[1]}")
                
                while True:
                    try:
                        novo_id_evento = int(input(f"Novo ID do evento [{atividade.id_evento}]: "))
                        if any(evento[0] == novo_id_evento for evento in eventos):
                            atividade.id_evento = novo_id_evento
                            break
                        else:
                            print("⚠️  ID de evento inválido.")
                    except ValueError:
                        print("⚠️  Digite um número válido.")

        alterar_horario = input(f"Alterar horário atual ({atividade.hora_inicio_formatada()})? (s/n): ").lower()
        if alterar_horario == 's':
            nova_hora = FormatadorData.solicitar_hora_usuario(
                f"Nova hora de início [{atividade.hora_inicio_formatada()}]",
                permitir_vazio=True
            )
            if nova_hora:
                atividade.hora_inicio = nova_hora

        while True:
            nova_vagas = input(f"Novas vagas [{atividade.vagas}]: ").strip()
            if not nova_vagas:
                break
            try:
                vagas_int = int(nova_vagas)
                if vagas_int < 0:
                    print("⚠️  Número de vagas não pode ser negativo.")
                    continue
                atividade.vagas = vagas_int
                break
            except ValueError:
                print("⚠️  Digite um número válido.")

        sucesso = self.crud_atividade.atualizar_atividade(atividade)
        if sucesso:
            print("✅ Atividade atualizada com sucesso!")
            return True
        else:
            print("❌ Falha ao atualizar a atividade.")
            return False

    def excluir_atividade(self, id_atividade=None):
        print("\n===== EXCLUIR ATIVIDADE =====")
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade para excluir: ")
            if not id_atividade.isdigit():
                print("⚠️  ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)

        atividade = self.crud_atividade.ler_atividade_por_id(id_atividade)
        if not atividade:
            print(f"⚠️  Nenhuma atividade encontrada com ID {id_atividade}")
            return False

        print("\nAtividade a ser excluída:")
        print("=" * 40)
        print(f"ID: {atividade.id}")
        print(f"Nome: {atividade.nome}")
        print(f"Facilitador: {atividade.facilitador}")
        print(f"Local: {atividade.local}")
        print(f"Horário: {atividade.hora_inicio_formatada()}")
        print(f"Vagas: {atividade.vagas}")
        print("=" * 40)

        confirmar = input("\nTem certeza de que deseja excluir esta atividade? (s/n): ")
        if confirmar.lower() == "s":
            sucesso = self.crud_atividade.deletar_atividade(id_atividade)
            if sucesso:
                print("✅ Atividade excluída com sucesso!")
                return True
            else:
                print("❌ Falha ao excluir a atividade.")
                return False
        else:
            print("❌ Exclusão cancelada.")
            return False

    def buscar_atividade(self, termo_busca=None):
        print("\n===== BUSCAR ATIVIDADES =====")
        if termo_busca is None:
            termo_busca = input("Digite o termo de busca (nome, facilitador ou local): ").strip()

        if not termo_busca:
            print("⚠️  O termo de busca não pode estar vazio.")
            return []

        atividades = self.crud_atividade.buscar_atividades(termo_busca)
        if not atividades:
            print(f"⚠️  Nenhuma atividade encontrada correspondente a '{termo_busca}'.")
            return []
        else:
            print(f"\n🔍 Encontradas {len(atividades)} atividade(s) correspondente(s) a '{termo_busca}':")
            print("=" * 70)
            for atividade in atividades:
                print(atividade)
                print("-" * 70)
            return atividades
