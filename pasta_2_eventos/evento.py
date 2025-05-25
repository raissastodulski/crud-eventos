from datetime import datetime

class Evento:
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
    
    def para_tupla(self):
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
    
    def para_tupla_com_id(self):
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
    
    @classmethod
    def de_tupla(cls, dados):
        id, titulo, descricao, data_incio, hora_inicio, data_fim, hora_fim, publico_alvo, tipo, endereco, capacidade = dados
        return cls(
            titulo=titulo, 
            descricao=descricao, 
            data_incio=data_incio, 
            hora_inicio=hora_inicio,
            data_fim = data_fim,
            hora_fim = hora_fim,
            publico_alvo = publico_alvo,
            tipo = tipo,
            endereco = endereco,
            capacidade = capacidade, 
            id=id
        )
    
    @property
    def duracao(self):
        if all([self.data_inicio, self.hora_fim, self.data_fim, self.hora_fim]):
            inicio = datetime.combine(self.data_inicio, self.hora_inicio)
            fim = datetime.combine(self.data_fim, self.hora_fim)
            return(fim - inicio).total_seconds()/3600
        return None    