import sqlite3
from .evento import Evento

class CrudBDEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def criar_evento(self, evento):
        """Adiciona um novo evento ao banco de dados"""
        try:
            self.gerenciador_bd.cursor.execute('''
            INSERT INTO eventos (titulo, descricao, data, hora_inicio, hora_fim, 
                                publico_alvo, capacidade, local, endereco)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (evento.nome, evento.descricao, evento.data, 
                 getattr(evento, 'hora_inicio', None), 
                 getattr(evento, 'hora_fim', None),
                 getattr(evento, 'publico_alvo', None), 
                 getattr(evento, 'capacidade', None),
                 evento.local, 
                 getattr(evento, 'endereco', None)))
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
                    if len(dados_evento) >= 10:  # Verifica se tem todos os campos necessários
                        evento = Evento(
                            nome=dados_evento[1],
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
            self.gerenciador_bd.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
            dados_evento = self.gerenciador_bd.cursor.fetchone()
            if dados_evento:
                evento = Evento(
                    nome=dados_evento[1],
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
            self.gerenciador_bd.cursor.execute('''
            UPDATE eventos
            SET titulo=?, descricao=?, data=?, hora_inicio=?, hora_fim=?, 
                publico_alvo=?, capacidade=?, local=?, endereco=?
            WHERE id=?
            ''', (evento.nome, evento.descricao, evento.data, 
                 getattr(evento, 'hora_inicio', None), 
                 getattr(evento, 'hora_fim', None),
                 getattr(evento, 'publico_alvo', None), 
                 getattr(evento, 'capacidade', None),
                 evento.local, 
                 getattr(evento, 'endereco', None),
                 evento.id))
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
        """Busca eventos contendo o termo de busca no título ou descrição"""
        try:
            padrao_busca = f"%{termo_busca}%"
            self.gerenciador_bd.cursor.execute("""
            SELECT * FROM eventos 
            WHERE titulo LIKE ? OR descricao LIKE ? OR local LIKE ?
            """, (padrao_busca, padrao_busca, padrao_busca))
            
            eventos = []
            for dados_evento in self.gerenciador_bd.cursor.fetchall():
                evento = Evento(
                    nome=dados_evento[1],
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
