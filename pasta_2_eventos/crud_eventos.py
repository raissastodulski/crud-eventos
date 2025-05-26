from datetime import datetime
from utils import FormatadorData, FormatadorTabela
from .evento import Evento
from .crud_bd_eventos import CrudBdEventos

class CrudEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crudBd = CrudBdEventos(gerenciador_bd)

    def criar_evento(self):
        print("\n===== ADICIONAR UM NOVO EVENTO =====")

        nome_evento = input("Informe Nome do Evento: ").strip()
        descricao_evento = input("\nDescreva o Evento que será realizado: ").strip()

        data_inicio = FormatadorData.solicitar_data_usuario(
            "Informe a DATA de INICIO do evento", 
            validar_futura=True
        )
        
        hora_inicio = FormatadorData.solicitar_hora_usuario(
            "Informe a HORA de INÍCIO do evento"
        )

        while True:
            data_fim = FormatadorData.solicitar_data_usuario(
                f"Informe a DATA de FIM do evento {nome_evento}"
            )
            
            if FormatadorData.validar_data_fim_posterior(data_inicio, data_fim):
                break

        while True:
            hora_fim_str = input("\nInforme a HORA de FIM do evento (hh:mm): ")
            try:
                hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()
                if data_inicio == data_fim and hora_fim <= hora_inicio:
                    print("⚠️  A hora final deve ser posterior à hora de início.")
                else:
                    break
            except ValueError:
                print("⚠️  Hora inválida. Use o formato hh:mm.")

        while True:
            publico_alvo = input("Qual será o Público Alvo? (Adulto/Juvenil/Infantil): ").strip().lower()
            if publico_alvo in ["adulto", "juvenil", "infantil"]:
                break
            else:
                print("⚠️  Opção inválida. Informe Adulto, Juvenil ou Infantil.")

        local = input("Informe o LOCAL do evento (ex: Auditório Principal, Sala de Conferências): ").strip()
        
        while True:        
            tipo_evento = input("Informe se o evento será Presencial OU Online: ").strip().lower()
            if tipo_evento == "online":
                print("Evento do tipo Online")
                endereco = "Online"
                capacidadeMax = None
                break
            elif tipo_evento == "presencial":
                print("Evento do tipo Presencial")
                endereco = input("\nInforme o ENDEREÇO completo do evento: (Rua, número, bairro, cidade, estado) ").strip()
                while True:
                    try:
                        capacidadeMax = int(input("Quantidade máxima de vagas para esse evento: "))
                        break
                    except ValueError:
                        print("⚠️  Informe um número inteiro.")
                break
            else:
                print("Tipo de evento inválido. Digite 'presencial' ou 'online'.")
            
        evento = Evento(
            nome=nome_evento,
            descricao=descricao_evento,
            data_inicio=data_inicio,
            hora_inicio=hora_inicio,
            data_fim=data_fim,
            hora_fim=hora_fim,
            publico_alvo=publico_alvo,
            local=local,
            endereco=endereco,
            capacidade=capacidadeMax
        )
        
        evento_id = self.crudBd.criar_evento(evento)
        
        if evento_id:
            print("✅ Evento criado com sucesso!")
            print(f"📅 Período: {evento.periodo_formatado()}")
        else:
            print("❌ Erro ao criar evento.")

    def visualizar_eventos(self):
        print("\n===== TODOS OS EVENTOS =====")

        eventos = self.crudBd.ler_todos_eventos()

        if not eventos:
            print("⚠️  Nenhum evento cadastrado até o momento.")
            return
        else:
            dados_tabela = []
            for evento in eventos:
                dados_tabela.append([
                    evento.id,
                    FormatadorTabela.truncar_texto(evento.nome, 30),
                    FormatadorTabela.truncar_texto(evento.publico_alvo.title(), 12),
                    evento.data_inicio_formatada(),
                    evento.data_fim_formatada(),
                    FormatadorTabela.truncar_texto(evento.local, 25),
                    evento.capacidade if evento.capacidade else "N/A"
                ])
            
            cabecalhos = ["ID", "Nome", "Público", "Data Início", "Data Fim", "Local", "Capacidade"]
            larguras = [4, 30, 12, 12, 12, 25, 10]
            
            tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
            print(tabela)
            print(f"\nTotal: {len(eventos)} evento(s)")
            return eventos

    def ver_detalhe_evento(self):
        print("\n===== DETALHES DO EVENTO =====")
        
        eventos = self.crudBd.ler_todos_eventos()
        if not eventos:
            print("⚠️  Nenhum evento cadastrado até o momento.")
            return

        try:
            id_evento = int(input("\nDigite o ID do evento para ver detalhes: "))
            evento = self.crudBd.ler_evento_por_id(id_evento)
            
            if evento:
                dados_detalhes = {
                    "ID": evento.id,
                    "Nome": evento.nome,
                    "Descrição": evento.descricao,
                    "Data Início": evento.data_inicio_formatada(),
                    "Hora Início": evento.hora_inicio_formatada(),
                    "Data Fim": evento.data_fim_formatada(),
                    "Hora Fim": evento.hora_fim_formatada(),
                    "Público Alvo": evento.publico_alvo.title(),
                    "Local": evento.local,
                    "Endereço": evento.endereco,
                    "Capacidade": evento.capacidade if evento.capacidade else "Não definida"
                }
                
                if evento.duracao:
                    dados_detalhes["Duração"] = f"{evento.duracao:.1f} horas"
                
                tabela_detalhes = FormatadorTabela.criar_tabela_detalhes(
                    f"DETALHES DO EVENTO (ID: {evento.id})",
                    dados_detalhes
                )
                print(tabela_detalhes)
            else:
                print("⚠️  Evento não encontrado.")
        except ValueError:
            print("⚠️  ID inválido. Digite um número.")

    def buscar_evento(self, termo=None):
        print("\n===== BUSCAR EVENTOS =====")
        
        if termo is None:
            termo = input("Digite um termo para buscar (nome, descrição, local ou endereço): ").strip()
        if not termo:
            print("⚠️  Digite um termo válido")
            return

        eventos = self.crudBd.buscar_eventos(termo)

        if eventos:
            print(f"\n🔍 {len(eventos)} resultado(s) encontrado(s) para '{termo}':")
            
            dados_tabela = []
            for evento in eventos:
                dados_tabela.append([
                    evento.id,
                    FormatadorTabela.truncar_texto(evento.nome, 30),
                    FormatadorTabela.truncar_texto(evento.publico_alvo.title(), 12),
                    evento.data_inicio_formatada(),
                    evento.data_fim_formatada(),
                    FormatadorTabela.truncar_texto(evento.local, 25),
                    evento.capacidade if evento.capacidade else "N/A"
                ])
            
            cabecalhos = ["ID", "Nome", "Público", "Data Início", "Data Fim", "Local", "Capacidade"]
            larguras = [4, 30, 12, 12, 12, 25, 10]
            
            tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
            print(tabela)
        else:
            print("⚠️  Nenhum evento encontrado.")

    def atualizar_evento(self):
        print("\n===== ATUALIZAR EVENTO =====")
        
        eventos = self.crudBd.ler_todos_eventos()
        if not eventos:
            print("⚠️  Nenhum evento cadastrado para atualizar.")
            return

        print("\nEventos disponíveis:")
        for i, evento in enumerate(eventos):
            print(f"{i+1} - {evento.nome} (ID: {evento.id})")

        while True:
            try:
                opcao = int(input("\nDigite o número do evento que deseja editar: "))
                if 1 <= opcao <= len(eventos):
                    evento = eventos[opcao - 1]
                    break
                else:
                    print("⚠️  Opção inválida. Tente novamente.")
            except ValueError:
                print("⚠️  Digite um número válido.")

        print(f"\n--- Atualizando evento: {evento.nome} ---")
        print("(Pressione Enter para manter o valor atual)")

        novo_nome = input(f"Nome (atual: {evento.nome}): ").strip()
        if novo_nome:
            evento.nome = novo_nome

        nova_descricao = input(f"Descrição (atual: {evento.descricao}): ").strip()
        if nova_descricao:
            evento.descricao = nova_descricao

        data_atual_str = FormatadorData.data_para_str(evento.data_inicio)
        nova_data_inicio = FormatadorData.solicitar_data_usuario(
            f"Data início (atual: {data_atual_str})", 
            permitir_vazio=True
        )
        if nova_data_inicio:
            evento.data_inicio = nova_data_inicio

        hora_atual_str = FormatadorData.hora_para_str(evento.hora_inicio)
        nova_hora_inicio = FormatadorData.solicitar_hora_usuario(
            f"Hora início (atual: {hora_atual_str})", 
            permitir_vazio=True
        )
        if nova_hora_inicio:
            evento.hora_inicio = nova_hora_inicio

        data_atual_str = FormatadorData.data_para_str(evento.data_fim)
        while True:
            nova_data_fim = FormatadorData.solicitar_data_usuario(
                f"Data fim (atual: {data_atual_str})", 
                permitir_vazio=True
            )
            if not nova_data_fim:
                break
            if FormatadorData.validar_data_fim_posterior(evento.data_inicio, nova_data_fim):
                evento.data_fim = nova_data_fim
                break
            else:
                print("⚠️  A data fim não pode ser antes da data de início.")

        hora_atual_str = FormatadorData.hora_para_str(evento.hora_fim)
        nova_hora_fim = FormatadorData.solicitar_hora_usuario(
            f"Hora fim (atual: {hora_atual_str})", 
            permitir_vazio=True
        )
        if nova_hora_fim:
            evento.hora_fim = nova_hora_fim

        while True:
            novo_publico = input(f"Público alvo (atual: {evento.publico_alvo}, opções: adulto/juvenil/infantil): ").strip().lower()
            if not novo_publico:
                break
            if novo_publico in ["adulto", "juvenil", "infantil"]:
                evento.publico_alvo = novo_publico
                break
            else:
                print("⚠️  Opção inválida. Use: adulto, juvenil ou infantil.")

        novo_local = input(f"Local (atual: {evento.local}): ").strip()
        if novo_local:
            evento.local = novo_local

        novo_endereco = input(f"Endereço (atual: {evento.endereco}): ").strip()
        if novo_endereco:
            evento.endereco = novo_endereco

        while True:
            nova_capacidade = input(f"Capacidade (atual: {evento.capacidade}): ").strip()
            if not nova_capacidade:
                break
            try:
                evento.capacidade = int(nova_capacidade)
                break
            except ValueError:
                print("⚠️  Capacidade deve ser um número inteiro.")

        if self.crudBd.atualizar_evento(evento):
            print("✅ Evento atualizado com sucesso!")
            print(f"📅 Novo período: {evento.periodo_formatado()}")
        else:
            print("❌ Erro ao atualizar evento.")

    def excluir_evento(self):
        print("\n===== EXCLUIR EVENTO =====")

        eventos = self.crudBd.ler_todos_eventos()
        if not eventos:
            print("⚠️  Nenhum evento cadastrado para excluir.")
            return

        print("\nEventos disponíveis:")
        for i, evento in enumerate(eventos):
            print(f"{i+1} - {evento.nome} (ID: {evento.id}) - {evento.data_inicio_formatada()}")
            
        while True:
            try:
                opcao = int(input("\nDigite o número do evento que deseja excluir: "))
                if 1 <= opcao <= len(eventos):
                    evento_selecionado = eventos[opcao - 1]
                    confirmacao = input(f"Tem certeza que deseja excluir o evento '{evento_selecionado.nome}'? (s/n): ").lower()
                    
                    if confirmacao == 's':
                        if self.crudBd.deletar_evento(evento_selecionado.id):
                            print("✅ Evento excluído com sucesso!")
                        else:
                            print("❌ Erro ao excluir evento.")
                    else:
                        print("Operação cancelada.")
                    break
                else:
                    print("⚠️  Opção inválida. Tente novamente.")
            except ValueError:
                print("⚠️  Digite um número válido.")
