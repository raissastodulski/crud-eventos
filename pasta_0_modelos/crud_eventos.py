from .evento import Evento
from .crud_bd_eventos import CrudBDEventos
import datetime

class CrudEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_eventos = CrudBDEventos(gerenciador_bd)
    
    def adicionar_evento(self):
        """Adiciona um novo evento"""
        print("\n===== ADICIONAR NOVO EVENTO =====")
        
        titulo = input("Digite o título do evento: ")
        descricao = input("Digite a descrição do evento: ")
        
        # Validação de data
        while True:
            data_str = input("Digite a data do evento (DD-MM-AAAA): ")
            try:
                # Valida o formato da data
                if data_str:
                    datetime.datetime.strptime(data_str, "%d-%m-%Y")
                break
            except ValueError:
                print("Formato de data inválido. Use DD-MM-AAAA.")
        
        # Validação de hora início
        while True:
            hora_inicio = input("Digite a hora de início do evento (HH:MM): ")
            if not hora_inicio:
                break
            try:
                # Valida o formato da hora
                datetime.datetime.strptime(hora_inicio, "%H:%M")
                break
            except ValueError:
                print("Formato de hora inválido. Use HH:MM.")
        
        # Validação de hora fim
        while True:
            hora_fim = input("Digite a hora de término do evento (HH:MM): ")
            if not hora_fim:
                break
            try:
                # Valida o formato da hora
                datetime.datetime.strptime(hora_fim, "%H:%M")
                break
            except ValueError:
                print("Formato de hora inválido. Use HH:MM.")
        
        publico_alvo = input("Digite o público-alvo do evento: ")
        
        # Validação de capacidade (número inteiro)
        capacidade = None
        capacidade_str = input("Digite a capacidade do evento (em número de pessoas): ")
        if capacidade_str and capacidade_str.isdigit():
            capacidade = int(capacidade_str)
        elif capacidade_str:
            print("Aviso: Capacidade inválida. Deve ser um número inteiro.")
        
        local = input("Digite o local do evento: ")
        endereco = input("Digite o endereço completo do evento: ")
        
        evento = Evento(titulo=titulo, descricao=descricao, data=data_str, local=local)
        evento.hora_inicio = hora_inicio if hora_inicio else None
        evento.hora_fim = hora_fim if hora_fim else None
        evento.publico_alvo = publico_alvo if publico_alvo else None
        evento.capacidade = capacidade
        evento.endereco = endereco if endereco else None
        self.crud_bd_eventos.criar_evento(evento)
        
        return True
    
    def ver_todos_eventos(self):
        """Ver todos os eventos"""
        print("\n===== TODOS OS EVENTOS =====")
        
        try:
            eventos = self.crud_bd_eventos.ler_todos_eventos()
            
            if not eventos:
                print("Nenhum evento encontrado.")
                return []
            else:
                for evento in eventos:
                    if evento:  # Verifica se o evento é válido
                        print(evento)
                return eventos
        except Exception as e:
            print(f"Erro ao listar eventos: {e}")
            return []
    
    def ver_detalhes_evento(self, id_evento=None):
        """Ver detalhes de um evento específico"""
        print("\n===== DETALHES DO EVENTO =====")
        
        if id_evento is None:
            id_evento = input("Digite o ID do evento: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        
        if evento:
            print("\nDetalhes do Evento:")
            print(f"ID: {evento.id}")
            print(f"Título: {evento.titulo}")
            print(f"Descrição: {evento.descricao}")
            print(f"Data: {evento.data}")
            
            # Mostrar campos adicionais
            if hasattr(evento, 'hora_inicio') and evento.hora_inicio:
                print(f"Hora de início: {evento.hora_inicio}")
            if hasattr(evento, 'hora_fim') and evento.hora_fim:
                print(f"Hora de término: {evento.hora_fim}")
            if hasattr(evento, 'publico_alvo') and evento.publico_alvo:
                print(f"Público-alvo: {evento.publico_alvo}")
            if hasattr(evento, 'capacidade') and evento.capacidade:
                print(f"Capacidade: {evento.capacidade} pessoas")
            
            print(f"Local: {evento.local}")
            
            if hasattr(evento, 'endereco') and evento.endereco:
                print(f"Endereço completo: {evento.endereco}")
            
            return evento
        else:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return None
    
    def atualizar_evento(self, id_evento=None):
        """Atualizar um evento existente"""
        print("\n===== ATUALIZAR EVENTO =====")
        
        if id_evento is None:
            id_evento = input("Digite o ID do evento para atualizar: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        
        print("\nDetalhes Atuais do Evento:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        
        # Mostrar todos os campos adicionais
        hora_inicio = getattr(evento, 'hora_inicio', None)
        if hora_inicio:
            print(f"Hora de início: {hora_inicio}")
            
        hora_fim = getattr(evento, 'hora_fim', None)
        if hora_fim:
            print(f"Hora de término: {hora_fim}")
            
        publico_alvo = getattr(evento, 'publico_alvo', None)
        if publico_alvo:
            print(f"Público-alvo: {publico_alvo}")
            
        capacidade = getattr(evento, 'capacidade', None)
        if capacidade:
            print(f"Capacidade: {capacidade} pessoas")
            
        print(f"Local: {evento.local}")
        
        endereco = getattr(evento, 'endereco', None)
        if endereco:
            print(f"Endereço completo: {endereco}")
            
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_titulo = input(f"Novo título [{evento.titulo}]: ")
        if novo_titulo:
            evento.titulo = novo_titulo
        
        nova_descricao = input(f"Nova descrição [{evento.descricao}]: ")
        if nova_descricao:
            evento.descricao = nova_descricao
        
        # Validação de data
        while True:
            nova_data = input(f"Nova data [{evento.data}] (DD-MM-AAAA): ")
            if not nova_data:
                break
            try:
                # Valida o formato da data
                datetime.datetime.strptime(nova_data, "%d-%m-%Y")
                evento.data = nova_data
                break
            except ValueError:
                print("Formato de data inválido. Use DD-MM-AAAA.")
        
        # Validação de hora início
        while True:
            nova_hora_inicio = input(f"Nova hora de início [{hora_inicio or ''}] (HH:MM): ")
            if not nova_hora_inicio:
                break
            try:
                # Valida o formato da hora
                datetime.datetime.strptime(nova_hora_inicio, "%H:%M")
                evento.hora_inicio = nova_hora_inicio
                break
            except ValueError:
                print("Formato de hora inválido. Use HH:MM.")
        
        # Validação de hora fim
        while True:
            nova_hora_fim = input(f"Nova hora de término [{hora_fim or ''}] (HH:MM): ")
            if not nova_hora_fim:
                break
            try:
                # Valida o formato da hora
                datetime.datetime.strptime(nova_hora_fim, "%H:%M")
                evento.hora_fim = nova_hora_fim
                break
            except ValueError:
                print("Formato de hora inválido. Use HH:MM.")
        
        novo_publico_alvo = input(f"Novo público-alvo [{publico_alvo or ''}]: ")
        if novo_publico_alvo:
            evento.publico_alvo = novo_publico_alvo
        
        # Validação de capacidade (número inteiro)
        nova_capacidade_str = input(f"Nova capacidade [{capacidade or ''}] (em número de pessoas): ")
        if nova_capacidade_str:
            if nova_capacidade_str.isdigit():
                evento.capacidade = int(nova_capacidade_str)
            else:
                print("Aviso: Capacidade inválida. Deve ser um número inteiro.")
        
        novo_local = input(f"Novo local [{evento.local}]: ")
        if novo_local:
            evento.local = novo_local
            
        novo_endereco = input(f"Novo endereço completo [{endereco or ''}]: ")
        if novo_endereco:
            evento.endereco = novo_endereco
        
        sucesso = self.crud_bd_eventos.atualizar_evento(evento)
        if not sucesso:
            print("Falha ao atualizar o evento.")
            return False
        
        return True
    
    def excluir_evento(self, id_evento=None):
        """Excluir um evento"""
        print("\n===== EXCLUIR EVENTO =====")
        
        if id_evento is None:
            id_evento = input("Digite o ID do evento para excluir: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        
        print("\nEvento a ser excluído:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        
        # Mostrar todos os campos adicionais
        if hasattr(evento, 'hora_inicio') and evento.hora_inicio:
            print(f"Hora de início: {evento.hora_inicio}")
        if hasattr(evento, 'hora_fim') and evento.hora_fim:
            print(f"Hora de término: {evento.hora_fim}")
        if hasattr(evento, 'publico_alvo') and evento.publico_alvo:
            print(f"Público-alvo: {evento.publico_alvo}")
        if hasattr(evento, 'capacidade') and evento.capacidade:
            print(f"Capacidade: {evento.capacidade} pessoas")
            
        print(f"Local: {evento.local}")
        
        if hasattr(evento, 'endereco') and evento.endereco:
            print(f"Endereço completo: {evento.endereco}")
        
        confirmar = input("\nTem certeza de que deseja excluir este evento? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.crud_bd_eventos.deletar_evento(id_evento)
            if not sucesso:
                print("Falha ao excluir o evento.")
                return False
            return True
        else:
            print("Exclusão cancelada.")
            return False
    
    def buscar_eventos(self, termo_busca=None):
        """Buscar eventos"""
        print("\n===== BUSCAR EVENTOS =====")
        
        if termo_busca is None:
            termo_busca = input("Digite o termo de busca: ")
        
        if not termo_busca:
            print("O termo de busca não pode estar vazio.")
            return []
        
        eventos = self.crud_bd_eventos.buscar_eventos(termo_busca)
        
        if not eventos:
            print(f"Nenhum evento encontrado correspondente a '{termo_busca}'.")
            return []
        else:
            print(f"\nEncontrados {len(eventos)} eventos correspondentes:")
            for evento in eventos:
                print(evento)
            return eventos