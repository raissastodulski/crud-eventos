from datetime import datetime, date, time
from database import DatabaseManager
from pasta_2_eventos import events_object


gerenciador_bd = DatabaseManager()


eventos = []

def criar_evento():

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
        
        
    evento = events_object(
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


    if evento.is_valid():
        gerenciador_bd.create_event("Eventos", evento.to_tuple())
        eventos.append(evento)
        print(f"\n✅ Evento {nome_evento} cadastrado com sucesso!")

    else:
        print("⚠️  Erro: Dados incompletos. Preencha todos os campos obrigatorios.")

    tem_atividades = input("O evento terá atividades? (s/n): ").lower()
    if tem_atividades == 's':
        try:
            from pasta_3_atividades import atividade
            atividade.menu_atividades(evento["id"])
        except ModuleNotFoundError:
            print("⚠️  Módulo de atividades não encontrado. Avise o responsável.")



def visualizar_eventos():
    print("\n>>> Lista de Eventos Cadastrados <<<")

    if not eventos:
        print("⚠️  Nenhum evento cadastrado até o momento.")
        return

    for evento in eventos:
        print("\n--------------------------------")
        print(f"Nome: {evento['nome']}")
        print(f"Descrição: {evento['descricao']}")
        print(f"Início: {evento['data_inicio'].strftime('%d/%m/%Y')} às {evento['hora_inicio'].strftime('%H:%M')}")
        print(f"Fim: {evento['data_fim'].strftime('%d/%m/%Y')} às {evento['hora_fim'].strftime('%H:%M')}")
        print(f"Duração: {evento.duracao:.1f} horas")
        print(f"Público Alvo: {evento['publico_alvo'].capitalize()}")
        print(f"Tipo: {evento['tipo'].capitalize()}")
        print(f"Endereço: {evento['endereco']}")
        if evento['tipo'] == "presencial":
            print(f"Capacidade Máxima: {evento['capacidade']}")
        print("-------------------------------")


def ver_detalhe_evento():
    if not eventos:
        print("⚠️  Nenhum evento cadastrado até o momento.")
        return

    visualizar_eventos()
    try:
        id_evento = int(input("\nDigite o ID do evento para ver detalhes: "))
        evento = None
        for i in eventos:
            if i.id == id_evento:
                evento = i
                break
        if evento:
            print("\n" + "=" *30)
            print(f"📌 Detalhes do Evento (ID: {evento.id})")
            print(evento)
            print("="*30)
        else:
            print("⚠️  Evento não encontrado.")
    except ValueError:
        print("⚠️  ID inválido. Digite um número.")


def buscar_evento():
    termo = input("Digite um termo para buscar(nome, descrição ou local): ").strip()
    if not termo:
        print("⚠️  Digite um termo válido")
        return
    
    resultados = gerenciador_bd.search_events(termo)
    if resultados:
        print(f"\n Resultados para '{termo}':")
        for evento in resultados:
            print("\n" + "=" *30)
            print(evento)
            print("=" * 30)

    else:
        print("⚠️  Nenhum evento encontrado.")
