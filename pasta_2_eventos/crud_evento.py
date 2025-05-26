from datetime import datetime, date, time
from compartilhado.formatador_data import FormatadorData
from .evento import Evento
from .crud_bd_eventos import CrudBDEventos

class CrudEvento:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crudBd = CrudBDEventos(gerenciador_bd)

    def criar_evento(self):
        print("\n===== ADICIONAR UM NOVO EVENTO =====")

        nome_evento = input("Informe Nome do Evento: ").strip()
        descricao_evento = input("\nDescreva o Evento que será realizado: ").strip()

        # Usar FormatadorData para obter data de início com validação
        data_inicio = FormatadorData.solicitar_data_usuario(
            "Informe a DATA de INICIO do evento", 
            validar_futura=True
        )
        
        # Usar FormatadorData para obter hora de início
        hora_inicio = FormatadorData.solicitar_hora_usuario(
            "Informe a HORA de INÍCIO do evento"
        )

        # Usar FormatadorData para obter data de fim com validação
        while True:
            data_fim = FormatadorData.solicitar_data_usuario(
                f"Informe a DATA de FIM do evento {nome_evento}"
            )
            
            if FormatadorData.validar_data_fim_posterior(data_inicio, data_fim):
                break
            except ValueError:
                print("⚠️  Hora inválida. Use o formato hh:mm.")

        while True:    
            data_fim_str = input(f"\nInforme a DATA de FIM do evento {nome_evento} (dd/mm/aaaa): ")
            try:           
                data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y").date()
                if data_fim < data_inicio:
                    print("⚠️  A data fim não pode ser antes da data de início.")
                else:
                    break
            except ValueError:
                print("⚠️  Data inválida. Use o formato dd/mm/aaaa.")

        while True:
            hora_fim_str = input("\nInforme a HORA de FIM do evento (hh:mm): ")
            try:
                hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()
                if hora_fim< hora_inicio:
                    print("⚠️  A hora final não pode ser anterior à hora de início do evento.")
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

        while True:        
            tipo_evento = input("Informe se o evento será Presencial OU Online: ").strip().lower()
            if tipo_evento == "online":
                print("Evento do tipo Online")
                endereco = "Online"
                capacidadeMax = None
                break
            elif tipo_evento == "presencial":
                print("Evento do tipo Presencial")
                endereco = input("\nInforme o endereço do evento:(Rua - numero - complemento - bairro/estado -) ").strip()
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
            tipo=tipo_evento,
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
            for evento in eventos:
                print(evento)
                print("-" * 50)
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
                print("\n" + "=" * 50)
                print(f"📌 Detalhes do Evento (ID: {evento.id})")
                print(evento)
                print("=" * 50)
                
                # Mostrar duração se disponível
                if evento.duracao:
                    print(f"Duração: {evento.duracao:.1f} horas")
                    print("=" * 50)
            else:
                print("⚠️  Evento não encontrado.")
        except ValueError:
            print("⚠️  ID inválido. Digite um número.")

    def buscar_evento(self, termo=None):
        print("\n===== BUSCAR EVENTOS =====")
        
        if termo is None:
            termo = input("Digite um termo para buscar (nome, descrição, tipo ou endereço): ").strip()
        if not termo:
            print("⚠️  Digite um termo válido")
            return

        eventos = self.crudBd.buscar_eventos(termo)

        if eventos:
            print(f"\n{len(eventos)} resultado(s) encontrado(s) para '{termo}':")
            for evento in eventos:
                print("\n" + "=" * 30)
                print(evento)
                print("=" * 30)
        else:
            print("⚠️  Nenhum evento encontrado.")

    def buscar_eventos_por_data(self):
        print("\n===== BUSCAR EVENTOS POR DATA =====")
        
        # Usar FormatadorData para obter datas de busca
        data_inicio = FormatadorData.solicitar_data_usuario(
            "Data início da busca [Enter para pular]", 
            permitir_vazio=True
        )
        
        data_fim = FormatadorData.solicitar_data_usuario(
            "Data fim da busca [Enter para pular]", 
            permitir_vazio=True
        )
        
        eventos = self.crudBd.buscar_eventos_por_data(data_inicio, data_fim)
        
        if eventos:
            periodo_str = ""
            if data_inicio and data_fim:
                periodo_str = f" de {FormatadorData.data_para_str(data_inicio)} a {FormatadorData.data_para_str(data_fim)}"
            elif data_inicio:
                periodo_str = f" a partir de {FormatadorData.data_para_str(data_inicio)}"
            elif data_fim:
                periodo_str = f" até {FormatadorData.data_para_str(data_fim)}"
                
            print(f"\n{len(eventos)} evento(s) encontrado(s){periodo_str}:")
            for evento in eventos:
                print("\n" + "=" * 30)
                print(evento)
                print("=" * 30)
        else:
            print("⚠️  Nenhum evento encontrado no período especificado.")

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

        # Nome
        novo_nome = input(f"Nome (atual: {evento.nome}): ").strip()
        if novo_nome:
            evento.nome = novo_nome

        # Descrição
        nova_descricao = input(f"Descrição (atual: {evento.descricao}): ").strip()
        if nova_descricao:
            evento.descricao = nova_descricao

        # Data início usando FormatadorData
        data_atual_str = FormatadorData.data_para_str(evento.data_inicio)
        nova_data_inicio = FormatadorData.solicitar_data_usuario(
            f"Data início (atual: {data_atual_str})", 
            permitir_vazio=True
        )
        if nova_data_inicio:
            evento.data_inicio = nova_data_inicio

        # Hora início usando FormatadorData
        hora_atual_str = FormatadorData.hora_para_str(evento.hora_inicio)
        nova_hora_inicio = FormatadorData.solicitar_hora_usuario(
            f"Hora início (atual: {hora_atual_str})", 
            permitir_vazio=True
        )
        if nova_hora_inicio:
            evento.hora_inicio = nova_hora_inicio

        # Data fim usando FormatadorData com validação
        while True:
            nova_data_inicio = input(f"Data início (atual: {evento.data_inicio}, formato: dd/mm/aaaa): ").strip()
            if not nova_data_inicio:
                break
            try:
                data_convertida = datetime.strptime(nova_data_inicio, "%d/%m/%Y").date()
                if data_convertida<date.today():
                    print("⚠️  A data não pode ser no passado. Tente novamente")
                else:    
                    evento.data_inicio = data_convertida
                    break
            except ValueError:
                print("⚠️  Data inválida. Use o formato dd/mm/aaaa.")

        # Hora início
        while True:
            nova_hora_inicio = input(f"Hora início (atual: {evento.hora_inicio}, formato: hh:mm): ").strip()
            if not nova_hora_inicio:
                break
            try:
                evento.hora_inicio = datetime.strptime(nova_hora_inicio, "%H:%M").time()
                break
                
            if FormatadorData.validar_data_fim_posterior(evento.data_inicio, nova_data_fim):
                evento.data_fim = nova_data_fim
                break
            else:
                print("⚠️  A data fim não pode ser antes da data de início.")

        # Hora fim usando FormatadorData
        hora_atual_str = FormatadorData.hora_para_str(evento.hora_fim)
        nova_hora_fim = FormatadorData.solicitar_hora_usuario(
            f"Hora fim (atual: {hora_atual_str})", 
            permitir_vazio=True
        )
        if nova_hora_fim:
            evento.hora_fim = nova_hora_fim
            try:
                data_fim_temp = datetime.strptime(nova_data_fim, "%d/%m/%Y").date()
                if data_fim_temp < evento.data_inicio:
                    print("⚠️  A data fim não pode ser antes da data de início.")
                else:
                    evento.data_fim = data_fim_temp
                    break
            except ValueError:
                print("⚠️  Data inválida. Use o formato dd/mm/aaaa.")

        # Hora fim
        while True:
            nova_hora_fim = input(f"Hora fim (atual: {evento.hora_fim}, formato: hh:mm): ").strip()
            if not nova_hora_fim:
                break
            try:
                hora_convertida = datetime.strptime(nova_hora_fim, "%H:%M").time()
                if hora_convertida< evento.hora_inicio:
                    print("⚠️  A hora final não pode ser anterior à hora de início do evento.")
                else:
                    evento.hora_fim = hora_convertida
                    break
            except ValueError:
                print("⚠️  Hora inválida. Use o formato hh:mm.")

        # Público alvo
        while True:
            novo_publico = input(f"Público alvo (atual: {evento.publico_alvo}, opções: adulto/juvenil/infantil): ").strip().lower()
            if not novo_publico:
                break
            if novo_publico in ["adulto", "juvenil", "infantil"]:
                evento.publico_alvo = novo_publico
                break
            else:
                print("⚠️  Opção inválida. Use: adulto, juvenil ou infantil.")

        # Tipo
        while True:
            novo_tipo = input(f"Tipo (atual: {evento.tipo}, opções: presencial/online): ").strip().lower()
            if not novo_tipo:
                break
            if novo_tipo in ["presencial", "online"]:
                evento.tipo = novo_tipo
                break
            else:
                print("⚠️  Opção inválida. Use: presencial ou online.")

        # Endereço
        if evento.tipo =="online":
            evento.endereco = "não se aplica"
            evento.capacidade = "Ilimitado"
        else:
            novo_endereco = input(f"Endereço (atual: {evento.endereco}): ").strip()
            if novo_endereco:
                evento.endereco = novo_endereco

            # Capacidade
            while True:
                nova_capacidade = input(f"Capacidade (atual: {evento.capacidade}): ").strip()
                if not nova_capacidade:
                    break
                try:
                    evento.capacidade = int(nova_capacidade)
                    break
                except ValueError:
                    print("⚠️  Capacidade deve ser um número inteiro.")

        # Salvar alterações
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

    def listar_eventos_por_tipo(self):
        print("\n===== LISTAR EVENTOS POR TIPO =====")
        
        tipo = input("Digite o tipo de evento (presencial/online): ").strip().lower()
        if not tipo:
            print("⚠️  Digite um tipo válido.")
            return
            
        eventos = self.crudBd.buscar_eventos_por_tipo(tipo)
        
        if eventos:
            print(f"\n{len(eventos)} evento(s) do tipo '{tipo}':")
            for evento in eventos:
                print(f"• {evento.nome} - {evento.periodo_formatado()}")
        else:
            print(f"⚠️  Nenhum evento do tipo '{tipo}' encontrado.")
