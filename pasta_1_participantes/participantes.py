participantes = []

def menu():
        print("~"*34)
        print("  CADASTRAMENTO DE PARTICIPANTES")
        print("~"*34)

        print("1 - Criar perfil do participante")
        print("2 - Atualizar Dados do participante")
        print("3 - Listar os participantes")
        print("4 - Excluir perfil")
        print("5 - Lista de eventos")
        print("6 - Retornar ao menu principal")

def atualizar_participante(nome_antigo, novo_nome,novo_email,novo_cpf,novo_telefone):
    for participante in participantes:
        if participante['nome'] == nome_antigo:
            participante['nome'] = novo_nome
            participante['email'] = novo_email
            participante['cpf'] = novo_cpf
            participante['telefone'] = novo_telefone
            print(f"Participante '{nome_antigo}' atualizado com sucesso!")
            return
    print(f"Participante com nome '{nome_antigo}' não encontrado.")

while True: 

    menu()

    resposta = input("Informe qual operação deseja realizar>> ")

    if(resposta == "1"):
        print("CADASTRO DE PERFIL")
        nome_participante = input("Informe seu nome>> ")
        email_participante = input("Informe seu e.mail>> ")
        cpf_participante = input("Informe seu CPF>> ")
        telefone_participante = input("Informe seu número de telefone>> ( (00)00000-0000 )")
            
        participante = {
            "nome":nome_participante,
            "email":email_participante,
            "cpf":cpf_participante,
            "telefone":telefone_participante
        }

        participantes.append(participante)

        print(f"Participante {nome_participante} de CPF {cpf_participante} cadastrado!")
    
    elif(resposta == "2"):
        print("ATUALIZAÇÃO DE PERFIL \n")
        nome_antigo = input("Digite o nome do participante a ser atualizado:")
        novo_nome = input("Informe o novo nome do usuario:")
        novo_email = input("Informe o novo email do usuario:")
        novo_cpf = input("Informe o novo cpf do usuario:")
        novo_telefone = input("Informe o novo telefone do usuario:")
        atualizar_participante(nome_antigo, novo_nome,novo_email,novo_cpf,novo_telefone)
    
    elif(resposta == "3"):
        print("LISTA DE PARTICIPANTES")
        if not participantes:
            print("Nenhum participante cadastrado.")
        else:
            print("\nLista de Participantes:")
            print("-" * 40)
            for participante in participantes:
                print(f"Nome: {participante['nome']}")
                print(f"E-mail: {participante['email']}")
                print(f"CPF: {participante['cpf']}")
                print(f"Telefone: {participante['telefone']}")
                print("-" * 40)

    elif(resposta == "4"):
        print("\nEXCLUIR PERFIL")
        for i, participante in enumerate(participantes):
            print(f"{i+1} - {participante["nome"]}")
        indice_participantes = int(input("\nInforme o número do perfil que deseja excluir >> "))
        while True:
            if 0 < indice_participantes <= len(participantes):
                nome_participante = participantes[indice_participantes - 1]["nome"]
                participantes.pop(indice_participantes - 1)
                print(f"Perfil {indice_participantes} de {nome_participante} excluido!")
                break
            else:
                print("\nResposta inválida, tente novamente.")
                indice_participantes = int(input(print("\nInforme o número do perfil que deseja excluir >> ")))

    elif(resposta == "5"):
        import cadastramentoEvento
        cadastramentoEvento.visualizar_eventos()
    
    elif(resposta == "6"):
        import old.mainOld as mainOld
        mainOld.menu()

    else:
        print("\nRESPOSTA INVALIDA, TENTE NOVAMENTE")
     
               




 
