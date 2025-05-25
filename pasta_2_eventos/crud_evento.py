from datetime import datetime, date, time
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

        while True:
            data_inicio_str = input("\nInforme a DATA de INICIO do evento (dd/mm/aaaa): ")
            try: 
                data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y").date()
                if data_inicio < date.today():
                    print("⚠️  A data não pode estar no passado.")
                else:
                    break
            except ValueError:
                print("⚠️  Data inválida. Use o formato dd/mm/aaaa.")
        
        while True:
            hora_inicio_str = input("\nInforme a HORA de INÍCIO do evento (hh:mm): ")
            try:
                hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
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
                endereco = input("\nInforme o endereço do evento: ").strip()
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

        # Data início
        while True:
            nova_data_inicio = input(f"Data início (atual: {evento.data_inicio}, formato: dd/mm/aaaa): ").strip()
            if not nova_data_inicio:
                break
            try:
                evento.data_inicio = datetime.strptime(nova_data_inicio, "%d/%m/%Y").date()
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
            except ValueError:
                print("⚠️  Hora inválida. Use o formato hh:mm.")

        # Data fim
        while True:
            nova_data_fim = input(f"Data fim (atual: {evento.data_fim}, formato: dd/mm/aaaa): ").strip()
            if not nova_data_fim:
                break
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
                evento.hora_fim = datetime.strptime(nova_hora_fim, "%H:%M").time()
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
        novo_endereco = input(f"Endereço (atual: {evento.endereco}): ").strip()
        if novo_endereco:
            evento.endereco = novo_endereco

        # Capacidade
        while True:
            nova_capacidade = input(f"Capacidade (atual: {evento.capacidade}): ").strip()
            if not nova_capacidade:
                break
            try:
                evento.capacidade = int(nova_capacidade) if nova_capacidade else None
                break
            except ValueError:
                print("⚠️  Capacidade deve ser um número inteiro.")

        # Salvar alterações
        if self.crudBd.atualizar_evento(evento):
            print("✅ Evento atualizado com sucesso!")
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
            print(f"{i+1} - {evento.nome} (ID: {evento.id})")
            
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

