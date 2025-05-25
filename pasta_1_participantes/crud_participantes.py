from .participante import Participante
from .crud_bd_participantes import CrudBDParticipantes
import datetime


class CrudParticipantes:
    @staticmethod
    def validar_cpf( cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
     
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        return digito1 == int(cpf[9]) and digito2 == int(cpf[10])


    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_participantes = CrudBDParticipantes(gerenciador_bd)
    
    def adicionar_participante(self):
        """Adiciona um novo participante"""
        print("\n===== ADICIONAR NOVO PARTICIPANTE =====")
        
        nome = input("Digite o nome do participante: ")
        cpf = input("Digite o CPF do participante: ")
        email = input("Digite o email do participante: ")
        telefone = input("Digite o telefone do participante: ")
        data = input("Digite a data de nascimento (AAAA-MM-DD) ou deixe em branco: ")
        
        participante = Participante(nome=nome, cpf=cpf, email=email, telefone=telefone, data=data)
        self.crud_bd_participantes.criar_participante(participante)
        
        return True
    
    def visualizar_participantes(self):
        print("\n==== LISTAR PARTICIPANTES ====")
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        if participantes:
            for participante in participantes:
                print(participante)
        else:
            print("Não há participantes")
    
    def detalhes_participante(self, idParticipante=None):
        print("\n==== DETALHES PARTICIPANTES ====")
        if idParticipante is None:
            idParticipante = input("Digite o ID do participante: ")
            if not idParticipante.isdigit():
                print("ID inválido, digite um ID válido, por favor")
                return None
        idParticipante = int(idParticipante)
        participante = self.crud_bd_participantes.ler_participante_por_id(idParticipante)

        if participante:
            print("\nDetalhes do Participante:")
            print(f"ID: {participante.id}")
            print(f"Nome: {participante.nome}")
            print(f"CPF: {participante.cpf}")
            print(f"Telefone: {participante.telefone}")
            print(f"Email: {participante.email}")
            print(f"Data de Nascimento: {participante.data}")
            return participante
        else:
            print("Participante com essa ID não encontrada, tente novamente")
            return None
        
    def atualizar_participante(self, idParticipante=None,):
        print("\n==== ATUALIZAR PARTICIPANTES ====")
        if idParticipante is None:
            idParticipante = input("Digite o ID do participante: ")
            if not idParticipante.isdigit():
                print("ID inválido, tente novamente")
                return None
            idParticipante = int(idParticipante)
        
        participante = self.crud_bd_participantes.ler_participante_por_id(idParticipante)

        if not participante:
            print(f"Nenhum participante encontrado com {idParticipante}")
            return False
        print("\nInformações do Participante:")
        print(f"ID: {participante.id}")
        print(f"Nome: {participante.nome}")
        print(f"CPF: {participante.cpf}")
        print(f"Telefone: {participante.telefone}")
        print(f"Email: {participante.email}")
        print(f"Data de Nascimento: {participante.data}")

        print("\nDigite os novos detalhes (deixe em branco par amanter o valor atual):")
        novo_nome = input(f"Nome a atualizar[{participante.nome}]: ")
        if novo_nome:
            participante.nome = novo_nome        
        while True:
            novo_cpf = input(f"CPF a atualizar [{participante.cpf}]: ")
            if not novo_cpf:
                break 
            if CrudParticipantes.validar_cpf(novo_cpf):
                participante.cpf = novo_cpf
                break
            else:
                print("CPF inválido. Tente novamente.")
        novo_email = input(f"Email a atualizar [{participante.email}]: ")
        if novo_email:
            participante.email = novo_email

        novo_telefone = input(f"Telefone a atualizar [{participante.telefone}]: ")
        if novo_telefone:
            participante.telefone = novo_telefone
        while True:
            nova_data = input(f"Nova data [{participante.data}] (DD-MM-AAAA): ")
            if not nova_data:
                break
            try:

                datetime.datetime.strptime(nova_data, "%d-%m-%Y")
                participante.data = nova_data
                break
            except ValueError:
                print("Formato de data inválido. Use DD-MM-AAAA.")
        sucesso = self.crud_bd_participantes.atualizar_participante(participante)
        if not sucesso:
            print("Falha ao atualizar a participante.")
            return False

        return True

    
    def excluir_participante(self, id_participante=None):
        """Excluir um participante"""
        print("\n===== EXCLUIR PARTICIPANTE =====")
        
        if id_participante is None:
            id_participante = input("Digite o ID do participante para excluir: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_participante = int(id_participante)
        
        participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
        
        if not participante:
            print(f"Nenhum participante encontrado com ID {id_participante}")
            return False
        
        print("\nParticipante a ser excluído:")
        print(f"ID: {participante.id}")
        print(f"Nome: {participante.nome}")
        print(f"CPF: {participante.cpf}")
        print(f"Email: {participante.email}")
        print(f"Telefone: {participante.telefone}")
        
        confirmar = input("\nTem certeza de que deseja excluir este participante? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.crud_bd_participantes.deletar_participante(id_participante)
            if not sucesso:
                print("Falha ao excluir o participante.")
                return False
            return True
        else:
            print("Exclusão cancelada.")
            return False
    
    def buscar_participantes(self, termo_busca=None):
        """Buscar participantes"""
        print("\n===== BUSCAR PARTICIPANTES =====")
        
        if termo_busca is None:
            termo_busca = input("Digite o termo de busca: ")
        
        if not termo_busca:
            print("O termo de busca não pode estar vazio.")
            return []
        
        participantes = self.crud_bd_participantes.buscar_participantes(termo_busca)
        
        if not participantes:
            print(f"Nenhum participante encontrado correspondente a '{termo_busca}'.")
            return []
        else:
            print(f"\nEncontrados {len(participantes)} participantes correspondentes:")
            for participante in participantes:
                print(participante)
            return participantes
