from pasta_1_participantes.participante_model import Participante
from pasta_1_participantes.crud_bd_participantes import CrudBDParticipantes

class CrudParticipantes:
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
    
    def ver_todos_participantes(self):
        """Mostrar todos os participantes"""
        print("\n==== LISTAR PARTICIPANTES ====")
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        if participantes:
            for participante in participantes:
                print(participante)
        else:
            print("Não há participantes")
    
    def ver_detalhes_participantes(self, idParticipante=None):
        """Ver todos os detalhes de um participante"""
        print("\n==== DETALHES PARTICIPANTES ====")
        if idParticipante is None:
            idParticipante = input("Digite o ID do participante: ")
        if not idParticipante.isdigit():
            print("ID inválido, digite um ID válido, por favor")
            return none
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
