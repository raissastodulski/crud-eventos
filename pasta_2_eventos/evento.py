from datetime import datetime, date, time
from compartilhado.formatador_data import FormatadorData

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
        # Usar FormatadorData para exibir datas no formato brasileiro
        data_inicio_str = FormatadorData.data_para_str(self.data_inicio)
        data_fim_str = FormatadorData.data_para_str(self.data_fim)
        hora_inicio_str = FormatadorData.hora_para_str(self.hora_inicio)
        hora_fim_str = FormatadorData.hora_para_str(self.hora_fim)
        
        return (
            f"Evento: {self.nome}\n"
            f"ID: {self.id}\n"
            f"Descrição: {self.descricao}\n"
            f"Inicio: {data_inicio_str} às {hora_inicio_str}\n"
            f"Término: {data_fim_str} às {hora_fim_str}\n"
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
            FormatadorData.data_para_iso(self.data_inicio), 
            FormatadorData.hora_para_str(self.hora_inicio),
            FormatadorData.data_para_iso(self.data_fim), 
            FormatadorData.hora_para_str(self.hora_fim), 
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
            FormatadorData.data_para_iso(self.data_inicio), 
            FormatadorData.hora_para_str(self.hora_inicio),
            FormatadorData.data_para_iso(self.data_fim), 
            FormatadorData.hora_para_str(self.hora_fim), 
            self.publico_alvo, 
            self.tipo,
            self.endereco, 
            self.capacidade
        )
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um evento a partir de tupla do banco (convertendo strings para objetos date/time)"""
        id, nome, descricao, data_inicio_str, hora_inicio_str, data_fim_str, hora_fim_str, publico_alvo, tipo, endereco, capacidade = dados
        
        # Usar FormatadorData para converter strings do banco para objetos date/time
        data_inicio = FormatadorData.iso_para_data(data_inicio_str)
        hora_inicio = FormatadorData.str_para_hora(hora_inicio_str)
        data_fim = FormatadorData.iso_para_data(data_fim_str)
        hora_fim = FormatadorData.str_para_hora(hora_fim_str)
        
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
    
    # Métodos de formatação convenientes
    def data_inicio_formatada(self):
        """Retorna data de início formatada em dd/mm/yyyy"""
        return FormatadorData.data_para_str(self.data_inicio)
    
    def data_fim_formatada(self):
        """Retorna data de fim formatada em dd/mm/yyyy"""
        return FormatadorData.data_para_str(self.data_fim)
    
    def hora_inicio_formatada(self):
        """Retorna hora de início formatada em hh:mm"""
        return FormatadorData.hora_para_str(self.hora_inicio)
    
    def hora_fim_formatada(self):
        """Retorna hora de fim formatada em hh:mm"""
        return FormatadorData.hora_para_str(self.hora_fim)
    
    def periodo_formatado(self):
        """Retorna período completo formatado"""
        if self.data_inicio == self.data_fim:
            return f"{self.data_inicio_formatada()} das {self.hora_inicio_formatada()} às {self.hora_fim_formatada()}"
        else:
            return f"De {self.data_inicio_formatada()} às {self.hora_inicio_formatada()} até {self.data_fim_formatada()} às {self.hora_fim_formatada()}"
