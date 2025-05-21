from pasta_0_modelos.evento import Evento
import datetime

class CrudEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def adicionar_evento(self):
        """Adiciona um novo evento"""
        print("\n===== ADICIONAR NOVO EVENTO =====")
        
        titulo = input("Digite o título do evento: ")
        descricao = input("Digite a descrição do evento: ")
        
        # Validação de data
        while True:
            data_str = input("Digite a data do evento (AAAA-MM-DD): ")
            try:
                # Valida o formato da data
                if data_str:
                    datetime.datetime.strptime(data_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Formato de data inválido. Use AAAA-MM-DD.")
        
        local = input("Digite o local do evento: ")
        
        evento = Evento(titulo=titulo, descricao=descricao, data=data_str, local=local)
        self.gerenciador_bd.criar_evento(evento)
        
        return True
    
    def ver_todos_eventos(self):
        """Ver todos os eventos"""
        print("\n===== TODOS OS EVENTOS =====")
        
        eventos = self.gerenciador_bd.ler_todos_eventos()
        
        if not eventos:
            print("Nenhum evento encontrado.")
            return []
        else:
            for evento in eventos:
                print(evento)
            return eventos
    
    def ver_detalhes_evento(self, id_evento=None):
        """Ver detalhes de um evento específico"""
        print("\n===== DETALHES DO EVENTO =====")
        
        if id_evento is None:
            id_evento = input("Digite o ID do evento: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_evento = int(id_evento)
        
        evento = self.gerenciador_bd.ler_evento_por_id(id_evento)
        
        if evento:
            print("\nDetalhes do Evento:")
            print(f"ID: {evento.id}")
            print(f"Título: {evento.titulo}")
            print(f"Descrição: {evento.descricao}")
            print(f"Data: {evento.data}")
            print(f"Local: {evento.local}")
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
        
        evento = self.gerenciador_bd.ler_evento_por_id(id_evento)
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        
        print("\nDetalhes Atuais do Evento:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        print(f"Local: {evento.local}")
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_titulo = input(f"Novo título [{evento.titulo}]: ")
        if novo_titulo:
            evento.titulo = novo_titulo
        
        nova_descricao = input(f"Nova descrição [{evento.descricao}]: ")
        if nova_descricao:
            evento.descricao = nova_descricao
        
        # Validação de data
        while True:
            nova_data = input(f"Nova data [{evento.data}] (AAAA-MM-DD): ")
            if not nova_data:
                break
            try:
                # Valida o formato da data
                datetime.datetime.strptime(nova_data, "%Y-%m-%d")
                evento.data = nova_data
                break
            except ValueError:
                print("Formato de data inválido. Use AAAA-MM-DD.")
        
        novo_local = input(f"Novo local [{evento.local}]: ")
        if novo_local:
            evento.local = novo_local
        
        sucesso = self.gerenciador_bd.atualizar_evento(evento)
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
        
        evento = self.gerenciador_bd.ler_evento_por_id(id_evento)
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        
        print("\nEvento a ser excluído:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        print(f"Local: {evento.local}")
        
        confirmar = input("\nTem certeza de que deseja excluir este evento? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.gerenciador_bd.deletar_evento(id_evento)
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
        
        eventos = self.gerenciador_bd.buscar_eventos(termo_busca)
        
        if not eventos:
            print(f"Nenhum evento encontrado correspondente a '{termo_busca}'.")
            return []
        else:
            print(f"\nEncontrados {len(eventos)} eventos correspondentes:")
            for evento in eventos:
                print(evento)
            return eventos