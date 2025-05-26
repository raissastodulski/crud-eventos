from utils import FormatadorData

class Inscricao:
    def __init__(self, id_participante=None, id_atividade=None, id=None, data_inscricao=None):
        self.id = id
        self.id_participante = id_participante
        self.id_atividade = id_atividade
        
        if not data_inscricao:
            self.data_inscricao = FormatadorData.data_hora_inscricao_agora()
        else:
            self.data_inscricao = data_inscricao
    
    def para_tupla(self):
        return (self.id_participante, self.id_atividade, self.data_inscricao)
    
    def para_tupla_com_id(self):
        return (self.id_participante, self.id_atividade, self.data_inscricao, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        id, id_participante, id_atividade, data_inscricao = dados
        return cls(id_participante=id_participante, id_atividade=id_atividade, 
                   data_inscricao=data_inscricao, id=id)