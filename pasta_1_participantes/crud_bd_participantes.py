import sqlite3
from .participante import Participante

class CrudBdParticipantes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_participante(self, participante):
        try:
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO participantes (nome, cpf, email, telefone, data_nascimento)
            VALUES (?, ?, ?, ?, ?)
            ''', participante.para_tupla())
            self.gerenciador_bd.conn.commit()
            print(f"Participante '{participante.nome}' adicionado com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar participante: {e}")
            return None
    
    def ler_todos_participantes(self):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM participantes")
            participantes = []
            for dados_participante in self.gerenciador_bd.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao recuperar participantes: {e}")
            return []
    
    def ler_participante_por_id(self, id_participante):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM participantes WHERE id=?", (id_participante,))
            dados_participante = self.gerenciador_bd.cursor.fetchone()
            if dados_participante:
                return Participante.de_tupla(dados_participante)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar participante: {e}")
            return None
    
    def atualizar_participante(self, participante):
        try:
            self.gerenciador_bd.cursor.execute('''
            UPDATE participantes
            SET nome=?, cpf=?, email=?, telefone=?, data_nascimento=?
            WHERE id=?
            ''', participante.para_tupla_com_id())
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Participante '{participante.nome}' atualizado com sucesso.")
                return True
            print(f"Nenhum participante encontrado com ID {participante.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar participante: {e}")
            return False
    
    def deletar_participante(self, id_participante):
        try:
            self.gerenciador_bd.cursor.execute("DELETE FROM participantes WHERE id=?", (id_participante,))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Participante com ID {id_participante} excluído com sucesso.")
                return True
            print(f"Nenhum participante encontrado com ID {id_participante}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir participante: {e}")
            return False
    
    def buscar_participantes(self, termo_busca):
        try:
            padrao_busca = f"%{termo_busca}%"
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM participantes 
            WHERE nome LIKE ? OR email LIKE ? OR cpf LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca))
            
            participantes = []
            for dados_participante in self.gerenciador_bd.cursor.fetchall():
                participantes.append(Participante.de_tupla(dados_participante))
            return participantes
        except sqlite3.Error as e:
            print(f"Erro ao buscar participantes: {e}")
            return []
