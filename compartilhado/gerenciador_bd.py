import sqlite3
import os

class GerenciadorBD:
    def __init__(self, nome_bd="crud-eventos.db"):
        self.nome_bd = nome_bd
        self.conn = None
        self.cursor = None
        self.inicializar()
    
    def inicializar(self):
        try:
            print(f"Tentando conectar ao banco: {self.nome_bd}")
            
            diretorio = os.path.dirname(self.nome_bd)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio)
                print(f"Diretório criado: {diretorio}")
            
            self.conn = sqlite3.connect(self.nome_bd, check_same_thread=False)
            if self.conn is None:
                raise Exception("Falha ao conectar com o banco de dados")
                
            self.cursor = self.conn.cursor()
            if self.cursor is None:
                raise Exception("Falha ao criar cursor do banco de dados")
            
            self.cursor.execute("SELECT 1")
            resultado = self.cursor.fetchone()
            if resultado is None:
                raise Exception("Falha no teste de conexão")
                
            self.criar_tabelas()
            print(f"✅ Conexão com banco de dados estabelecida: {self.nome_bd}")
            
        except sqlite3.Error as e:
            print(f"❌ Erro SQLite: {e}")
            self._limpar_conexao()
        except Exception as e:
            print(f"❌ Erro geral na inicialização: {e}")
            self._limpar_conexao()
    
    def _limpar_conexao(self):
        try:
            if self.cursor:
                self.cursor.close()
        except:
            pass
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
        self.conn = None
        self.cursor = None
    
    def criar_tabelas(self):
        try:
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
                local TEXT,
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
                telefone TEXT,
                data_nascimento DATETIME
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                facilitador TEXT,
                local TEXT,
                id_evento INTEGER,
                data_inicio DATE,
                hora_inicio TIME,
                data_fim DATE,
                hora_fim TIME,
                vagas INTEGER,
                FOREIGN KEY (id_evento) REFERENCES eventos (id)
            )
            ''')
            
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
            
            self.conn.commit()
            print("✅ Tabelas criadas/verificadas com sucesso")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            if self.conn:
                try:
                    self.conn.rollback()
                except:
                    pass
    
    def fechar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("✅ Conexão com banco de dados encerrada.")
        except Exception as e:
            print(f"⚠️  Erro ao fechar conexão: {e}")
        finally:
            self.conn = None
            self.cursor = None
