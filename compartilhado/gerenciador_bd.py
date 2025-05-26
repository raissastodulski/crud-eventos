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
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eventos'")
        tabela_existe = self.cursor.fetchone()
        
        if tabela_existe:
            self.cursor.execute("PRAGMA table_info(eventos)")
            colunas = {coluna[1]: coluna[2] for coluna in self.cursor.fetchall()}
            
            if 'titulo' in colunas or 'local' in colunas or 'data' in colunas:
                print("Migrando tabela eventos para nova estrutura...")
                self._migrar_tabela_eventos()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_inicio DATE,
            hora_inicio TIME,
            data_fim DATE,
            hora_fim TIME,
            publico_alvo TEXT,
            tipo TEXT,
            endereco TEXT,
            capacidade INTEGER
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            email TEXT,
            telefone TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            facilitador TEXT,
            local TEXT,
            id_evento INTEGER,
            hora_inicio TIME,
            vagas INTEGER,
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        )
        ''')
        
        self.cursor.execute("PRAGMA table_info(inscricoes)")
        colunas = [coluna[1] for coluna in self.cursor.fetchall()]
        
        if 'id_evento' in colunas and 'id_atividade' not in colunas:
            print("Migrando tabela de inscrições para novo formato...")
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscricoes_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_participante INTEGER,
                id_atividade INTEGER,
                data_inscricao DATETIME,
                FOREIGN KEY (id_participante) REFERENCES participantes (id),
                FOREIGN KEY (id_atividade) REFERENCES atividades (id)
            )
            ''')
            
            try:
                self.cursor.execute('''
                INSERT INTO inscricoes_temp (id_participante, id_atividade, data_inscricao)
                SELECT i.id_participante, 
                       (SELECT MIN(a.id) FROM atividades a WHERE a.id_evento = i.id_evento), 
                       datetime('now', 'localtime')
                FROM inscricoes i
                WHERE EXISTS (SELECT 1 FROM atividades a WHERE a.id_evento = i.id_evento)
                ''')
                
                self.conn.commit()
                
                self.cursor.execute("DROP TABLE inscricoes")
                
                self.cursor.execute("ALTER TABLE inscricoes_temp RENAME TO inscricoes")
                
                print("Migração concluída com sucesso!")
            except sqlite3.Error as e:
                print(f"Erro durante a migração: {e}")
                self.cursor.execute("DROP TABLE IF EXISTS inscricoes_temp")
        elif not colunas:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscricoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_participante INTEGER,
                id_atividade INTEGER,
                data_inscricao DATETIME,
                FOREIGN KEY (id_participante) REFERENCES participantes (id),
                FOREIGN KEY (id_atividade) REFERENCES atividades (id)
            )
            ''')
        elif 'id_atividade' in colunas and 'data_inscricao' not in colunas:
            self.cursor.execute("ALTER TABLE inscricoes ADD COLUMN data_inscricao DATETIME")
        
        self.conn.commit()
    
    def _migrar_tabela_eventos(self):
        try:
            self.cursor.execute('''
            CREATE TABLE eventos_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                data_inicio DATE,
                hora_inicio TIME,
                data_fim DATE,
                hora_fim TIME,
                publico_alvo TEXT,
                tipo TEXT,
                endereco TEXT,
                capacidade INTEGER
            )
            ''')
            
            self.cursor.execute("PRAGMA table_info(eventos)")
            colunas_existentes = [coluna[1] for coluna in self.cursor.fetchall()]
            
            nome_col = 'titulo' if 'titulo' in colunas_existentes else 'nome'
            data_col = 'data' if 'data' in colunas_existentes else 'data_inicio'
            endereco_col = 'endereco' if 'endereco' in colunas_existentes else 'local'
            
            select_fields = [
                f'{nome_col} as nome',
                'descricao' if 'descricao' in colunas_existentes else 'NULL as descricao',
                f'{data_col} as data_inicio',
                'hora_inicio' if 'hora_inicio' in colunas_existentes else 'NULL as hora_inicio',
                f'{data_col} as data_fim',
                'hora_fim' if 'hora_fim' in colunas_existentes else 'NULL as hora_fim',
                'publico_alvo' if 'publico_alvo' in colunas_existentes else 'NULL as publico_alvo',
                'NULL as tipo',
                f'{endereco_col} as endereco',
                'capacidade' if 'capacidade' in colunas_existentes else 'NULL as capacidade'
            ]
            
            query = f"INSERT INTO eventos_temp (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, publico_alvo, tipo, endereco, capacidade) SELECT {', '.join(select_fields)} FROM eventos"
            self.cursor.execute(query)
            
            self.cursor.execute("DROP TABLE eventos")
            self.cursor.execute("ALTER TABLE eventos_temp RENAME TO eventos")
            
            self.conn.commit()
            print("Migração da tabela eventos concluída com sucesso!")
            
        except sqlite3.Error as e:
            print(f"Erro durante migração da tabela eventos: {e}")
            try:
                self.cursor.execute("DROP TABLE IF EXISTS eventos_temp")
            except:
                pass
    
    def fechar(self):
        if self.conn:
            self.conn.close()
            print("Conexão com banco de dados encerrada.")
