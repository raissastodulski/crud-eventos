class Inscricao:
    def __init__(self, id_participante=None, id_evento=None, id=None):
        self.id = id
        self.id_participante = id_participante
        self.id_evento = id_evento
    
    def para_tupla(self):
        """Converte inscrição para tupla para operações de banco de dados (sem ID)"""
        return (self.id_participante, self.id_evento)
    
    def para_tupla_com_id(self):
        """Converte inscrição para tupla para operações de banco de dados (com ID)"""
        return (self.id_participante, self.id_evento, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um objeto Inscricao a partir de uma tupla do banco de dados"""
        id, id_participante, id_evento = dados
        return cls(id_participante=id_participante, id_evento=id_evento, id=id)
    
    def __str__(self):
        """Representação em string da inscrição"""
        return f"[{self.id}] Participante ID: {self.id_participante} | Evento ID: {self.id_evento}"
