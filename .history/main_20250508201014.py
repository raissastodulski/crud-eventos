import re


organizadores = []

def 

while True:

    def isCpfValid(cpf):
    
        if not isinstance(cpf,str):
            return False

        # Remove some unwanted characters
        cpf = re.sub("[^0-9]",'',cpf)
        
        # Verify if CPF number is equal
        if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
            return False

        # Checks if string has 11 characters
        if len(cpf) != 11:
            return False

        sum = 0
        weight = 10

        """ Calculating the first cpf check digit. """
        for n in range(9):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifyingDigit = 11 -  sum % 11

        if verifyingDigit > 9 :
            firstVerifyingDigit = 0
        else:
            firstVerifyingDigit = verifyingDigit

        """ Calculating the second check digit of cpf. """
        sum = 0
        weight = 11
        for n in range(10):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifyingDigit = 11 -  sum % 11

        if verifyingDigit > 9 :
            secondVerifyingDigit = 0
        else:
            secondVerifyingDigit = verifyingDigit

        if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
            return True
        return False
    
    class BuscaEndereco:

        def __init__(self, cep):
            cep = str(cep)
            if self.cep_eh_Valido(cep):
                self.cep = cep
            else:
                raise ValueError("CEP inválido!")

        def cep_eh_Valido(self, cep):
            if len(cep) == 8:
                padrao_cep = re.compile(r'(\d){5}(\d){3}')

                match = padrao_cep.match(cep)

                return True
            else:
                return False    

       
    opcao = int(input("\nDigite a opção desejada: "))
    
    if (opcao == 1):

        while True:     
            print("------MENU ORGANIZADOR-----")
            
            print("1 - Novo Cadastro")
            print("2 - Editar Cadastro")
            print("3 - Excluir Cadastro")
            print("4 - Criar Evento")
            print("5 - Voltar ao menu")
            
            opcao = int(input("\nDigite a opção desejada: "))
            
            if (opcao == 1):
                nome = input("Digite o nome: ")
                telefone = input("Digite o seu telefone (XX) XXXXX-XXXX: ")
                while True:
                    email = input("Digite o email: ")
                    try:
                        valid = re.search(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}$', email)
                        break
                    except ValueError:
                        print("\nEmail inválido! Digite um email válido.")
                
                while True:
                    cpf = input("Digite o cpf 000.000.000-00: ") 
                    try:
                        isCpfValid(cpf)
                        break
                    except ValueError:
                        print("\nCPF inválido! Digite um cpf válido.")
                endereco = input("Digite o seu endereço: ")
                numero = int(input("Digite o número: "))
                complemento = input("Digite o complemento: ")
                bairro = input("Digite o seu bairro: ")
                cidade = input("Digite o sua Cidade: ")
                estado = input("Digite o seu Estado: ")
                while True:
                    cep = input("Digite o seu cep: ")
                    try:
                        objeto_cep = BuscaEndereco(cep)
                        break
                    except ValueError:
                        print("\nCep inválido! Digite o cep válido.")        

                organizador = {
                    "nome":nome,
                    "cpf":cpf,
                    "telefone": telefone,
                    "email":email,
                    "endereço":endereco,
                    "número":numero,
                    "complemento":complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado":estado,
                    "cep":cep
                }

                organizadores.append(organizador)
                print(f"\nA atividade {nome} foi cadastrada com sucesso!\n")

            elif (opcao == 2):
                if organizadores:
                    print("\n--- Editar Organizador ---")
                    for i, organizador in enumerate(organizadores):
                        print(f"{i+1}. Nome: {organizador['nome']}")
                        print(f"   CPF: {organizador['cpf']}")
                        print(f"   Telefone: {organizador['telefone']}")
                        print(f"   E-mail: {organizador['email']}")
                        print(f"   Horário: {organizador['endereço']}")
                        print(f"   Número: {organizador['número']}")
                        print(f"   Complemento: {organizador['complemento']}")
                        print(f"   Bairro: {organizador['bairro']}")
                        print(f"   Cidade: {organizador['cidade']}")
                        print(f"   Estado: {organizador['estado']}")
                        print(f"   Cep: {organizador['cep']}")
                    indice_editar = int(input("Digite o número da atividade que deseja excluir: ")) - 1 
                    if 0 <= indice_editar < len(organizadores):
                        organizador = organizadores[indice_editar]

                        print("\nCampos disponíveis para edição: nome, cpf, telefone, email, número, endereço, complemento, bairro, cidade, estado, cep\n")
                        campo_editar = input("\nDigite o campo que deseja editar: ").lower()

                        if campo_editar in organizador:
                            novo_valor = input(f"Digite o novo valor para {campo_editar}: ")
                        organizador[campo_editar] = novo_valor
                        print(f"\nCampo {campo_editar} atualizado com sucesso!\n")
            elif (opcao == 3):
                if organizadores:
                    print("\n--- Excluir Organizador ---")
                    for i, organizador in enumerate(organizadores):
                        print(f"{i+1}. {organizador['nome']}")
                    indice_excluir = int(input("Digite o número da atividade que deseja excluir: ")) - 1
                    if 0 <= indice_excluir < len(organizadores):
                        organizador_excluido = organizadores.pop(indice_excluir)
                        print(f"A atividade '{organizador_excluido['nome']}' foi excluída com sucesso!")
                    else:
                        print("\nOrganizador não existe")
            elif (opcao == 4):
                import cadastramentoEvento
                cadastramentoEvento.criar_evento()
                print("ola")
            elif (opcao == 5):
                break
            else:
                print("\nOpção inválida! Tente novamento\n")
    elif(opcao ==2 ):
        import participantes
        participantes.menu()
    elif(opcao == 3):
        print("\nPrograma encerrado. Volte sempre!!")
        break
    else:
        print("\nOpção inválida. Tente novamente\n")