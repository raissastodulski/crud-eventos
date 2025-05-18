class Evento:
    def __init__(self, titulo="", descricao="", data="", local="", id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.local = local
    
    def para_tupla(self):
        """Converte evento para tupla para operações de banco de dados (sem ID)"""
        return (self.titulo, self.descricao, self.data, self.local)
    
    def para_tupla_com_id(self):
        """Converte evento para tupla para operações de banco de dados (com ID)"""
        return (self.titulo, self.descricao, self.data, self.local, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        """Cria um objeto Evento a partir de uma tupla do banco de dados"""
        id, titulo, descricao, data, local = dados
        return cls(titulo=titulo, descricao=descricao, data=data, local=local, id=id)
    
    def __str__(self):
        """Representação em string do evento"""
        data_str = f" | {self.data}" if self.data else ""
        local_str = f" | {self.local}" if self.local else ""
        return f"[{self.id}] {self.titulo}{data_str}{local_str}"