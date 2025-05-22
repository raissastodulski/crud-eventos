import sqlite3

class GerenciadorBD:
    def __init__(self, nome_bd="crud-eventos.db"):
        self.nome_bd = nome_bd
        self.conn = None
        self.cursor = None
        self.inicializar()
    
    def inicializar(self):
        try:
            self.conn = sqlite3.connect(self.nome_bd)
            self.cursor = self.conn.cursor()
            self.criar_tabelas()
            print(f"Conexão com banco de dados estabelecida: {self.nome_bd}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
    
    def criar_tabelas(self):
        # Tabela eventos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data TEXT,
            hora_inicio TEXT,
            hora_fim TEXT,
            publico_alvo TEXT,
            capacidade INTEGER,
            local TEXT,
            endereco TEXT
        )
        ''')
        
        # Tabela participantes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            email TEXT,
            telefone TEXT,
            data TEXT
        )
        ''')
        
        # Tabela atividades
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            facilitador TEXT,
            id_evento INTEGER,
            hora_inicio TEXT,
            vagas INTEGER,
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        )
        ''')
        
        # Tabela inscrições
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_participante INTEGER,
            id_evento INTEGER,
            FOREIGN KEY (id_participante) REFERENCES participantes (id),
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        )
        ''')
        
        self.conn.commit()
    
    def fechar(self):
        if self.conn:
            self.conn.close()
            print("Conexão com banco de dados encerrada.")
