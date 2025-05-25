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
        # Verificar se precisa migrar a tabela eventos
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eventos'")
        tabela_existe = self.cursor.fetchone()
        
        if tabela_existe:
            # Verificar estrutura atual da tabela
            self.cursor.execute("PRAGMA table_info(eventos)")
            colunas = {coluna[1]: coluna[2] for coluna in self.cursor.fetchall()}
            
            # Se a tabela tem estrutura antiga, migrar
            if 'titulo' in colunas or 'local' in colunas or 'data' in colunas:
                print("Migrando tabela eventos para nova estrutura...")
                self._migrar_tabela_eventos()
        
        # Criar/atualizar tabela eventos com nova estrutura
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_inicio TEXT,
            hora_inicio TEXT,
            data_fim TEXT,
            hora_fim TEXT,
            publico_alvo TEXT,
            tipo TEXT,
            endereco TEXT,
            capacidade INTEGER
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
        
        # Verificar se a tabela inscricoes existe e se precisa ser migrada
        self.cursor.execute("PRAGMA table_info(inscricoes)")
        colunas = [coluna[1] for coluna in self.cursor.fetchall()]
        
        if 'id_evento' in colunas and 'id_atividade' not in colunas:
            # Migrar dados da tabela de inscrições existente
            print("Migrando tabela de inscrições para novo formato...")
            
            # Criar tabela temporária com a nova estrutura
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscricoes_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_participante INTEGER,
                id_atividade INTEGER,
                data_inscricao TEXT,
                FOREIGN KEY (id_participante) REFERENCES participantes (id),
                FOREIGN KEY (id_atividade) REFERENCES atividades (id)
            )
            ''')
            
            try:
                # Migrar dados existentes para a tabela temporária
                # Este processo básico seleciona a primeira atividade de cada evento para inscrição
                self.cursor.execute('''
                INSERT INTO inscricoes_temp (id_participante, id_atividade, data_inscricao)
                SELECT i.id_participante, 
                       (SELECT MIN(a.id) FROM atividades a WHERE a.id_evento = i.id_evento), 
                       datetime('now')
                FROM inscricoes i
                WHERE EXISTS (SELECT 1 FROM atividades a WHERE a.id_evento = i.id_evento)
                ''')
                
                self.conn.commit()
                
                # Remover tabela antiga
                self.cursor.execute("DROP TABLE inscricoes")
                
                # Renomear tabela temporária
                self.cursor.execute("ALTER TABLE inscricoes_temp RENAME TO inscricoes")
                
                print("Migração concluída com sucesso!")
            except sqlite3.Error as e:
                print(f"Erro durante a migração: {e}")
                # Se houver erro, manter a tabela antiga
                self.cursor.execute("DROP TABLE IF EXISTS inscricoes_temp")
        elif not colunas:
            # Se a tabela não existir, criar no novo formato
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscricoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_participante INTEGER,
                id_atividade INTEGER,
                data_inscricao TEXT,
                FOREIGN KEY (id_participante) REFERENCES participantes (id),
                FOREIGN KEY (id_atividade) REFERENCES atividades (id)
            )
            ''')
        elif 'id_atividade' in colunas and 'data_inscricao' not in colunas:
            # Se a tabela já tiver id_atividade mas não tiver data_inscricao, adicionar a coluna
            self.cursor.execute("ALTER TABLE inscricoes ADD COLUMN data_inscricao TEXT")
        
        self.conn.commit()
    
    def _migrar_tabela_eventos(self):
        """Migra a tabela eventos da estrutura antiga para a nova"""
        try:
            # Criar tabela temporária com nova estrutura
            self.cursor.execute('''
            CREATE TABLE eventos_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                data_inicio TEXT,
                hora_inicio TEXT,
                data_fim TEXT,
                hora_fim TEXT,
                publico_alvo TEXT,
                tipo TEXT,
                endereco TEXT,
                capacidade INTEGER
            )
            ''')
            
            # Verificar quais colunas existem na tabela atual
            self.cursor.execute("PRAGMA table_info(eventos)")
            colunas_existentes = [coluna[1] for coluna in self.cursor.fetchall()]
            
            # Migrar dados da tabela antiga para a nova
            nome_col = 'titulo' if 'titulo' in colunas_existentes else 'nome'
            data_col = 'data' if 'data' in colunas_existentes else 'data_inicio'
            endereco_col = 'endereco' if 'endereco' in colunas_existentes else 'local'
            
            # Construir query de migração baseada nas colunas disponíveis
            select_fields = [
                f'{nome_col} as nome',
                'descricao' if 'descricao' in colunas_existentes else 'NULL as descricao',
                f'{data_col} as data_inicio',
                'hora_inicio' if 'hora_inicio' in colunas_existentes else 'NULL as hora_inicio',
                f'{data_col} as data_fim',  # Usar mesma data para fim inicialmente
                'hora_fim' if 'hora_fim' in colunas_existentes else 'NULL as hora_fim',
                'publico_alvo' if 'publico_alvo' in colunas_existentes else 'NULL as publico_alvo',
                'NULL as tipo',  # Campo novo
                f'{endereco_col} as endereco',
                'capacidade' if 'capacidade' in colunas_existentes else 'NULL as capacidade'
            ]
            
            query = f"INSERT INTO eventos_temp (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, publico_alvo, tipo, endereco, capacidade) SELECT {', '.join(select_fields)} FROM eventos"
            self.cursor.execute(query)
            
            # Remover tabela antiga e renomear a nova
            self.cursor.execute("DROP TABLE eventos")
            self.cursor.execute("ALTER TABLE eventos_temp RENAME TO eventos")
            
            self.conn.commit()
            print("Migração da tabela eventos concluída com sucesso!")
            
        except sqlite3.Error as e:
            print(f"Erro durante migração da tabela eventos: {e}")
            # Em caso de erro, tentar limpar tabela temporária
            try:
                self.cursor.execute("DROP TABLE IF EXISTS eventos_temp")
            except:
                pass
    
    def fechar(self):
        if self.conn:
            self.conn.close()
            print("Conexão com banco de dados encerrada.")