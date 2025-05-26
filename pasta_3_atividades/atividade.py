from compartilhado.formatador_data import FormatadorData
from datetime import time, datetime

class Atividade:
    def __init__(self, nome="", facilitador="", local="", id_evento=None, 
                 data_inicio=None, hora_inicio="", data_fim=None, hora_fim="", vagas=0, id=None):
        self.id = id
        self.nome = nome
        self.facilitador = facilitador
        self.local = local
        self.id_evento = id_evento
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.vagas = vagas
        
        if isinstance(hora_inicio, time):
            self.hora_inicio = hora_inicio.strftime("%H:%M")
        else:
            self.hora_inicio = hora_inicio
            
        if isinstance(hora_fim, time):
            self.hora_fim = hora_fim.strftime("%H:%M")
        else:
            self.hora_fim = hora_fim

    def para_tupla(self):
        return (
            self.nome,
            self.facilitador,
            self.local,
            self.id_evento,
            FormatadorData.data_para_iso(self.data_inicio),
            self.hora_inicio,
            FormatadorData.data_para_iso(self.data_fim),
            self.hora_fim,
            self.vagas,
        )

    def para_tupla_com_id(self):
        return (
            self.nome,
            self.facilitador,
            self.local,
            self.id_evento,
            FormatadorData.data_para_iso(self.data_inicio),
            self.hora_inicio,
            FormatadorData.data_para_iso(self.data_fim),
            self.hora_fim,
            self.vagas,
            self.id,
        )

    @classmethod
    def de_tupla(cls, dados):
        if len(dados) == 7:
            id, nome, facilitador, local, id_evento, hora_inicio, vagas = dados
            data_inicio = None
            data_fim = None
            hora_fim = ""
        elif len(dados) >= 10:
            id, nome, facilitador, local, id_evento, data_inicio_str, hora_inicio, data_fim_str, hora_fim, vagas = dados[:10]
            data_inicio = FormatadorData.iso_para_data(data_inicio_str)
            data_fim = FormatadorData.iso_para_data(data_fim_str)
        else:
            raise ValueError(f"Formato de dados inválido para Atividade: {dados}")
        
        return cls(
            nome=nome,
            facilitador=facilitador,
            local=local,
            id_evento=id_evento,
            data_inicio=data_inicio,
            hora_inicio=hora_inicio,
            data_fim=data_fim,
            hora_fim=hora_fim,
            vagas=vagas,
            id=id,
        )

    def __str__(self):
        periodo = ""
        if self.data_inicio and self.hora_inicio:
            data_inicio_str = FormatadorData.data_para_str(self.data_inicio) if self.data_inicio else ""
            periodo = f" | Período: {data_inicio_str} {self.hora_inicio}"
            if self.data_fim and self.hora_fim:
                if self.data_inicio == self.data_fim:
                    periodo += f" às {self.hora_fim}"
                else:
                    data_fim_str = FormatadorData.data_para_str(self.data_fim)
                    periodo += f" até {data_fim_str} {self.hora_fim}"
        elif self.hora_inicio:
            periodo = f" | Horário: {self.hora_inicio}"
        
        return f"[{self.id}] {self.nome} | Facilitador: {self.facilitador} | Local: {self.local}{periodo} | Vagas: {self.vagas}"
    
    def hora_inicio_formatada(self):
        if isinstance(self.hora_inicio, str):
            return self.hora_inicio
        return FormatadorData.hora_para_str(self.hora_inicio)
    
    def hora_fim_formatada(self):
        if isinstance(self.hora_fim, str):
            return self.hora_fim
        return FormatadorData.hora_para_str(self.hora_fim)
    
    def data_inicio_formatada(self):
        return FormatadorData.data_para_str(self.data_inicio) if self.data_inicio else ""
    
    def data_fim_formatada(self):
        return FormatadorData.data_para_str(self.data_fim) if self.data_fim else ""
    
    def periodo_formatado(self):
        if not self.data_inicio or not self.hora_inicio:
            return f"Horário: {self.hora_inicio}" if self.hora_inicio else "Horário não definido"
        
        if self.data_inicio == self.data_fim or not self.data_fim:
            return f"{self.data_inicio_formatada()} das {self.hora_inicio_formatada()} às {self.hora_fim_formatada() if self.hora_fim else 'não definido'}"
        else:
            return f"De {self.data_inicio_formatada()} às {self.hora_inicio_formatada()} até {self.data_fim_formatada()} às {self.hora_fim_formatada()}"
    
    @property
    def duracao(self):
        if all([self.data_inicio, self.hora_inicio, self.data_fim, self.hora_fim]):
            try:
                inicio_time = FormatadorData.str_para_hora(self.hora_inicio) if isinstance(self.hora_inicio, str) else self.hora_inicio
                fim_time = FormatadorData.str_para_hora(self.hora_fim) if isinstance(self.hora_fim, str) else self.hora_fim
                
                inicio = datetime.combine(self.data_inicio, inicio_time)
                fim = datetime.combine(self.data_fim, fim_time)
                return (fim - inicio).total_seconds() / 3600
            except (TypeError, ValueError):
                return None
        return None
    
    def dados_formatados(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'facilitador': self.facilitador,
            'local': self.local,
            'id_evento': self.id_evento,
            'data_inicio': self.data_inicio_formatada(),
            'hora_inicio': self.hora_inicio_formatada(),
            'data_fim': self.data_fim_formatada(),
            'hora_fim': self.hora_fim_formatada(),
            'vagas': self.vagas
        }
