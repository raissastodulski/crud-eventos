import sqlite3
from .evento import Evento

class CrudBdEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def _executar_com_seguranca(self, funcao):
        try:
            if not self.gerenciador_bd.verificar_conexao():
                print("❌ Erro: Conexão com banco de dados não disponível")
                return None
            return funcao()
        except sqlite3.Error as e:
            print(f"❌ Erro SQLite: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None
    
    def criar_evento(self, evento):
        def _criar():
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO eventos (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, 
                                publico_alvo, local, endereco, capacidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', evento.para_tupla())
            self.gerenciador_bd.conn.commit()
            print(f"Evento '{evento.nome}' adicionado com sucesso.")
            return self.gerenciador_bd.cursor.lastrowid
        
        return self._executar_com_seguranca(_criar)
    
    def ler_todos_eventos(self):
        def _ler():
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos")
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    if len(dados_evento) >= 10:
                        evento = Evento.de_tupla(dados_evento)
                        eventos.append(evento)
                    else:
                        print(f"Aviso: Registro de evento incompleto: {dados_evento}")
                except Exception as ex:
                    print(f"Erro ao processar evento: {ex}")
            return eventos
        
        result = self._executar_com_seguranca(_ler)
        return result if result is not None else []
    
    def ler_evento_por_id(self, id_evento):
        def _ler():
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
            dados_evento = self.gerenciador_bd.cursor.fetchone()
            if dados_evento:
                return Evento.de_tupla(dados_evento)
            return None
        
        return self._executar_com_seguranca(_ler)
    
    def atualizar_evento(self, evento):
        def _atualizar():
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
        
        result = self._executar_com_seguranca(_atualizar)
        return result if result is not None else False
    
    def deletar_evento(self, id_evento):
        def _deletar():
            self.gerenciador_bd.cursor.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
            self.gerenciador_bd.conn.commit()
            if self.gerenciador_bd.cursor.rowcount > 0:
                print(f"Evento com ID {id_evento} excluído com sucesso.")
                return True
            print(f"Nenhum evento encontrado com ID {id_evento}")
            return False
        
        result = self._executar_com_seguranca(_deletar)
        return result if result is not None else False
    
    def buscar_eventos(self, termo_busca):
        def _buscar():
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
        
        result = self._executar_com_seguranca(_buscar)
        return result if result is not None else []
    
    def buscar_eventos_por_data(self, data_inicio=None, data_fim=None):
        def _buscar_por_data():
            data_inicio_str = data_inicio.isoformat() if data_inicio else None
            data_fim_str = data_fim.isoformat() if data_fim else None
            
            if data_inicio_str and data_fim_str:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_inicio >= ? AND data_fim <= ?
                ORDER BY data_inicio
                """, (data_inicio_str, data_fim_str))
            elif data_inicio_str:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_inicio >= ?
                ORDER BY data_inicio
                """, (data_inicio_str,))
            elif data_fim_str:
                self.gerenciador_bd.cursor.execute("""
                SELECT * FROM eventos 
                WHERE data_fim <= ?
                ORDER BY data_inicio
                """, (data_fim_str,))
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
        
        result = self._executar_com_seguranca(_buscar_por_data)
        return result if result is not None else []
    
    def buscar_eventos_por_local(self, local):
        def _buscar_por_local():
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM eventos 
            WHERE local LIKE ? OR endereco LIKE ?
            ORDER BY data_inicio
            """, (f"%{local}%", f"%{local}%"))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                try:
                    evento = Evento.de_tupla(dados_evento)
                    eventos.append(evento)
                except Exception as ex:
                    print(f"Erro ao processar evento na busca por local: {ex}")
            return eventos
        
        result = self._executar_com_seguranca(_buscar_por_local)
        return result if result is not None else []
