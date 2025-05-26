from .participante import Participante
from .crud_bd_participantes import CrudBdParticipantes
from datetime import datetime
from utils import FormatadorTabela


class CrudParticipantes:
    @staticmethod
    def validar_cpf(cpf):
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

    @staticmethod
    def validar_data_nascimento(data_str):
        if not data_str.strip():
            return None
        
        try:
            return datetime.strptime(data_str.strip(), "%d/%m/%Y")
        except ValueError:
            return None

    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_participantes = CrudBdParticipantes(gerenciador_bd)
    
    def adicionar_participante(self):
        print("\n===== ADICIONAR NOVO PARTICIPANTE =====")
        
        nome = input("Digite o nome do participante: ")
        
        while True:
            cpf = input("Digite o CPF do participante: ")
            if not cpf or self.validar_cpf(cpf):
                break
            print("CPF inválido. Tente novamente.")
        
        email = input("Digite o email do participante: ")
        telefone = input("Digite o telefone do participante: ")
        
        while True:
            data_nascimento_str = input("Digite a data de nascimento (DD/MM/AAAA) ou deixe em branco: ")
            if not data_nascimento_str.strip():
                data_nascimento = None
                break
            
            data_nascimento = self.validar_data_nascimento(data_nascimento_str)
            if data_nascimento:
                break
            else:
                print("Formato de data inválido. Use DD/MM/AAAA.")
        
        participante = Participante(nome=nome, cpf=cpf, email=email, telefone=telefone, data_nascimento=data_nascimento)
        self.crud_bd_participantes.criar_participante(participante)
        
        return True
    
    def visualizar_participantes(self):
        print("\n==== LISTAR PARTICIPANTES ====")
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        if participantes:
            dados_tabela = []
            for p in participantes:
                data_nasc = ""
                if p.data_nascimento:
                    if isinstance(p.data_nascimento, datetime):
                        data_nasc = p.data_nascimento.strftime('%d/%m/%Y')
                    else:
                        data_nasc = str(p.data_nascimento)
                
                dados_tabela.append([
                    p.id,
                    FormatadorTabela.truncar_texto(p.nome, 25),
                    FormatadorTabela.truncar_texto(p.cpf or "", 14),
                    FormatadorTabela.truncar_texto(p.email or "", 30),
                    FormatadorTabela.truncar_texto(p.telefone or "", 15),
                    data_nasc
                ])
            
            cabecalhos = ["ID", "Nome", "CPF", "Email", "Telefone", "Nascimento"]
            larguras = [4, 25, 14, 30, 15, 12]
            
            tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
            print(tabela)
            print(f"\nTotal: {len(participantes)} participante(s)")
        else:
            print("Não há participantes cadastrados.")
    
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
            data_nasc = "Não informada"
            if participante.data_nascimento:
                if isinstance(participante.data_nascimento, datetime):
                    data_nasc = participante.data_nascimento.strftime('%d/%m/%Y')
                else:
                    data_nasc = str(participante.data_nascimento)
            
            dados_detalhes = {
                "ID": participante.id,
                "Nome": participante.nome,
                "CPF": participante.cpf or "Não informado",
                "Email": participante.email or "Não informado",
                "Telefone": participante.telefone or "Não informado",
                "Data de Nascimento": data_nasc
            }
            
            tabela_detalhes = FormatadorTabela.criar_tabela_detalhes(
                f"DETALHES DO PARTICIPANTE (ID: {participante.id})",
                dados_detalhes
            )
            print(tabela_detalhes)
            return participante
        else:
            print("Participante com essa ID não encontrada, tente novamente")
            return None
        
    def atualizar_participante(self, idParticipante=None):
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
        
        data_nascimento_atual = ""
        if participante.data_nascimento:
            if isinstance(participante.data_nascimento, datetime):
                data_nascimento_atual = participante.data_nascimento.strftime('%d/%m/%Y')
            else:
                data_nascimento_atual = str(participante.data_nascimento)
        print(f"Data de Nascimento: {data_nascimento_atual or 'Não informada'}")

        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_nome = input(f"Nome a atualizar [{participante.nome}]: ")
        if novo_nome:
            participante.nome = novo_nome
            
        while True:
            novo_cpf = input(f"CPF a atualizar [{participante.cpf}]: ")
            if not novo_cpf:
                break 
            if self.validar_cpf(novo_cpf):
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
            nova_data_str = input(f"Nova data de nascimento [{data_nascimento_atual}] (DD/MM/AAAA): ")
            if not nova_data_str:
                break
            
            nova_data = self.validar_data_nascimento(nova_data_str)
            if nova_data:
                participante.data_nascimento = nova_data
                break
            else:
                print("Formato de data inválido. Use DD/MM/AAAA.")
                
        sucesso = self.crud_bd_participantes.atualizar_participante(participante)
        if not sucesso:
            print("Falha ao atualizar o participante.")
            return False

        return True
    
    def excluir_participante(self, id_participante=None):
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
            print(f"\n🔍 Encontrados {len(participantes)} participante(s) correspondente(s) a '{termo_busca}':")
            
            dados_tabela = []
            for p in participantes:
                data_nasc = ""
                if p.data_nascimento:
                    if isinstance(p.data_nascimento, datetime):
                        data_nasc = p.data_nascimento.strftime('%d/%m/%Y')
                    else:
                        data_nasc = str(p.data_nascimento)
                
                dados_tabela.append([
                    p.id,
                    FormatadorTabela.truncar_texto(p.nome, 25),
                    FormatadorTabela.truncar_texto(p.cpf or "", 14),
                    FormatadorTabela.truncar_texto(p.email or "", 30),
                    FormatadorTabela.truncar_texto(p.telefone or "", 15),
                    data_nasc
                ])
            
            cabecalhos = ["ID", "Nome", "CPF", "Email", "Telefone", "Nascimento"]
            larguras = [4, 25, 14, 30, 15, 12]
            
            tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
            print(tabela)
            return participantes
