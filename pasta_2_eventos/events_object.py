import datetime

class Event:
    def __init__(self, id=None, nome=None, descricao=None, data_inicio=None, hora_inicio= None,
                 data_fim = None, hora_fim = None, publico_alvo=None, tipo = None, endereco = None, capacidade = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.hora_inicio = hora_inicio
        self.data_fim = data_fim
        self.hora_fim = hora_fim
        self.publico_alvo = publico_alvo
        self.tipo = tipo
        self.endereco = endereco
        self.capacidade =capacidade
    
    def __str__(self):
        return (
            f"Evento: {self.nome}\n"
            f"ID: {self.id}\n"
            f"Descrição: {self.descricao}\n"
            f"Inicio: {self.data_inicio} às {self.hora_inicio}\n"
            f"Término: {self.data_fim} às {self.hora_fim}\n"
            f"Público-Alvo: {self.publico_alvo}\n"
            f"Tipo: {self.tipo}\n"
            f"Endereço: {self.endereco}\n"
            f"Capacidade Max: {self.capacidade}\n"
        )
    
    def to_tuple(self):
        """Convert the event object to a tuple for database operations"""
        return (
            self.nome, 
            self.descricao, 
            self.data_inicio, 
            self.hora_inicio,
            self.data_fim, 
            self.hora_fim, 
            self.publico_alvo, 
            self.tipo,
            self.endereco, 
            self.capacidade)
    
    def to_tuple_with_id(self):
        """Convert the event object to a tuple including the ID for database operations"""
        return (
            self.id,
            self.nome, 
            self.descricao, 
            self.data_inicio, 
            self.hora_inicio,
            self.data_fim, 
            self.hora_fim, 
            self.publico_alvo, 
            self.tipo,
            self.endereco, 
            self.capacidade
        )
    
    @staticmethod
    def from_tuple(tuple_data):
        """Create an Event object from a database tuple"""
        return Event(
            id=tuple_data[0],
            nome = tuple_data[1],
            descricao = tuple_data[2],
            data_inicio = tuple_data[3],
            hora_inicio = tuple_data[4],
            data_fim = tuple_data[5],
            hora_fim = tuple_data[6],
            publico_alvo = tuple_data[7],
            tipo = tuple_data[8],
            endereco = tuple_data[9],
            capacidade = tuple_data[10],

        )
    
    
    @property
    def duracao(self):
        if all([self.data_inicio, self.hora_fim, self.data_fim, self.hora_fim]):
            inicio = datetime.combine(self.data_inicio, self.hora_inicio)
            fim = datetime.combine(self.data_fim, self.hora_fim)
            return(fim - inicio).total_seconds()/3600
        return None
