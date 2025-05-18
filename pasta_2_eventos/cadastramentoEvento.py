from datetime import datetime, date, time

print("---MODULO EVENTOS---")

def menu():
    print("\n>>>Menu Eventos<<<\n")
    print("------------------------")
    print("1 - Criar Evento")
    print("2 - Visualizar Evento")
    print("3 - Editar Evento")
    print("4 - Excluir Evento")
    print("------------------------")


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
        
        
    evento = {
        "nome":nome_evento,
        "descricao":descricao_evento,
        "data_inicio":data_inicio,
        "hora_inicio":hora_inicio,
        "data_fim":data_fim,
        "hora_fim":hora_fim,
        "publico_alvo":publico_alvo,
        "tipo":local,
        "endereco":local_presencial,
        "capacidade":capacidadeMax
    }
        
    eventos.append(evento)
    print(f"\n✅ Evento {nome_evento} cadastrado com sucesso!")
    print(f"Data Inicio: {data_inicio.strftime('%d/%m/%Y')} às {hora_inicio}")
    print(f"Data de fim: {data_fim.strftime('%d/%m/%Y')} às {hora_fim}")

    tem_atividades = input("O evento terá atividades? (s/n): ").lower()
    if tem_atividades == 's':
        try:
            import atividade
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
        print(f"Público Alvo: {evento['publico_alvo'].capitalize()}")
        print(f"Tipo: {evento['tipo'].capitalize()}")
        print(f"Endereço: {evento['endereco']}")
        if evento['tipo'] == "presencial":
            print(f"Capacidade Máxima: {evento['capacidade']}")
        print("-------------------------------")




while True:
    menu()

    try:
        escolha = int(input("Escolha um serviço: "))
    except ValueError:
        print("Opção inválida.")
        continue
    
    if escolha == 1:
        criar_evento()

    elif escolha == 2:
        visualizar_eventos()

    elif escolha == 3:
        print("Editar eventos (em construção)")

    elif escolha == 4:
        print("Excluir evento(em construção)")

    else:
        print("Opção inválida.")
    
    repetir = input("\nDeseja continuar no menu?(s/n): ").strip().lower()
    if repetir != 's':
        print("Saindo do Módulo de eventos.")
        break

