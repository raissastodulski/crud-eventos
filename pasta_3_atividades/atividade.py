from pasta_3_atividades.atividade_model import Atividade
from pasta_3_atividades.crud_bd_atividades import CrudBDAtividades
from pasta_0_modelos import CrudBDEventos

class CrudAtividades:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_atividades = CrudBDAtividades(gerenciador_bd)
        self.crud_bd_eventos = CrudBDEventos(gerenciador_bd)
    
    def adicionar_atividade(self):
        """Adiciona uma nova atividade"""
        print("\n===== ADICIONAR NOVA ATIVIDADE =====")
        
        # Primeiro, verificamos se existem eventos para associar a atividade
        eventos = self.crud_bd_eventos.ler_todos_eventos()
        if not eventos:
            print("Não há eventos cadastrados. Uma atividade deve estar associada a um evento.")
            return False
        
        # Listar eventos para o usuário escolher
        print("\nEventos disponíveis:")
        for evento in eventos:
            print(f"[{evento.id}] {evento.titulo} ({evento.data})")
        
        # Solicitar ID do evento
        while True:
            id_evento = input("\nDigite o ID do evento para associar a atividade: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                continue
            
            id_evento = int(id_evento)
            evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
            if not evento:
                print(f"Nenhum evento encontrado com ID {id_evento}. Tente novamente.")
                continue
            
            break
        
        nome = input("Digite o nome da atividade: ")
        facilitador = input("Digite o nome do facilitador: ")
        hora_inicio = input("Digite a hora de início da atividade (HH:MM): ")
        
        while True:
            vagas_str = input("Digite o número de vagas disponíveis: ")
            if vagas_str.isdigit():
                vagas = int(vagas_str)
                break
            print("Por favor, digite um número válido.")
        
        atividade = Atividade(
            nome=nome,
            facilitador=facilitador,
            id_evento=id_evento,
            hora_inicio=hora_inicio,
            vagas=vagas
        )
        
        self.crud_bd_atividades.criar_atividade(atividade)
        print(f"Atividade '{nome}' adicionada com sucesso ao evento '{evento.titulo}'.")
        
        return True
    
    def ver_todas_atividades(self):
        """Ver todas as atividades"""
        print("\n===== TODAS AS ATIVIDADES =====")
        
        atividades = self.crud_bd_atividades.ler_todas_atividades()
        
        if not atividades:
            print("Nenhuma atividade encontrada.")
            return []
        else:
            # Para cada atividade, vamos obter o nome do evento
            for atividade in atividades:
                evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
                nome_evento = evento.titulo if evento else "Evento não encontrado"
                print(f"{atividade} | Evento: {nome_evento}")
            
            return atividades
    
    def ver_atividades_por_evento(self, id_evento=None):
        """Ver atividades de um evento específico"""
        print("\n===== ATIVIDADES POR EVENTO =====")
        
        if id_evento is None:
            # Listar eventos para o usuário escolher
            eventos = self.crud_bd_eventos.ler_todos_eventos()
            if not eventos:
                print("Não há eventos cadastrados.")
                return []
            
            print("\nEventos disponíveis:")
            for evento in eventos:
                print(f"[{evento.id}] {evento.titulo} ({evento.data})")
            
            id_evento = input("\nDigite o ID do evento para listar suas atividades: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return []
            
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}.")
            return []
        
        print(f"\nAtividades do evento: {evento.titulo}")
        atividades = self.crud_bd_atividades.ler_atividades_por_evento(id_evento)
        
        if not atividades:
            print(f"Nenhuma atividade encontrada para o evento '{evento.titulo}'.")
            return []
        
        for atividade in atividades:
            print(atividade)
        
        return atividades
    
    def ver_detalhes_atividade(self, id_atividade=None):
        """Ver detalhes de uma atividade específica"""
        print("\n===== DETALHES DA ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_atividade = int(id_atividade)
        
        atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
        
        if atividade:
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            nome_evento = evento.titulo if evento else "Evento não encontrado"
            
            print("\nDetalhes da Atividade:")
            print(f"ID: {atividade.id}")
            print(f"Nome: {atividade.nome}")
            print(f"Facilitador: {atividade.facilitador}")
            print(f"Evento: {nome_evento} (ID: {atividade.id_evento})")
            print(f"Hora de Início: {atividade.hora_inicio}")
            print(f"Vagas Disponíveis: {atividade.vagas}")
            return atividade
        else:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return None
    
    def atualizar_atividade(self, id_atividade=None):
        """Atualizar uma atividade existente"""
        print("\n===== ATUALIZAR ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade para atualizar: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)
        
        atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
        
        if not atividade:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return False
        
        # Mostrar os detalhes atuais
        evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
        nome_evento = evento.titulo if evento else "Evento não encontrado"
        
        print("\nDetalhes Atuais da Atividade:")
        print(f"ID: {atividade.id}")
        print(f"Nome: {atividade.nome}")
        print(f"Facilitador: {atividade.facilitador}")
        print(f"Evento: {nome_evento} (ID: {atividade.id_evento})")
        print(f"Hora de Início: {atividade.hora_inicio}")
        print(f"Vagas Disponíveis: {atividade.vagas}")
        
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_nome = input(f"Novo nome [{atividade.nome}]: ")
        if novo_nome:
            atividade.nome = novo_nome
        
        novo_facilitador = input(f"Novo facilitador [{atividade.facilitador}]: ")
        if novo_facilitador:
            atividade.facilitador = novo_facilitador
        
        # Opcionalmente, permitir mudar o evento associado
        mudar_evento = input("Deseja mudar o evento associado? (s/n): ")
        if mudar_evento.lower() == 's':
            # Listar eventos para o usuário escolher
            eventos = self.crud_bd_eventos.ler_todos_eventos()
            if not eventos:
                print("Não há outros eventos cadastrados.")
            else:
                print("\nEventos disponíveis:")
                for evt in eventos:
                    print(f"[{evt.id}] {evt.titulo} ({evt.data})")
                
                novo_id_evento = input(f"Novo ID do evento [{atividade.id_evento}]: ")
                if novo_id_evento.isdigit():
                    novo_id_evento = int(novo_id_evento)
                    evento_novo = self.crud_bd_eventos.ler_evento_por_id(novo_id_evento)
                    if evento_novo:
                        atividade.id_evento = novo_id_evento
                    else:
                        print(f"Evento com ID {novo_id_evento} não encontrado. Mantendo o evento atual.")
        
        nova_hora_inicio = input(f"Nova hora de início [{atividade.hora_inicio}]: ")
        if nova_hora_inicio:
            atividade.hora_inicio = nova_hora_inicio
        
        novas_vagas = input(f"Novas vagas disponíveis [{atividade.vagas}]: ")
        if novas_vagas.isdigit():
            atividade.vagas = int(novas_vagas)
        
        sucesso = self.crud_bd_atividades.atualizar_atividade(atividade)
        if not sucesso:
            print("Falha ao atualizar a atividade.")
            return False
        
        print("Atividade atualizada com sucesso.")
        return True
    
    def excluir_atividade(self, id_atividade=None):
        """Excluir uma atividade"""
        print("\n===== EXCLUIR ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade para excluir: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)
        
        atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
        
        if not atividade:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return False
        
        # Mostrar os detalhes para confirmar
        evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
        nome_evento = evento.titulo if evento else "Evento não encontrado"
        
        print("\nAtividade a ser excluída:")
        print(f"ID: {atividade.id}")
        print(f"Nome: {atividade.nome}")
        print(f"Facilitador: {atividade.facilitador}")
        print(f"Evento: {nome_evento}")
        
        confirmar = input("\nTem certeza de que deseja excluir esta atividade? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.crud_bd_atividades.deletar_atividade(id_atividade)
            if not sucesso:
                print("Falha ao excluir a atividade.")
                return False
            
            print("Atividade excluída com sucesso.")
            return True
        else:
            print("Exclusão cancelada.")
            return False
