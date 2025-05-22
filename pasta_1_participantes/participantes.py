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
        """Ver todos os participantes"""
        print("\n===== TODOS OS PARTICIPANTES =====")
        
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        
        if not participantes:
            print("Nenhum participante encontrado.")
            return []
        else:
            for participante in participantes:
                print(participante)
            return participantes
    
    def ver_detalhes_participante(self, id_participante=None):
        """Ver detalhes de um participante específico"""
        print("\n===== DETALHES DO PARTICIPANTE =====")
        
        if id_participante is None:
            id_participante = input("Digite o ID do participante: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_participante = int(id_participante)
        
        participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
        
        if participante:
            print("\nDetalhes do Participante:")
            print(f"ID: {participante.id}")
            print(f"Nome: {participante.nome}")
            print(f"CPF: {participante.cpf}")
            print(f"Email: {participante.email}")
            print(f"Telefone: {participante.telefone}")
            if participante.data:
                print(f"Data de Nascimento: {participante.data}")
            return participante
        else:
            print(f"Nenhum participante encontrado com ID {id_participante}")
            return None
    
    def atualizar_participante(self, id_participante=None):
        """Atualizar um participante existente"""
        print("\n===== ATUALIZAR PARTICIPANTE =====")
        
        if id_participante is None:
            id_participante = input("Digite o ID do participante para atualizar: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_participante = int(id_participante)
        
        participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
        
        if not participante:
            print(f"Nenhum participante encontrado com ID {id_participante}")
            return False
        
        print("\nDetalhes Atuais do Participante:")
        print(f"ID: {participante.id}")
        print(f"Nome: {participante.nome}")
        print(f"CPF: {participante.cpf}")
        print(f"Email: {participante.email}")
        print(f"Telefone: {participante.telefone}")
        if participante.data:
            print(f"Data de Nascimento: {participante.data}")
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_nome = input(f"Novo nome [{participante.nome}]: ")
        if novo_nome:
            participante.nome = novo_nome
        
        novo_cpf = input(f"Novo CPF [{participante.cpf}]: ")
        if novo_cpf:
            participante.cpf = novo_cpf
        
        novo_email = input(f"Novo email [{participante.email}]: ")
        if novo_email:
            participante.email = novo_email
        
        novo_telefone = input(f"Novo telefone [{participante.telefone}]: ")
        if novo_telefone:
            participante.telefone = novo_telefone
        
        nova_data = input(f"Nova data de nascimento [{participante.data}] (AAAA-MM-DD): ")
        if nova_data:
            participante.data = nova_data
        
        sucesso = self.crud_bd_participantes.atualizar_participante(participante)
        if not sucesso:
            print("Falha ao atualizar o participante.")
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
