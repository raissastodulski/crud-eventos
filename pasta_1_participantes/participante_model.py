class Participante:
    def __init__(self, nome="", cpf="", email="", telefone="", data="", id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data = data
    
    def para_tupla(self):
        """Converte participante para tupla para operações de banco de dados (sem ID)"""
        return (self.nome, self.cpf, self.email, self.telefone, self.data)
    
    def para_tupla_com_id(self):
        """Converte participante para tupla para operações de banco de dados (com ID)"""
        return (self.nome, self.cpf, self.email, self.telefone, self.data, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um objeto Participante a partir de uma tupla do banco de dados"""
        id, nome, cpf, email, telefone, data = dados
        return cls(nome=nome, cpf=cpf, email=email, telefone=telefone, data=data, id=id)
    
    def __str__(self):
        """Representação em string do participante"""
        return f"[{self.id}] {self.nome} | CPF: {self.cpf} | Email: {self.email}"