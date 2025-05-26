from datetime import datetime
from compartilhado.formatador_data import FormatadorData

class Participante:
    def __init__(self, nome="", cpf="", email="", telefone="", data_nascimento=None, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
    
    def para_tupla(self):
        data_nascimento_str = None
        if self.data_nascimento:
            if isinstance(self.data_nascimento, datetime):
                data_nascimento_str = self.data_nascimento.strftime('%Y-%m-%d %H:%M:%S')
            elif hasattr(self.data_nascimento, 'isoformat'):
                data_nascimento_str = self.data_nascimento.isoformat()
            else:
                data_nascimento_str = str(self.data_nascimento)
        
        return (self.nome, self.cpf, self.email, self.telefone, data_nascimento_str)
    
    def para_tupla_com_id(self):
        data_nascimento_str = None
        if self.data_nascimento:
            if isinstance(self.data_nascimento, datetime):
                data_nascimento_str = self.data_nascimento.strftime('%Y-%m-%d %H:%M:%S')
            elif hasattr(self.data_nascimento, 'isoformat'):
                data_nascimento_str = self.data_nascimento.isoformat()
            else:
                data_nascimento_str = str(self.data_nascimento)
        
        return (self.nome, self.cpf, self.email, self.telefone, data_nascimento_str, self.id)
    
    @classmethod
    def de_tupla(cls, dados):
        if len(dados) == 5:  # Old format without data_nascimento
            id, nome, cpf, email, telefone = dados
            return cls(nome=nome, cpf=cpf, email=email, telefone=telefone, id=id)
        elif len(dados) >= 6:  # New format with data_nascimento
            id, nome, cpf, email, telefone, data_nascimento = dados[:6]
            
            # Parse data_nascimento if it exists
            data_nascimento_parsed = None
            if data_nascimento:
                try:
                    if isinstance(data_nascimento, str):
                        # Try different date formats
                        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
                            try:
                                data_nascimento_parsed = datetime.strptime(data_nascimento, fmt)
                                break
                            except ValueError:
                                continue
                    elif isinstance(data_nascimento, datetime):
                        data_nascimento_parsed = data_nascimento
                except (ValueError, TypeError):
                    data_nascimento_parsed = None
            
            return cls(nome=nome, cpf=cpf, email=email, telefone=telefone, 
                      data_nascimento=data_nascimento_parsed, id=id)
        else:
            raise ValueError(f"Formato de dados inválido: {dados}")

    def __str__(self):
        data_nascimento_str = ""
        if self.data_nascimento:
            if isinstance(self.data_nascimento, datetime):
                data_nascimento_str = f" | Nascimento: {self.data_nascimento.strftime('%d/%m/%Y')}"
            else:
                data_nascimento_str = f" | Nascimento: {self.data_nascimento}"
        
        return f"[{self.id}] {self.nome} | CPF: {self.cpf} | Email: {self.email}{data_nascimento_str}"
    
    def dados_formatados(self):
        data_nascimento_formatada = None
        if self.data_nascimento:
            if isinstance(self.data_nascimento, datetime):
                data_nascimento_formatada = self.data_nascimento.strftime('%d/%m/%Y')
            else:
                data_nascimento_formatada = str(self.data_nascimento)
        
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'data_nascimento': data_nascimento_formatada
        }
