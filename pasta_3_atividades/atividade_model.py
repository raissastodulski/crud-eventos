from compartilhado.formatador_data import FormatadorData

class Atividade:
    def __init__(
        self, nome="", facilitador="", local="", id_evento=None, hora_inicio="", vagas=0, id=None
    ):
        self.id = id
        self.nome = nome
        self.facilitador = facilitador
        self.local = local
        self.id_evento = id_evento
        self.hora_inicio = hora_inicio
        self.vagas = vagas

    def para_tupla(self):
        return (
            self.nome,
            self.facilitador,
            self.local,
            self.id_evento,
            self.hora_inicio,
            self.vagas,
        )

    def para_tupla_com_id(self):
        return (
            self.nome,
            self.facilitador,
            self.local,
            self.id_evento,
            self.hora_inicio,
            self.vagas,
            self.id,
        )

    @classmethod
    def de_tupla(cls, dados):
        id, nome, facilitador, local, id_evento, hora_inicio, vagas = dados
        return cls(
            nome=nome,
            facilitador=facilitador,
            local=local,
            id_evento=id_evento,
            hora_inicio=hora_inicio,
            vagas=vagas,
            id=id,
        )

    def __str__(self):
        return f"[{self.id}] {self.nome} | Facilitador: {self.facilitador} | Local: {self.local} | Horário: {self.hora_inicio} | Vagas: {self.vagas}"
    
    def hora_inicio_formatada(self):
        """Retorna hora de início formatada em hh:mm"""
        return FormatadorData.hora_para_str(self.hora_inicio)
    
    def dados_formatados(self):
        """Retorna dados formatados para exibição"""
        return {
            'id': self.id,
            'nome': self.nome,
            'facilitador': self.facilitador,
            'local': self.local,
            'id_evento': self.id_evento,
            'hora_inicio': self.hora_inicio_formatada(),
            'vagas': self.vagas
        }
