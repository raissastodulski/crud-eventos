class Atividade:
    def __init__(self, nome="", facilitador="", id_evento=None, hora_inicio="", vagas=0, id=None):
        self.id = id
        self.nome = nome
        self.facilitador = facilitador
        self.id_evento = id_evento
        self.hora_inicio = hora_inicio
        self.vagas = vagas
    
    def para_tupla(self):
        return (self.nome, self.facilitador, self.id_evento, self.hora_inicio, self.vagas)
    
    def para_tupla_com_id(self):
        return (self.nome, self.facilitador, self.id_evento, self.hora_inicio, self.vagas, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        id, nome, facilitador, id_evento, hora_inicio, vagas = dados
        return cls(nome=nome, facilitador=facilitador, id_evento=id_evento, 
                   hora_inicio=hora_inicio, vagas=vagas, id=id)
    
    def __str__(self):
        return f"[{self.id}] {self.nome} | Facilitador: {self.facilitador} | Horário: {self.hora_inicio} | Vagas: {self.vagas}"