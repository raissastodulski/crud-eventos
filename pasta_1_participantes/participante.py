class Participante:
    def __init__(self, nome="", cpf="", email="", telefone="", id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
    
    def para_tupla(self):
        return (self.nome, self.cpf, self.email, self.telefone)
    
    def para_tupla_com_id(self):
        return (self.nome, self.cpf, self.email, self.telefone, self.id)
    
    @classmethod
    def de_tupla(cls):
        id, nome, cpf, email, telefone = dados
        return cls(nome=nome, cpf=cpf, email=email, telefone=telefone, id=id)

    def __str__(self):
        return f"[{self.id}] {self.nome} | CPF: {self.cpf} | Email: {self.email}"
    
    def dados_formatados(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone
        }
