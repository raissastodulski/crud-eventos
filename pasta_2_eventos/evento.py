from datetime import datetime, date, time

class Evento:
    def __init__(self, id=None, nome=None, descricao=None, data_inicio=None, hora_inicio=None,
                 data_fim=None, hora_fim=None, publico_alvo=None, tipo=None, endereco=None, capacidade=None):
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
        self.capacidade = capacidade

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
        """Converte o evento para tupla com strings (para inserção no banco)"""
        return (
            self.nome, 
            self.descricao, 
            self.data_inicio.isoformat() if self.data_inicio else None, 
            self.hora_inicio.strftime('%H:%M') if self.hora_inicio else None,
            self.data_fim.isoformat() if self.data_fim else None, 
            self.hora_fim.strftime('%H:%M') if self.hora_fim else None, 
            self.publico_alvo, 
            self.tipo,
            self.endereco, 
            self.capacidade)
    
    def para_tupla_com_id(self):
        """Converte o evento para tupla com ID e strings (para atualização no banco)"""
        return (
            self.id,
            self.nome, 
            self.descricao, 
            self.data_inicio.isoformat() if self.data_inicio else None, 
            self.hora_inicio.strftime('%H:%M') if self.hora_inicio else None,
            self.data_fim.isoformat() if self.data_fim else None, 
            self.hora_fim.strftime('%H:%M') if self.hora_fim else None, 
            self.publico_alvo, 
            self.tipo,
            self.endereco, 
            self.capacidade
        )
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um evento a partir de tupla do banco (convertendo strings para objetos date/time)"""
        id, nome, descricao, data_inicio_str, hora_inicio_str, data_fim_str, hora_fim_str, publico_alvo, tipo, endereco, capacidade = dados
        
        # Converter strings para objetos date/time
        data_inicio = None
        if data_inicio_str:
            try:
                data_inicio = datetime.fromisoformat(data_inicio_str).date()
            except (ValueError, TypeError):
                # Tentar formato alternativo
                try:
                    data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    data_inicio = None
        
        hora_inicio = None
        if hora_inicio_str:
            try:
                hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            except (ValueError, TypeError):
                hora_inicio = None
        
        data_fim = None
        if data_fim_str:
            try:
                data_fim = datetime.fromisoformat(data_fim_str).date()
            except (ValueError, TypeError):
                # Tentar formato alternativo
                try:
                    data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    data_fim = None
        
        hora_fim = None
        if hora_fim_str:
            try:
                hora_fim = datetime.strptime(hora_fim_str, '%H:%M').time()
            except (ValueError, TypeError):
                hora_fim = None
        
        return cls(
            id=id,
            nome=nome, 
            descricao=descricao, 
            data_inicio=data_inicio, 
            hora_inicio=hora_inicio,
            data_fim=data_fim,
            hora_fim=hora_fim,
            publico_alvo=publico_alvo,
            tipo=tipo,
            endereco=endereco,
            capacidade=capacidade
        )
    
    @property
    def duracao(self):
        """Calcula a duração do evento em horas"""
        if all([self.data_inicio, self.hora_inicio, self.data_fim, self.hora_fim]):
            try:
                inicio = datetime.combine(self.data_inicio, self.hora_inicio)
                fim = datetime.combine(self.data_fim, self.hora_fim)
                return (fim - inicio).total_seconds() / 3600
            except (TypeError, ValueError):
                return None
        return None
