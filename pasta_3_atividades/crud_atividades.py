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
            self.gerenciador_bd.cursor.execute("SELECT id, nome, data_inicio, data_fim FROM eventos ORDER BY data_inicio")
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
            data_inicio_str = FormatadorData.data_para_str(FormatadorData.iso_para_data(evento[2])) if evento[2] else "N/A"
            print(f"{evento[0]} - {evento[1]} ({data_inicio_str})")

        while True:
            try:
                id_evento = int(input("\nDigite o ID do evento para esta atividade: "))
                evento_selecionado = next((e for e in eventos if e[0] == id_evento), None)
                if evento_selecionado:
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

        data_evento_inicio = FormatadorData.iso_para_data(evento_selecionado[2]) if evento_selecionado[2] else None
        data_evento_fim = FormatadorData.iso_para_data(evento_selecionado[3]) if evento_selecionado[3] else None

        print(f"\nO evento ocorre de {FormatadorData.data_para_str(data_evento_inicio)} até {FormatadorData.data_para_str(data_evento_fim)}")
        
        while True:
            data_inicio = FormatadorData.solicitar_data_usuario(
                "Digite a data de início da atividade"
            )
            if data_evento_inicio and data_evento_fim:
                if data_evento_inicio <= data_inicio <= data_evento_fim:
                    break
                else:
                    print(f"⚠️  A data da atividade deve estar entre {FormatadorData.data_para_str(data_evento_inicio)} e {FormatadorData.data_para_str(data_evento_fim)}")
            else:
                break

        hora_inicio = FormatadorData.solicitar_hora_usuario(
            "Digite a hora de início da atividade"
        )

        while True:
            data_fim = FormatadorData.solicitar_data_usuario(
                f"Digite a data de fim da atividade (padrão: {FormatadorData.data_para_str(data_inicio)})",
                permitir_vazio=True
            )
            if not data_fim:
                data_fim = data_inicio
            
            if data_evento_inicio and data_evento_fim:
                if data_evento_inicio <= data_fim <= data_evento_fim:
                    break
                else:
                    print(f"⚠️  A data da atividade deve estar entre {FormatadorData.data_para_str(data_evento_inicio)} e {FormatadorData.data_para_str(data_evento_fim)}")
            else:
                break

        while True:
            hora_fim = FormatadorData.solicitar_hora_usuario(
                "Digite a hora de fim da atividade",
                permitir_vazio=True
            )
            if not hora_fim:
                from datetime import datetime, timedelta
                hora_inicio_dt = datetime.strptime(FormatadorData.hora_para_str(hora_inicio), "%H:%M")
                hora_fim_dt = hora_inicio_dt + timedelta(hours=1)
                hora_fim = hora_fim_dt.time()
                print(f"Usando horário padrão: {FormatadorData.hora_para_str(hora_fim)}")
            
            if data_inicio == data_fim and hora_fim <= hora_inicio:
                print("⚠️  A hora de fim deve ser posterior à hora de início.")
                continue
            break

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
            data_inicio=data_inicio,
            hora_inicio=hora_inicio,
            data_fim=data_fim,
            hora_fim=hora_fim,
            vagas=vagas,
        )
        
        resultado = self.crud_atividade.criar_atividade(atividade)
        if resultado:
            print("✅ Atividade criada com sucesso!")
            print(f"📅 Período: {atividade.periodo_formatado()}")
            return True
        else:
            print("❌ Erro ao criar atividade.")
            return False

    def ver_todas_atividades(self):
        print("\n===== TODAS AS ATIVIDADES =====")
        atividades = self.crud_atividade.ler_atividades_com_evento()
        if not atividades:
            print("⚠️  Nenhuma atividade encontrada.")
            return []
        else:
            for atividade in atividades:
                evento_info = f" (Evento: {atividade.evento_nome})" if hasattr(atividade, 'evento_nome') else ""
                print(f"{atividade}{evento_info}")
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
            print(f"Período: {atividade.periodo_formatado()}")
            print(f"Vagas: {atividade.vagas if atividade.vagas > 0 else 'Ilimitado'}")
            if atividade.duracao:
                print(f"Duração: {atividade.duracao:.1f} horas")
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
                    data_inicio_str = FormatadorData.data_para_str(FormatadorData.iso_para_data(evento[2])) if evento[2] else "N/A"
                    print(f"{evento[0]} - {evento[1]} ({data_inicio_str})")
                
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

        alterar_periodo = input(f"Alterar período atual ({atividade.periodo_formatado()})? (s/n): ").lower()
        if alterar_periodo == 's':
            nova_data_inicio = FormatadorData.solicitar_data_usuario(
                f"Nova data de início [{atividade.data_inicio_formatada()}]",
                permitir_vazio=True
            )
            if nova_data_inicio:
                atividade.data_inicio = nova_data_inicio
            
            nova_hora_inicio = FormatadorData.solicitar_hora_usuario(
                f"Nova hora de início [{atividade.hora_inicio_formatada()}]",
                permitir_vazio=True
            )
            if nova_hora_inicio:
                atividade.hora_inicio = nova_hora_inicio
            
            nova_data_fim = FormatadorData.solicitar_data_usuario(
                f"Nova data de fim [{atividade.data_fim_formatada()}]",
                permitir_vazio=True
            )
            if nova_data_fim:
                atividade.data_fim = nova_data_fim
            
            nova_hora_fim = FormatadorData.solicitar_hora_usuario(
                f"Nova hora de fim [{atividade.hora_fim_formatada()}]",
                permitir_vazio=True
            )
            if nova_hora_fim:
                atividade.hora_fim = nova_hora_fim

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
        print(f"Período: {atividade.periodo_formatado()}")
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

    def ver_atividades_por_evento(self, id_evento=None):
        print("\n===== ATIVIDADES POR EVENTO =====")
        
        if id_evento is None:
            eventos = self.listar_eventos_disponiveis()
            if not eventos:
                print("⚠️  Nenhum evento encontrado.")
                return []
            
            print("\nEventos disponíveis:")
            for evento in eventos:
                data_inicio_str = FormatadorData.data_para_str(FormatadorData.iso_para_data(evento[2])) if evento[2] else "N/A"
                print(f"{evento[0]} - {evento[1]} ({data_inicio_str})")
            
            while True:
                try:
                    id_evento = int(input("\nDigite o ID do evento: "))
                    if any(evento[0] == id_evento for evento in eventos):
                        break
                    else:
                        print("⚠️  ID de evento inválido.")
                except ValueError:
                    print("⚠️  Digite um número válido.")
        
        atividades = self.crud_atividade.ler_atividades_por_evento(id_evento)
        if not atividades:
            print(f"⚠️  Nenhuma atividade encontrada para o evento ID {id_evento}.")
            return []
        else:
            print(f"\n📋 Atividades do evento ID {id_evento}:")
            print("=" * 70)
            for atividade in atividades:
                print(atividade)
                print("-" * 70)
            print(f"\nTotal: {len(atividades)} atividade(s)")
            return atividades
