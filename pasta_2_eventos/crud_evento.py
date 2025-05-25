from datetime import datetime, date, time
from .evento import Evento
from .crud_bd_eventos import CrudBDEventos



class CrudEvento:
    def __init__(self,gerenciador_bd):
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
            data_fim_str = input(f"\nInforme a DATA de FIM  do evento {nome_evento} (dd/mm/aaaa)")
            try:           
                data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y").date()
                if data_fim < data_inicio:
                    print("⚠️  A data fim não pode ser antes da data de início.")
                else:
                    break
            except ValueError:
                print("⚠️  Data inválida. Use o formato dd/mm/aaaa.")

        while True:
            hora_fim_str = input("\nInforme a HORA de FIM do evento (hh:mm):")
            try:
                hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()
                break
            except ValueError:
                print("⚠️  Hora inválida. Use o formato hh:mm.")

        while True:
            publico_alvo = input("Qual será o Publico Alvo? (Adulto/Juvenil/Infantil)").strip().lower()
            if publico_alvo in ["adulto","juvenil","infantil"]:
                break
            else:
                print("⚠️  Opção inválida. Informe Adulto, Juvenil ou Infantil.")

        while True:        
            local = input("Informe se o evento será Presencial OU Online: ").strip().lower()
            if(local =="online"):
                print("Evento do tipo Online")
                local_presencial = "Não se Aplica"
                capacidadeMax = None
                break

            elif local == "presencial":
                print("Evento do tipo Presencial")
                local_presencial = input("\nInforme o endereço do evento: \n").strip()
                while True:
                    try:
                        capacidadeMax = int(input("Quantidade maxima de vagas para esse evento? "))
                        break
                    except ValueError:
                        print("⚠️  Informe um número inteiro.")
                break
            
            else:
                print("Tipo de evento inválido. Digite 'presencial' ou 'online'.")
            
            
        evento = Evento(
            nome = nome_evento,
            descricao = descricao_evento,
            data_inicio = data_inicio,
            hora_inicio = hora_inicio,
            data_fim = data_fim,
            hora_fim = hora_fim,
            publico_alvo = publico_alvo,
            tipo = local,
            endereco = local_presencial,
            capacidade = capacidadeMax
        )
        #ajustar aqui
        self.crudBd.criar_evento(evento)

        #testar se vai linkar
        tem_atividades = input("O evento terá atividades? (s/n): ").lower()
        if tem_atividades == 's':
            try:
                from pasta_3_atividades import menu_activity
                menu_activity(evento["id"])
            except ModuleNotFoundError:
                print("⚠️  Módulo de atividades não encontrado. Avise o responsável.")



    def visualizar_eventos(self):
        print("\n===== TODOS OS EVENTOS =====")

        eventos = self.crudBd.ler_todos_eventos(evento)

        if not eventos:
            print("⚠️  Nenhum evento cadastrado até o momento.")
            return
        else:
            for evento in eventos:
                print(evento)
            return eventos



    def ver_detalhe_evento(self):
        print("\n===== DETALHES DO EVENTO =====")
        if not evento:
            print("⚠️  Nenhum evento cadastrado até o momento.")
            return

        
        try:
            id_evento = int(input("\nDigite o ID do evento para ver detalhes: "))
            evento = None
            for i in evento:
                if i.id == id_evento:
                    evento = i
                    break
            evento = self.crudBd.ler_evento_por_id(int(id_evento))
            if evento:
                print("\n" + "=" *30)
                print(f"📌 Detalhes do Evento (ID: {evento.id})")
                print(f"ID: {evento.id}")
                print(f"Título: {evento.titulo}")
                print(f"Descrição: {evento.descricao}")
                print(f"Data: {evento.data}")
                print(f"Local: {evento.local}")
                print("="*30)
            else:
                print("⚠️  Evento não encontrado.")
        except ValueError:
            print("⚠️  ID inválido. Digite um número.")

        


    def buscar_evento(self, termo = None):
        print("\n===== BUSCAR ATIVIDADES =====")
        
        if termo is None:
            termo = input("Digite um termo para buscar(nome, descrição ou local): ").strip()
        if not termo:
            print("⚠️  Digite um termo válido")
            return

        eventos = self.crudBd.buscar_eventos(termo)

        if eventos:
            print(f"\n Resultados para '{len(termo)}':")
            for evento in eventos:
                print("\n" + "=" *30)
                print(evento)
                print("=" * 30)

        else:
            print("⚠️  Nenhum evento encontrado.")

    def excluir_evento(self):
        print("\n===== EXCLUIR EVENTO =====")

        for i, evento in enumerate(eventos):
            print(f"{i+1} - {evento['nome']}")
        while True:
            try:
                ind_evento = int(input("\nDigite o número do evento que deseja excluir:"))
                if 0 < ind_evento <= len(eventos):
                    evento = eventos[ind_evento - 1]['nome']
                    eventos.pop(ind_evento - 1)
                    print(f"Evento excluido com Sucesso!")
                    break
                else:
                    print("\n Opção invalida tente novamente.")
                    evento = int(input("\nQual evento gostaria de excluir?"))
            except ValueError:
                print("\nTente novamente. Qual evento gostaria de excluir?")

    def atualizar_eventos(self):
        
        print("\nAtualizar Evento:")
        for i, evento in enumerate(eventos):
            print(f"{i+1} - {evento['nome']}")

        while True:
            try:
                edit_evento = int(input("\nDiga o número do evento que deseja editar: "))
                if 0 <= edit_evento <= len(eventos):
                    evento = eventos[edit_evento - 1]
                    print(f"\nVamos atualizar o evento:")

                    evento_campos = [
                        "nome", "descricao", "data_inicio", "hora_inicio",
                        "data_fim", "hora_fim", "publico_alvo", "tipo",
                        "endereco", "capacidade"
                    ]
                    
                    for evento_chave in evento_campos:
                        evento_atual = evento.get(evento_chave,"")
                        evento_novo = input(f"{evento_chave.replace('_',' ').capitalize()}(Atual: {evento_atual})")
                    if evento_novo.strip() != "":
                        evento[evento_chave] = evento_novo

                    print("Evento Atualizado!")
                    break
                else:
                    print("Invalido, tente novamente!")
                    return
            except ValueError:
                print("Invalido, Digite um número.")
