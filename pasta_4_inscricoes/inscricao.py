from compartilhado.formatador_data import FormatadorData

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
    
    def __str__(self):
        return f"[{self.id}] Participante ID: {self.id_participante} | Atividade ID: {self.id_atividade} | Data: {self.data_inscricao}"
    
    def dados_formatados(self):
        return {
            'id': self.id,
            'id_participante': self.id_participante,
            'id_atividade': self.id_atividade,
            'data_inscricao': self.data_inscricao
        }
