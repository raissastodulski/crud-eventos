import sqlite3
from pasta_0_modelos.evento import Evento

class GerenciadorBD:
    def __init__(self, nome_bd="eventos.db"):
        self.nome_bd = nome_bd
        self.conn = None
        self.cursor = None
        self.inicializar()
    
    def inicializar(self):
        """Inicializa a conexão com o banco de dados e cria tabelas se não existirem"""
        try:
            self.conn = sqlite3.connect(self.nome_bd)
            self.cursor = self.conn.cursor()
            self.criar_tabelas()
            print(f"Conexão com banco de dados estabelecida: {self.nome_bd}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
    
    def criar_tabelas(self):
        """Cria a tabela de eventos se não existir"""
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
        );
        
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            email TEXT,
            telefone TEXT,
            data TEXT
        );
        
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            facilitador TEXT,
            id_evento INTEGER,
            hora_inicio TEXT,
            vagas INTEGER,
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        );
                            
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_participante INTEGER,
            id_evento INTEGER,
            FOREIGN KEY (id_participante) REFERENCES participantes (id),
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        );
        ''')
        self.conn.commit()
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("Conexão com banco de dados encerrada.")
    
    # Operações CRUD
    
    def criar_evento(self, evento):
        """Adiciona um novo evento ao banco de dados"""
        try:
            self.cursor.execute('''
            INSERT INTO eventos (titulo, descricao, data, local)
            VALUES (?, ?, ?, ?)
            ''', evento.para_tupla())
            self.conn.commit()
            print(f"Evento '{evento.titulo}' adicionado com sucesso.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar evento: {e}")
            return None
    
    def ler_todos_eventos(self):
        """Recupera todos os eventos do banco de dados"""
        try:
            self.cursor.execute("SELECT * FROM eventos")
            eventos = []
            for dados_evento in self.cursor.fetchall():
                eventos.append(Evento.de_tupla(dados_evento))
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao recuperar eventos: {e}")
            return []
    
    def ler_evento_por_id(self, id_evento):
        """Recupera um único evento pelo ID"""
        try:
            self.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
            dados_evento = self.cursor.fetchone()
            if dados_evento:
                return Evento.de_tupla(dados_evento)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar evento: {e}")
            return None
    
    def atualizar_evento(self, evento):
        """Atualiza um evento existente"""
        try:
            self.cursor.execute('''
            UPDATE eventos
            SET titulo=?, descricao=?, data=?, local=?
            WHERE id=?
            ''', evento.para_tupla_com_id())
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Evento '{evento.titulo}' atualizado com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {evento.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar evento: {e}")
            return False
    
    def deletar_evento(self, id_evento):
        """Exclui um evento pelo ID"""
        try:
            self.cursor.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Evento com ID {id_evento} excluído com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir evento: {e}")
            return False
    
    def buscar_eventos(self, termo_busca):
        """Busca eventos contendo o termo de busca no título ou descrição"""
        try:
            padrao_busca = f"%{termo_busca}%"
            self.cursor.execute("""
            SELECT * FROM eventos 
            WHERE titulo LIKE ? OR descricao LIKE ? OR local LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca))
            
            eventos = []
            for dados_evento in self.cursor.fetchall():
                eventos.append(Evento.de_tupla(dados_evento))
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao buscar eventos: {e}")
            return []