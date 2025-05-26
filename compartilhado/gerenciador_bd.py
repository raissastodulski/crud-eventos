import sqlite3
import os

class GerenciadorBD:
    def __init__(self, caminho_bd=None):
        # Se caminho_bd for um diretório, adiciona o nome do arquivo
        if caminho_bd and os.path.isdir(caminho_bd):
            self.nome_bd = os.path.join(caminho_bd, "crud-eventos.db")
        elif caminho_bd:
            self.nome_bd = caminho_bd
        else:
            self.nome_bd = "crud-eventos.db"
            
        self.conn = None
        self.cursor = None
        self.inicializar()
    
    def inicializar(self):
        try:
            print(f"Tentando conectar ao banco: {self.nome_bd}")
            
            # Verificar se o diretório existe
            diretorio = os.path.dirname(self.nome_bd)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio)
                print(f"Diretório criado: {diretorio}")
            
            # Conectar ao banco
            self.conn = sqlite3.connect(self.nome_bd, check_same_thread=False)
            if self.conn is None:
                raise Exception("Falha ao conectar com o banco de dados")
                
            self.cursor = self.conn.cursor()
            if self.cursor is None:
                raise Exception("Falha ao criar cursor do banco de dados")
            
            # Testar a conexão
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
        """Limpa as conexões em caso de erro"""
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
    
    def verificar_conexao(self):
        """Verifica e restabelece a conexão se necessário"""
        try:
            if self.conn is None or self.cursor is None:
                print("⚠️  Conexão perdida. Tentando reconectar...")
                self.inicializar()
                return self.conn is not None and self.cursor is not None
            
            # Testar se a conexão ainda está ativa
            self.cursor.execute("SELECT 1")
            return True
            
        except sqlite3.Error:
            print("⚠️  Conexão com problemas. Tentando reconectar...")
            self.inicializar()
            return self.conn is not None and self.cursor is not None
        except Exception:
            print("⚠️  Erro na verificação de conexão. Tentando reconectar...")
            self.inicializar()
            return self.conn is not None and self.cursor is not None
    
    def executar_com_retry(self, funcao):
        """Executa uma função com retry em caso de erro de conexão"""
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            try:
                if not self.verificar_conexao():
                    if tentativa == max_tentativas - 1:
                        raise Exception("Não foi possível estabelecer conexão com o banco")
                    continue
                    
                return funcao()
                
            except sqlite3.Error as e:
                print(f"❌ Erro SQLite (tentativa {tentativa + 1}): {e}")
                if tentativa == max_tentativas - 1:
                    raise
                self.inicializar()
            except Exception as e:
                print(f"❌ Erro geral (tentativa {tentativa + 1}): {e}")
                if tentativa == max_tentativas - 1:
                    raise
        
        raise Exception("Máximo de tentativas excedido")
    
    def criar_tabelas(self):
        def _criar_tabelas_interno():
            if not self.verificar_conexao():
                raise Exception("Conexão com banco não disponível para criar tabelas")
                
            # Verificar se a tabela eventos existe e sua estrutura
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eventos'")
            tabela_existe = self.cursor.fetchone()
            
            if tabela_existe:
                self.cursor.execute("PRAGMA table_info(eventos)")
                colunas = {coluna[1]: coluna[2] for coluna in self.cursor.fetchall()}
                
                if 'endereco' in colunas and 'local' not in colunas:
                    print("Migrando tabela eventos para nova estrutura...")
                    self._migrar_tabela_eventos()
            
            # Criar tabela eventos
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
            
            # Verificar e migrar tabela participantes se necessário
            self.cursor.execute("PRAGMA table_info(participantes)")
            colunas_participantes = [coluna[1] for coluna in self.cursor.fetchall()]
            
            if colunas_participantes and 'data_nascimento' not in colunas_participantes:
                print("Adicionando coluna data_nascimento à tabela participantes...")
                try:
                    self.cursor.execute("ALTER TABLE participantes ADD COLUMN data_nascimento DATETIME")
                    if 'data' in colunas_participantes:
                        self._migrar_participantes_remove_data()
                except sqlite3.Error as e:
                    print(f"Erro ao adicionar coluna data_nascimento: {e}")
            
            # Criar tabela participantes
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
            
            # Verificar e migrar tabela atividades se necessário
            self.cursor.execute("PRAGMA table_info(atividades)")
            colunas_atividades = [coluna[1] for coluna in self.cursor.fetchall()]
            
            if colunas_atividades and ('data_inicio' not in colunas_atividades or 'data_fim' not in colunas_atividades or 'hora_fim' not in colunas_atividades):
                print("Migrando tabela atividades para nova estrutura...")
                self._migrar_tabela_atividades()
            
            # Criar tabela atividades
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
            
            # Verificar e migrar tabela inscrições se necessário
            self.cursor.execute("PRAGMA table_info(inscricoes)")
            colunas = [coluna[1] for coluna in self.cursor.fetchall()]
            
            if 'id_evento' in colunas and 'id_atividade' not in colunas:
                print("Migrando tabela de inscrições para novo formato...")
                self._migrar_inscricoes()
            elif not colunas:
                # Criar tabela inscrições
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
            print("✅ Tabelas criadas/verificadas com sucesso")
        
        try:
            self.executar_com_retry(_criar_tabelas_interno)
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            if self.conn:
                try:
                    self.conn.rollback()
                except:
                    pass
    
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
                local TEXT,
                endereco TEXT,
                capacidade INTEGER
            )
            ''')
            
            self.cursor.execute('''
            INSERT INTO eventos_temp (id, nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, publico_alvo, local, endereco, capacidade)
            SELECT id, nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, publico_alvo, endereco, endereco, capacidade
            FROM eventos
            ''')
            
            self.cursor.execute("DROP TABLE eventos")
            self.cursor.execute("ALTER TABLE eventos_temp RENAME TO eventos")
            
            self.conn.commit()
            print("✅ Migração da tabela eventos concluída com sucesso!")
            
        except sqlite3.Error as e:
            print(f"❌ Erro durante migração da tabela eventos: {e}")
            try:
                self.cursor.execute("DROP TABLE IF EXISTS eventos_temp")
            except:
                pass
    
    def _migrar_participantes_remove_data(self):
        try:
            self.cursor.execute('''
            CREATE TABLE participantes_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cpf TEXT,
                email TEXT,
                telefone TEXT,
                data_nascimento DATETIME
            )
            ''')
            
            self.cursor.execute('''
            INSERT INTO participantes_temp (id, nome, cpf, email, telefone)
            SELECT id, nome, cpf, email, telefone
            FROM participantes
            ''')
            
            self.cursor.execute("DROP TABLE participantes")
            self.cursor.execute("ALTER TABLE participantes_temp RENAME TO participantes")
            
            self.conn.commit()
            print("✅ Migração da tabela participantes concluída com sucesso!")
            
        except sqlite3.Error as e:
            print(f"❌ Erro durante migração da tabela participantes: {e}")
            try:
                self.cursor.execute("DROP TABLE IF EXISTS participantes_temp")
            except:
                pass
    
    def _migrar_tabela_atividades(self):
        """Migrate atividades table to include data_inicio, data_fim, hora_fim"""
        try:
            self.cursor.execute('''
            CREATE TABLE atividades_temp (
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
            INSERT INTO atividades_temp (id, nome, facilitador, local, id_evento, data_inicio, hora_inicio, data_fim, hora_fim, vagas)
            SELECT a.id, a.nome, a.facilitador, a.local, a.id_evento, 
                   e.data_inicio, a.hora_inicio, e.data_fim, 
                   CASE WHEN a.hora_inicio IS NOT NULL 
                        THEN time(a.hora_inicio, '+1 hour') 
                        ELSE e.hora_fim 
                   END,
                   a.vagas
            FROM atividades a
            LEFT JOIN eventos e ON a.id_evento = e.id
            ''')
            
            self.cursor.execute("DROP TABLE atividades")
            self.cursor.execute("ALTER TABLE atividades_temp RENAME TO atividades")
            
            self.conn.commit()
            print("✅ Migração da tabela atividades concluída com sucesso!")
            
        except sqlite3.Error as e:
            print(f"❌ Erro durante migração da tabela atividades: {e}")
            try:
                self.cursor.execute("DROP TABLE IF EXISTS atividades_temp")
            except:
                pass
    
    def _migrar_inscricoes(self):
        """Migrar tabela de inscrições para novo formato"""
        try:
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
            
            print("✅ Migração de inscrições concluída com sucesso!")
        except sqlite3.Error as e:
            print(f"❌ Erro durante a migração de inscrições: {e}")
            self.cursor.execute("DROP TABLE IF EXISTS inscricoes_temp")
    
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
