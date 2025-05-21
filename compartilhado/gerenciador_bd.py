import sqlite3
from pasta_0_modelos.evento import Evento
from pasta_1_participantes.participante_model import Participante # Verify this path
from pasta_3_atividades.atividade_model import Atividade # Verify this path
from pasta_4_inscricoes.inscricao import Inscricao # Verify this path

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
        """Cria as tabelas se não existirem"""
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
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("Conexão com banco de dados encerrada.")
    
    # === CRUD EVENTOS ===
    
    def criar_evento(self, evento):
        """Adiciona um novo evento ao banco de dados"""
        try:
            self.cursor.execute('''
            INSERT INTO eventos (titulo, descricao, data, hora_inicio, hora_fim, 
                                publico_alvo, capacidade, local, endereco)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (evento.titulo, evento.descricao, evento.data, 
                 getattr(evento, 'hora_inicio', None), 
                 getattr(evento, 'hora_fim', None),
                 getattr(evento, 'publico_alvo', None), 
                 getattr(evento, 'capacidade', None),
                 evento.local, 
                 getattr(evento, 'endereco', None)))
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
                try:
                    if len(dados_evento) >= 10:  # Verifica se tem todos os campos necessários
                        evento = Evento(
                            titulo=dados_evento[1],
                            descricao=dados_evento[2],
                            data=dados_evento[3],
                            local=dados_evento[8],
                            id=dados_evento[0]
                        )
                        # Adiciona os outros atributos
                        evento.hora_inicio = dados_evento[4]
                        evento.hora_fim = dados_evento[5]
                        evento.publico_alvo = dados_evento[6]
                        evento.capacidade = dados_evento[7]
                        evento.endereco = dados_evento[9]
                        eventos.append(evento)
                    else:
                        print(f"Aviso: Registro de evento incompleto: {dados_evento}")
                except Exception as ex:
                    print(f"Erro ao processar evento: {ex}")
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
                evento = Evento(
                    titulo=dados_evento[1],
                    descricao=dados_evento[2],
                    data=dados_evento[3],
                    local=dados_evento[8],
                    id=dados_evento[0]
                )
                # Adiciona os outros atributos
                evento.hora_inicio = dados_evento[4]
                evento.hora_fim = dados_evento[5]
                evento.publico_alvo = dados_evento[6]
                evento.capacidade = dados_evento[7]
                evento.endereco = dados_evento[9]
                return evento
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar evento: {e}")
            return None
    
    def atualizar_evento(self, evento):
        """Atualiza um evento existente"""
        try:
            self.cursor.execute('''
            UPDATE eventos
            SET titulo=?, descricao=?, data=?, hora_inicio=?, hora_fim=?, 
                publico_alvo=?, capacidade=?, local=?, endereco=?
            WHERE id=?
            ''', (evento.titulo, evento.descricao, evento.data, 
                 getattr(evento, 'hora_inicio', None), 
                 getattr(evento, 'hora_fim', None),
                 getattr(evento, 'publico_alvo', None), 
                 getattr(evento, 'capacidade', None),
                 evento.local, 
                 getattr(evento, 'endereco', None),
                 evento.id))
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
                evento = Evento(
                    titulo=dados_evento[1],
                    descricao=dados_evento[2],
                    data=dados_evento[3],
                    local=dados_evento[8],
                    id=dados_evento[0]
                )
                # Adiciona os outros atributos
                evento.hora_inicio = dados_evento[4]
                evento.hora_fim = dados_evento[5]
                evento.publico_alvo = dados_evento[6]
                evento.capacidade = dados_evento[7]
                evento.endereco = dados_evento[9]
                eventos.append(evento)
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao buscar eventos: {e}")
            return []
    
    # === CRUD PARTICIPANTES ===
    
    def criar_participante(self, participante):
        """Adiciona um novo participante ao banco de dados"""
        try:
            self.cursor.execute('''
            INSERT INTO participantes (nome, cpf, email, telefone, data)
            VALUES (?, ?, ?, ?, ?)
            ''', participante.para_tupla())
            self.conn.commit()
            print(f"Participante '{participante.nome}' adicionado com sucesso.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar participante: {e}")
            return None
    
    def ler_todos_participantes(self):
        """Recupera todos os participantes do banco de dados"""
        try:
            self.cursor.execute("SELECT * FROM participantes")
            participantes = []
            for dados_participante in self.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar participantes: {e}")
            return []
    
    def ler_participante_por_id(self, id_participante):
        """Recupera um único participante pelo ID"""
        try:
            self.cursor.execute("SELECT * FROM participantes WHERE id=?", (id_participante,))
            dados_participante = self.cursor.fetchone()
            if dados_participante:
                return Participante.de_tupla(dados_participante)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar participante: {e}")
            return None
    
    def atualizar_participante(self, participante):
        """Atualiza um participante existente"""
        try:
            self.cursor.execute('''
            UPDATE participantes
            SET nome=?, cpf=?, email=?, telefone=?, data=?
            WHERE id=?
            ''', participante.para_tupla_com_id())
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Participante '{participante.nome}' atualizado com sucesso.")
                return True
            print(f"Nenhum participante encontrado com ID {participante.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar participante: {e}")
            return False
    
    def deletar_participante(self, id_participante):
        """Exclui um participante pelo ID"""
        try:
            self.cursor.execute("DELETE FROM participantes WHERE id=?", (id_participante,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Participante com ID {id_participante} excluído com sucesso.")
                return True
            print(f"Nenhum participante encontrado com ID {id_participante}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir participante: {e}")
            return False
    
    def buscar_participantes(self, termo_busca):
        """Busca participantes contendo o termo de busca no nome, email ou CPF"""
        try:
            padrao_busca = f"%{termo_busca}%"
            self.cursor.execute("""
            SELECT * FROM participantes 
            WHERE nome LIKE ? OR email LIKE ? OR cpf LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca))
            
            participantes = []
            for dados_participante in self.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao buscar participantes: {e}")
            return []
    
    # === CRUD ATIVIDADES ===
    
    def criar_atividade(self, atividade):
        """Adiciona uma nova atividade ao banco de dados"""
        try:
            self.cursor.execute('''
            INSERT INTO atividades (nome, facilitador, id_evento, hora_inicio, vagas)
            VALUES (?, ?, ?, ?, ?)
            ''', atividade.para_tupla())
            self.conn.commit()
            print(f"Atividade '{atividade.nome}' adicionada com sucesso.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar atividade: {e}")
            return None
    
    def ler_todas_atividades(self):
        """Recupera todas as atividades do banco de dados"""
        try:
            self.cursor.execute("SELECT * FROM atividades")
            atividades = []
            for dados_atividade in self.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividades: {e}")
            return []
    
    def ler_atividade_por_id(self, id_atividade):
        """Recupera uma única atividade pelo ID"""
        try:
            self.cursor.execute("SELECT * FROM atividades WHERE id=?", (id_atividade,))
            dados_atividade = self.cursor.fetchone()
            if dados_atividade:
                return Atividade.de_tupla(dados_atividade)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividade: {e}")
            return None
    
    def ler_atividades_por_evento(self, id_evento):
        """Recupera todas as atividades associadas a um evento"""
        try:
            self.cursor.execute("SELECT * FROM atividades WHERE id_evento=?", (id_evento,))
            atividades = []
            for dados_atividade in self.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividades do evento: {e}")
            return []
    
    def atualizar_atividade(self, atividade):
        """Atualiza uma atividade existente"""
        try:
            self.cursor.execute('''
            UPDATE atividades
            SET nome=?, facilitador=?, id_evento=?, hora_inicio=?, vagas=?
            WHERE id=?
            ''', atividade.para_tupla_com_id())
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Atividade '{atividade.nome}' atualizada com sucesso.")
                return True
            print(f"Nenhuma atividade encontrada com ID {atividade.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar atividade: {e}")
            return False
    
    def deletar_atividade(self, id_atividade):
        """Exclui uma atividade pelo ID"""
        try:
            self.cursor.execute("DELETE FROM atividades WHERE id=?", (id_atividade,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Atividade com ID {id_atividade} excluída com sucesso.")
                return True
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir atividade: {e}")
            return False
    
    # === CRUD INSCRIÇÕES ===
    
    def criar_inscricao(self, inscricao):
        """Adiciona uma nova inscrição ao banco de dados"""
        try:
            # Verifica se o participante já está inscrito no evento
            self.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (inscricao.id_participante, inscricao.id_evento))
            
            if self.cursor.fetchone():
                print(f"Participante ID {inscricao.id_participante} já está inscrito no evento ID {inscricao.id_evento}.")
                return None
            
            self.cursor.execute('''
            INSERT INTO inscricoes (id_participante, id_evento)
            VALUES (?, ?)
            ''', inscricao.para_tupla())
            self.conn.commit()
            print(f"Inscrição para participante ID {inscricao.id_participante} no evento ID {inscricao.id_evento} adicionada com sucesso.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar inscrição: {e}")
            return None
    
    def ler_todas_inscricoes(self):
        """Recupera todas as inscrições do banco de dados"""
        try:
            self.cursor.execute("SELECT * FROM inscricoes")
            inscricoes = []
            for dados_inscricao in self.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições: {e}")
            return []
    
    def ler_inscricao_por_id(self, id_inscricao):
        """Recupera uma única inscrição pelo ID"""
        try:
            self.cursor.execute("SELECT * FROM inscricoes WHERE id=?", (id_inscricao,))
            dados_inscricao = self.cursor.fetchone()
            if dados_inscricao:
                return Inscricao.de_tupla(dados_inscricao)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrição: {e}")
            return None
    
    def ler_inscricoes_por_evento(self, id_evento):
        """Recupera todas as inscrições associadas a um evento"""
        try:
            self.cursor.execute("SELECT * FROM inscricoes WHERE id_evento=?", (id_evento,))
            inscricoes = []
            for dados_inscricao in self.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do evento: {e}")
            return []
    
    def ler_inscricoes_por_participante(self, id_participante):
        """Recupera todas as inscrições de um participante"""
        try:
            self.cursor.execute("SELECT * FROM inscricoes WHERE id_participante=?", (id_participante,))
            inscricoes = []
            for dados_inscricao in self.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do participante: {e}")
            return []
    
    def verificar_inscricao(self, id_participante, id_evento):
        """Verifica se um participante já está inscrito em um evento"""
        try:
            self.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (id_participante, id_evento))
            
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar inscrição: {e}")
            return False
    
    def deletar_inscricao(self, id_inscricao):
        """Exclui uma inscrição pelo ID"""
        try:
            self.cursor.execute("DELETE FROM inscricoes WHERE id=?", (id_inscricao,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Inscrição com ID {id_inscricao} excluída com sucesso.")
                return True
            print(f"Nenhuma inscrição encontrada com ID {id_inscricao}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir inscrição: {e}")
            return False
    
    def deletar_inscricao_por_participante_evento(self, id_participante, id_evento):
        """Exclui uma inscrição pela combinação de participante e evento"""
        try:
            self.cursor.execute('''
            DELETE FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (id_participante, id_evento))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Inscrição para participante ID {id_participante} no evento ID {id_evento} excluída com sucesso.")
                return True
            print(f"Nenhuma inscrição encontrada para participante ID {id_participante} no evento ID {id_evento}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir inscrição: {e}")
            return False
    
    # === MÉTODOS AUXILIARES ===
    
    def listar_participantes_por_evento(self, id_evento):
        """Lista todos os participantes inscritos em um evento"""
        try:
            self.cursor.execute('''
            SELECT p.* FROM participantes p
            JOIN inscricoes i ON p.id = i.id_participante
            WHERE i.id_evento = ?
            ''', (id_evento,))
            
            participantes = []
            for dados_participante in self.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao listar participantes do evento: {e}")
            return []
    
    def listar_eventos_por_participante(self, id_participante):
        """Lista todos os eventos em que um participante está inscrito"""
        try:
            self.cursor.execute('''
            SELECT e.* FROM eventos e
            JOIN inscricoes i ON e.id = i.id_evento
            WHERE i.id_participante = ?
            ''', (id_participante,))
            
            eventos = []
            for dados_evento in self.cursor.fetchall():
                evento = Evento(
                    titulo=dados_evento[1],
                    descricao=dados_evento[2],
                    data=dados_evento[3],
                    local=dados_evento[8],
                    id=dados_evento[0]
                )
                # Adiciona os outros atributos
                evento.hora_inicio = dados_evento[4]
                evento.hora_fim = dados_evento[5]
                evento.publico_alvo = dados_evento[6]
                evento.capacidade = dados_evento[7]
                evento.endereco = dados_evento[9]
                eventos.append(evento)
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao listar eventos do participante: {e}")
            return []
    
    def contar_participantes_por_evento(self, id_evento):
        """Conta o número de participantes inscritos em um evento"""
        try:
            self.cursor.execute('''
            SELECT COUNT(*) FROM inscricoes
            WHERE id_evento = ?
            ''', (id_evento,))
            
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Erro ao contar participantes do evento: {e}")
            return 0
