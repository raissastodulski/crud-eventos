import sqlite3
from .atividade_model import Atividade


class CrudBDAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd

    def criar_atividade(self, atividade):
        try:
            self.gerenciador_bd.cursor.execute(
                """
            INSERT INTO atividades (nome, facilitador, local, id_evento, hora_inicio, vagas)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                atividade.para_tupla(),
            )
            self.gerenciador_bd.conn.commit()
            print(f"Atividade '{atividade.nome}' adicionada com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar atividade: {e}")
            return None

    def ler_todas_atividades(self):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM atividades")
            atividades = []
            for dados_atividade in self.gerenciador_bd.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividades: {e}")
            return []

    def ler_atividade_por_id(self, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute(
                "SELECT * FROM atividades WHERE id=?", (id_atividade,)
            )
            dados_atividade = self.gerenciador_bd.cursor.fetchone()
            if dados_atividade:
                return Atividade.de_tupla(dados_atividade)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividade: {e}")
            return None

    def ler_atividades_por_evento(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute(
                "SELECT * FROM atividades WHERE id_evento=?", (id_evento,)
            )
            atividades = []
            for dados_atividade in self.gerenciador_bd.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao recuperar atividades do evento: {e}")
            return []

    def atualizar_atividade(self, atividade):
        try:
            self.gerenciador_bd.cursor.execute(
                """
            UPDATE atividades
            SET nome=?, facilitador=?, local=?, id_evento=?, hora_inicio=?, vagas=?
            WHERE id=?
            """,
                atividade.para_tupla_com_id(),
            )
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Atividade '{atividade.nome}' atualizada com sucesso.")
                return True
            print(f"Nenhuma atividade encontrada com ID {atividade.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar atividade: {e}")
            return False

    def deletar_atividade(self, id_atividade):
        try:
            self.gerenciador_bd.cursor.execute(
                "DELETE FROM atividades WHERE id=?", (id_atividade,)
            )
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Atividade com ID {id_atividade} excluída com sucesso.")
                return True
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir atividade: {e}")
            return False

    def buscar_atividades(self, termo_busca):
        try:
            termo = f"%{termo_busca}%"
            self.gerenciador_bd.cursor.execute(
                """
                SELECT * FROM atividades 
                WHERE nome LIKE ? OR facilitador LIKE ? OR local LIKE ?
                """,
                (termo, termo, termo),
            )

            atividades = []
            for dados_atividade in self.gerenciador_bd.cursor.fetchall():
                atividades.append(Atividade.de_tupla(dados_atividade))
            return atividades
        except sqlite3.Error as e:
            print(f"Erro ao buscar atividades: {e}")
            return []
