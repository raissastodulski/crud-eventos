class Evento:
    def __init__(self, titulo="", descricao="", data="", local="", id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.local = local
    
    def para_tupla(self):
        """Converte evento para tupla para operações de banco de dados (sem ID)"""
        # Cria uma tupla com todos os campos conforme esperado pelo método criar_evento do GerenciadorBD
        hora_inicio = getattr(self, 'hora_inicio', None)
        hora_fim = getattr(self, 'hora_fim', None)
        publico_alvo = getattr(self, 'publico_alvo', None)
        capacidade = getattr(self, 'capacidade', None)
        endereco = getattr(self, 'endereco', None)
        return (self.titulo, self.descricao, self.data, hora_inicio, hora_fim, publico_alvo, capacidade, self.local, endereco)
    
    def para_tupla_com_id(self):
        """Converte evento para tupla para operações de banco de dados (com ID)"""
        # Cria uma tupla com todos os campos conforme esperado pelo método atualizar_evento do GerenciadorBD
        hora_inicio = getattr(self, 'hora_inicio', None)
        hora_fim = getattr(self, 'hora_fim', None)
        publico_alvo = getattr(self, 'publico_alvo', None)
        capacidade = getattr(self, 'capacidade', None)
        endereco = getattr(self, 'endereco', None)
        return (self.titulo, self.descricao, self.data, hora_inicio, hora_fim, publico_alvo, capacidade, self.local, endereco, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um objeto Evento a partir de uma tupla do banco de dados"""
        if dados and len(dados) >= 4:
            id, titulo, descricao, data = dados[0:4]
            # Determinamos qual índice corresponde ao local com base no schema do banco de dados
            # Na tabela eventos, o local está na posição 8 (índice 8) conforme o esquema de criação de tabelas
            local = ""
            if len(dados) > 8:
                local = dados[8]
            evento = cls(titulo=titulo, descricao=descricao, data=data, local=local, id=id)
            
            # Adiciona os outros atributos se disponíveis
            if len(dados) > 4:
                evento.hora_inicio = dados[4]
            if len(dados) > 5:
                evento.hora_fim = dados[5]
            if len(dados) > 6:
                evento.publico_alvo = dados[6]
            if len(dados) > 7:
                evento.capacidade = dados[7]
            if len(dados) > 9:
                evento.endereco = dados[9]
                
            return evento
        else:
            print(f"Aviso: Dados incompletos para criar um Evento: {dados}")
            return None
    
    def __str__(self):
        """Representação em string do evento"""
        data_str = f" | {self.data}" if self.data else ""
        local_str = f" | {self.local}" if self.local else ""
        return f"[{self.id}] {self.titulo}{data_str}{local_str}"