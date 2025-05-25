import sqlite3
from .evento import Evento

class CrudBDEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_evento(self, evento):
        """Adiciona um novo evento ao banco de dados"""
        try:
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO eventos (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, 
                                publico_alvo, tipo, endereco, capacidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', evento.para_tupla())
            self.gerenciador_bd.conn.commit()
            print(f"Evento '{evento.nome}' adicionado com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao criar evento: {e}")
            return None
    
    def ler_todos_eventos(self):
        """Recupera todos os eventos do banco de dados"""
        try:
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos")
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    if len(dados_evento) >= 11:  # Verifica se tem todos os campos necessários
                        evento = Evento.de_tupla(dados_evento)
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
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
            dados_evento = self.gerenciador_bd.cursor.fetchone()
            if dados_evento:
                return Evento.de_tupla(dados_evento)
            return None
        except sqlite3.Error as e:
            print(f"Erro ao recuperar evento: {e}")
            return None
    
    def atualizar_evento(self, evento):
        """Atualiza um evento existente"""
        try:
            self.gerenciador_bd.cursor.execute('''
            UPDATE eventos
            SET nome=?, descricao=?, data_inicio=?, hora_inicio=?, data_fim=?, hora_fim=?, 
                publico_alvo=?, tipo=?, endereco=?, capacidade=?
            WHERE id=?
            ''', (*evento.para_tupla(), evento.id))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Evento '{evento.nome}' atualizado com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {evento.id}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar evento: {e}")
            return False
    
    def deletar_evento(self, id_evento):
        """Exclui um evento pelo ID"""
        try:
            self.gerenciador_bd.cursor.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Evento com ID {id_evento} excluído com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao excluir evento: {e}")
            return False
    
    def buscar_eventos(self, termo_busca):
        """Busca eventos contendo o termo de busca no nome, descrição, tipo ou endereço"""
        try:
            padrao_busca = f"%{termo_busca}%"
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM eventos 
            WHERE nome LIKE ? OR descricao LIKE ? OR tipo LIKE ? OR endereco LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca, padrao_busca))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento na busca: {ex}")
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao buscar eventos: {e}")
            return []
    
    def buscar_eventos_por_data(self, data_inicio=None, data_fim=None):
        """Busca eventos por período de data"""
        try:
            if data_inicio and data_fim:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_inicio >= ? AND data_fim <= ?
                ORDER BY data_inicio
                """, (data_inicio, data_fim))
            elif data_inicio:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_inicio >= ?
                ORDER BY data_inicio
                """, (data_inicio,))
            elif data_fim:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_fim <= ?
                ORDER BY data_inicio
                """, (data_fim,))
            else:
                return self.ler_todos_eventos()
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento na busca por data: {ex}")
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao buscar eventos por data: {e}")
            return []
    
    def buscar_eventos_por_tipo(self, tipo):
        """Busca eventos por tipo"""
        try:
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM eventos 
            WHERE tipo LIKE ?
            ORDER BY data_inicio
            """, (f"%{tipo}%",))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento na busca por tipo: {ex}")
            return eventos
        except sqlite3.Error as e:
            print(f"Erro ao buscar eventos por tipo: {e}")
            return []
