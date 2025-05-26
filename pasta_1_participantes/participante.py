from compartilhado.formatador_data import FormatadorData

class Participante:
    def __init__(self, nome="", cpf="", email="", telefone="", data="", id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        
        if not data:
            self.data = FormatadorData.data_cadastro_hoje()
        else:
            self.data = data
    
    def para_tupla(self):
        return (self.nome, self.cpf, self.email, self.telefone, self.data)
    
    def para_tupla_com_id(self):
        return (self.nome, self.cpf, self.email, self.telefone, self.data, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        id, nome, cpf, email, telefone, data = dados
        return cls(nome=nome, cpf=cpf, email=email, telefone=telefone, data=data, id=id)
    
    def __str__(self):
        return f"[{self.id}] {self.nome} | CPF: {self.cpf} | Email: {self.email} | Cadastrado em: {self.data}"
    
    def dados_formatados(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data
        }
