import sqlite3
from .evento import Evento

class CrudBdEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_evento(self, evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO eventos (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, 
                                publico_alvo, local, endereco, capacidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', evento.para_tupla())
            self.gerenciador_bd.conn.commit()
            print(f"Evento '{evento.nome}' adicionado com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except Exception as ex:
            print(f"Erro ao criar evento: {ex}")
            return None
    
    def ler_todos_eventos(self):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos")
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento: {ex}")
            return eventos
        except Exception as ex:
            print(f"Erro ao ler eventos: {ex}")
            return []
    
    def ler_evento_por_id(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
            dados_evento = self.gerenciador_bd.cursor.fetchone()
            if dados_evento:
                return Evento.de_tupla(dados_evento)
            return None
        except Exception as ex:
            print(f"Erro ao ler evento por ID: {ex}")
            return None
    
    def atualizar_evento(self, evento):
        try:
            self.gerenciador_bd.cursor.execute('''
            UPDATE eventos
            SET nome=?, descricao=?, data_inicio=?, hora_inicio=?, data_fim=?, hora_fim=?, 
                publico_alvo=?, local=?, endereco=?, capacidade=?
            WHERE id=?
            ''', (*evento.para_tupla(), evento.id))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Evento '{evento.nome}' atualizado com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {evento.id}")
            return False
        except Exception as ex:
            print(f"Erro ao atualizar evento: {ex}")
            return False
        
    def deletar_evento(self, id_evento):
        try:
            self.gerenciador_bd.cursor.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Evento com ID {id_evento} excluído com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        except Exception as ex:
            print(f"Erro ao deletar evento: {ex}")
            return False
        
    def buscar_eventos(self, termo_busca):
        try:
            padrao_busca = f"%{termo_busca}%"
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM eventos 
            WHERE nome LIKE ? OR descricao LIKE ? OR local LIKE ? OR endereco LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca, padrao_busca))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento na busca: {ex}")
            return eventos
        except Exception as ex:
            print(f"Erro ao buscar eventos: {ex}")
            return []
    