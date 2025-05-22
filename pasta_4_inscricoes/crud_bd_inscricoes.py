import sqlite3
from datetime import datetime
from pasta_4_inscricoes.inscricao import Inscricao
from pasta_0_modelos.evento import Evento
from pasta_3_atividades.atividade_model import Atividade
from pasta_1_participantes.participante_model import Participante

class CrudBDInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_inscricao(self, inscricao):
        try:
            # Verifica se o participante já está inscrito na atividade
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_atividade = ?
            ''', (inscricao.id_participante, inscricao.id_atividade))
            
            if self.gerenciador_bd.cursor.fetchone():
                print(f"Participante ID {inscricao.id_participante} já está inscrito na atividade ID {inscricao.id_atividade}.")
                return None
            
            # Obter a atividade para verificar vagas disponíveis
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM atividades WHERE id = ?
            ''', (inscricao.id_atividade,))
            
            dados_atividade = self.gerenciador_bd.cursor.fetchone()
            if not dados_atividade:
                print(f"Atividade com ID {inscricao.id_atividade} não encontrada.")
                return None
            
            atividade = Atividade.de_tupla(dados_atividade)
            
            # Contar inscrições existentes para esta atividade
            self.gerenciador_bd.cursor.execute('''
            SELECT COUNT(*) FROM inscricoes WHERE id_atividade = ?
            ''', (inscricao.id_atividade,))
            
            count_inscricoes_atividade = self.gerenciador_bd.cursor.fetchone()[0]
            
            # Verificar se há vagas disponíveis na atividade
            if count_inscricoes_atividade >= atividade.vagas:
                print(f"Não há vagas disponíveis para a atividade ID {inscricao.id_atividade}.")
                return None
            
            # Obter o evento associado à atividade
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM eventos 
            WHERE id = ?
            ''', (atividade.id_evento,))
            
            dados_evento = self.gerenciador_bd.cursor.fetchone()
            if not dados_evento:
                print(f"Evento associado à atividade ID {inscricao.id_atividade} não encontrado.")
                return None
            
            # Criar um objeto Evento a partir dos dados obtidos
            evento = Evento.de_tupla(dados_evento)
            
            # Contar participantes únicos inscritos no evento (através de qualquer atividade do evento)
            self.gerenciador_bd.cursor.execute('''
            SELECT COUNT(DISTINCT i.id_participante) 
            FROM inscricoes i
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ?
            ''', (atividade.id_evento,))
            
            count_participantes_evento = self.gerenciador_bd.cursor.fetchone()[0]
            
            # Verificar se o participante já está inscrito em alguma atividade deste evento
            self.gerenciador_bd.cursor.execute('''
            SELECT i.* FROM inscricoes i
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ? AND i.id_participante = ?
            ''', (atividade.id_evento, inscricao.id_participante))
            
            participante_ja_inscrito_evento = self.gerenciador_bd.cursor.fetchone() is not None
            
            # Se o participante não estiver inscrito no evento e o evento já atingiu a capacidade,
            # não permitir a inscrição
            if not participante_ja_inscrito_evento and count_participantes_evento >= evento.capacidade and evento.capacidade is not None:
                print(f"O evento associado à atividade já atingiu sua capacidade máxima de {evento.capacidade} participantes.")
                print("Como você não está inscrito em nenhuma atividade deste evento, não é possível realizar a inscrição.")
                return None
            
            # Se a data de inscrição não foi fornecida, usar a data atual
            if inscricao.data_inscricao is None:
                inscricao.data_inscricao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Inserir a inscrição
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO inscricoes (id_participante, id_atividade, data_inscricao)
            VALUES (?, ?, ?)
            ''', inscricao.para_tupla())
            
            self.gerenciador_bd.conn.commit()
            print(f"Inscrição para participante ID {inscricao.id_participante} na atividade ID {inscricao.id_atividade} adicionada com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar inscrição: {e}")
            return None
    
    def ler_todas_inscricoes(self):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes")
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições: {e}")
            return []
    
    def ler_inscricao_por_id(self, id_inscricao):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id=?", (id_inscricao,))
            dados_inscricao = self.gerenciador_bd.cursor.fetchone()
            if dados_inscricao:
                return Inscricao.de_tupla(dados_inscricao)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrição: {e}")
            return None
    
    def ler_inscricoes_por_atividade(self, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id_atividade=?", (id_atividade,))
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições da atividade: {e}")
            return []
    
    def ler_inscricoes_por_evento(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT i.* FROM inscricoes i
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ?
            ''', (id_evento,))
            
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do evento: {e}")
            return []
    
    def ler_inscricoes_por_participante(self, id_participante):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id_participante=?", (id_participante,))
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do participante: {e}")
            return []
    
    def verificar_inscricao_atividade(self, id_participante, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_atividade = ?
            ''', (id_participante, id_atividade))
            
            return self.gerenciador_bd.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar inscrição: {e}")
            return False
    
    def verificar_inscricao_evento(self, id_participante, id_evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM inscricoes i
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ? AND i.id_participante = ?
            ''', (id_evento, id_participante))
            
            return self.gerenciador_bd.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar inscrição no evento: {e}")
            return False
    
    def deletar_inscricao(self, id_inscricao):
        try:
            self.gerenciador_bd.cursor.execute("DELETE FROM inscricoes WHERE id=?", (id_inscricao,))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Inscrição com ID {id_inscricao} excluída com sucesso.")
                return True
            print(f"Nenhuma inscrição encontrada com ID {id_inscricao}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir inscrição: {e}")
            return False
    
    def deletar_inscricao_por_participante_atividade(self, id_participante, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute('''
            DELETE FROM inscricoes 
            WHERE id_participante = ? AND id_atividade = ?
            ''', (id_participante, id_atividade))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Inscrição para participante ID {id_participante} na atividade ID {id_atividade} excluída com sucesso.")
                return True
            print(f"Nenhuma inscrição encontrada para participante ID {id_participante} na atividade ID {id_atividade}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir inscrição: {e}")
            return False
    
    def listar_participantes_por_atividade(self, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT p.* FROM participantes p
            JOIN inscricoes i ON p.id = i.id_participante
            WHERE i.id_atividade = ?
            ''', (id_atividade,))
            
            participantes = []
            for dados_participante in self.gerenciador_bd.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao listar participantes da atividade: {e}")
            return []
    
    def listar_participantes_por_evento(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT DISTINCT p.* FROM participantes p
            JOIN inscricoes i ON p.id = i.id_participante
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ?
            ''', (id_evento,))
            
            participantes = []
            for dados_participante in self.gerenciador_bd.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao listar participantes do evento: {e}")
            return []
    
    def listar_atividades_por_participante(self, id_participante):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT a.* FROM atividades a
            JOIN inscricoes i ON a.id = i.id_atividade
            WHERE i.id_participante = ?
            ''', (id_participante,))
            
            atividades = []
            for dados_atividade in self.gerenciador_bd.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao listar atividades do participante: {e}")
            return []
    
    def listar_eventos_por_participante(self, id_participante):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT DISTINCT e.* FROM eventos e
            JOIN atividades a ON e.id = a.id_evento
            JOIN inscricoes i ON a.id = i.id_atividade
            WHERE i.id_participante = ?
            ''', (id_participante,))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                evento = Evento.de_tupla(dados_evento)
                eventos.append(evento)
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao listar eventos do participante: {e}")
            return []
    
    def contar_participantes_por_atividade(self, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT COUNT(*) FROM inscricoes
            WHERE id_atividade = ?
            ''', (id_atividade,))
            
            return self.gerenciador_bd.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Erro ao contar participantes da atividade: {e}")
            return 0
    
    def contar_participantes_por_evento(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT COUNT(DISTINCT i.id_participante) FROM inscricoes i
            JOIN atividades a ON i.id_atividade = a.id
            WHERE a.id_evento = ?
            ''', (id_evento,))
            
            return self.gerenciador_bd.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Erro ao contar participantes do evento: {e}")
            return 0