from datetime import datetime, date, time
from compartilhado.formatador_data import FormatadorData

class Evento:
    def __init__(self, id=None, nome=None, descricao=None, data_inicio=None, hora_inicio=None,
                 data_fim=None, hora_fim=None, publico_alvo=None, local=None, endereco=None, capacidade=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.hora_inicio = hora_inicio
        self.data_fim = data_fim
        self.hora_fim = hora_fim
        self.publico_alvo = publico_alvo
        self.local = local
        self.endereco = endereco
        self.capacidade = capacidade

    def __str__(self):
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
            f"Local: {self.local}\n"
            f"Endereço: {self.endereco}\n"
            f"Capacidade Max: {self.capacidade}\n"
        )    
    
    def para_tupla(self):
        return (
            self.nome, 
            self.descricao, 
            FormatadorData.data_para_iso(self.data_inicio), 
            FormatadorData.hora_para_str(self.hora_inicio),
            FormatadorData.data_para_iso(self.data_fim), 
            FormatadorData.hora_para_str(self.hora_fim), 
            self.publico_alvo, 
            self.local,
            self.endereco, 
            self.capacidade)
    
    def para_tupla_com_id(self):
        return (
            self.id,
            self.nome, 
            self.descricao, 
            FormatadorData.data_para_iso(self.data_inicio), 
            FormatadorData.hora_para_str(self.hora_inicio),
            FormatadorData.data_para_iso(self.data_fim), 
            FormatadorData.hora_para_str(self.hora_fim), 
            self.publico_alvo, 
            self.local,
            self.endereco, 
            self.capacidade
        )
    
    @classmethod
    def de_tupla(cls, dados):
        if len(dados) == 11:
            id, nome, descricao, data_inicio_str, hora_inicio_str, data_fim_str, hora_fim_str, publico_alvo, tipo, endereco, capacidade = dados
            local = endereco
            endereco_final = endereco
        elif len(dados) == 10:
            nome, descricao, data_inicio_str, hora_inicio_str, data_fim_str, hora_fim_str, publico_alvo, local, endereco_final, capacidade = dados
            id = None
        elif len(dados) >= 11:
            id, nome, descricao, data_inicio_str, hora_inicio_str, data_fim_str, hora_fim_str, publico_alvo, local, endereco_final, capacidade = dados[:11]
        else:
            raise ValueError(f"Formato de dados inválido para Evento: {dados}")
        
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
            local=local,
            endereco=endereco_final,
            capacidade=capacidade
        )
    
    @property
    def duracao(self):
        if all([self.data_inicio, self.hora_inicio, self.data_fim, self.hora_fim]):
            try:
                inicio = datetime.combine(self.data_inicio, self.hora_inicio)
                fim = datetime.combine(self.data_fim, self.hora_fim)
                return (fim - inicio).total_seconds() / 3600
            except (TypeError, ValueError):
                return None
        return None
    
    def data_inicio_formatada(self):
        return FormatadorData.data_para_str(self.data_inicio)
    
    def data_fim_formatada(self):
        return FormatadorData.data_para_str(self.data_fim)
    
    def hora_inicio_formatada(self):
        return FormatadorData.hora_para_str(self.hora_inicio)
    
    def hora_fim_formatada(self):
        return FormatadorData.hora_para_str(self.hora_fim)
    
    def periodo_formatado(self):
        if self.data_inicio == self.data_fim:
            return f"{self.data_inicio_formatada()} das {self.hora_inicio_formatada()} às {self.hora_fim_formatada()}"
        else:
            return f"De {self.data_inicio_formatada()} às {self.hora_inicio_formatada()} até {self.data_fim_formatada()} às {self.hora_fim_formatada()}"
