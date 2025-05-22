import datetime

class Activity:
    def __init__(self, id=None, nome=None, facilitador=None, horario= None,
                 local = None, vagas = None):
        self.id = id
        self.nome = nome
        self.facilitador = facilitador
        self.horario = horario
        self.local = local
        self.vagas =vagas
    
    def __str__(self):
        return (
            f"Atividade: {self.nome}\n"
            f"ID: {self.id}\n"
            f"Facilitador: {self.facilitador}\n"
            f"Horário: {self.horario}\n"
            f"Local: {self.local}\n"
            f"Vagas: {self.vagas}\n"
        )
    
    def to_tuple(self):
        """Convert the event object to a tuple for database operations"""
        return (
            self.nome, 
            self.facilitador, 
            self.horario, 
            self.local, 
            self.vagas,
        )
    
    def to_tuple_with_id(self):
        """Convert the event object to a tuple including the ID for database operations"""
        return (
            self.id,
            self.nome, 
            self.facilitador, 
            self.horario, 
            self.local,
            self.vagas, 
            
        )
    
    @staticmethod
    def from_tuple(tuple_data):
        """Create an Event object from a database tuple"""
        return Activity(
            id=tuple_data[0],
            nome = tuple_data[1],
            facilitador= tuple_data[2],
            horario = tuple_data[3],
            local = tuple_data[4],
            vagas = tuple_data[5],
            
        )