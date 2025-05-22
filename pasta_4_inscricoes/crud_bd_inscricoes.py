import sqlite3
from pasta_4_inscricoes.inscricao import Inscricao
from pasta_0_modelos import Evento
from pasta_1_participantes.participante_model import Participante

class CrudBDInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_inscricao(self, inscricao):
        """Adiciona uma nova inscrição ao banco de dados"""
        try:
            # Verifica se o participante já está inscrito no evento
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (inscricao.id_participante, inscricao.id_evento))
            
            if self.gerenciador_bd.cursor.fetchone():
                print(f"Participante ID {inscricao.id_participante} já está inscrito no evento ID {inscricao.id_evento}.")
                return None
            
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO inscricoes (id_participante, id_evento)
            VALUES (?, ?)
            ''', inscricao.para_tupla())
            self.gerenciador_bd.conn.commit()
            print(f"Inscrição para participante ID {inscricao.id_participante} no evento ID {inscricao.id_evento} adicionada com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar inscrição: {e}")
            return None
    
    def ler_todas_inscricoes(self):
        """Recupera todas as inscrições do banco de dados"""
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
        """Recupera uma única inscrição pelo ID"""
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id=?", (id_inscricao,))
            dados_inscricao = self.gerenciador_bd.cursor.fetchone()
            if dados_inscricao:
                return Inscricao.de_tupla(dados_inscricao)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrição: {e}")
            return None
    
    def ler_inscricoes_por_evento(self, id_evento):
        """Recupera todas as inscrições associadas a um evento"""
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id_evento=?", (id_evento,))
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do evento: {e}")
            return []
    
    def ler_inscricoes_por_participante(self, id_participante):
        """Recupera todas as inscrições de um participante"""
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM inscricoes WHERE id_participante=?", (id_participante,))
            inscricoes = []
            for dados_inscricao in self.gerenciador_bd.cursor.fetchall():
                inscricoes.append(Inscricao.de_tupla(dados_inscricao))
            return inscricoes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar inscrições do participante: {e}")
            return []
    
    def verificar_inscricao(self, id_participante, id_evento):
        """Verifica se um participante já está inscrito em um evento"""
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT * FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (id_participante, id_evento))
            
            return self.gerenciador_bd.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erro ao verificar inscrição: {e}")
            return False
    
    def deletar_inscricao(self, id_inscricao):
        """Exclui uma inscrição pelo ID"""
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
    
    def deletar_inscricao_por_participante_evento(self, id_participante, id_evento):
        """Exclui uma inscrição pela combinação de participante e evento"""
        try:
            self.gerenciador_bd.cursor.execute('''
            DELETE FROM inscricoes 
            WHERE id_participante = ? AND id_evento = ?
            ''', (id_participante, id_evento))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Inscrição para participante ID {id_participante} no evento ID {id_evento} excluída com sucesso.")
                return True
            print(f"Nenhuma inscrição encontrada para participante ID {id_participante} no evento ID {id_evento}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir inscrição: {e}")
            return False
    
    def listar_participantes_por_evento(self, id_evento):
        """Lista todos os participantes inscritos em um evento"""
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT p.* FROM participantes p
            JOIN inscricoes i ON p.id = i.id_participante
            WHERE i.id_evento = ?
            ''', (id_evento,))
            
            participantes = []
            for dados_participante in self.gerenciador_bd.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao listar participantes do evento: {e}")
            return []
    
    def listar_eventos_por_participante(self, id_participante):
        """Lista todos os eventos em que um participante está inscrito"""
        try:
            self.gerenciador_bd.cursor.execute('''
            SELECT e.* FROM eventos e
            JOIN inscricoes i ON e.id = i.id_evento
            WHERE i.id_participante = ?
            ''', (id_participante,))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
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
            self.gerenciador_bd.cursor.execute('''
            SELECT COUNT(*) FROM inscricoes
            WHERE id_evento = ?
            ''', (id_evento,))
            
            return self.gerenciador_bd.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Erro ao contar participantes do evento: {e}")
            return 0
