from pasta_4_inscricoes.inscricao import Inscricao
from pasta_4_inscricoes.crud_bd_inscricoes import CrudBDInscricoes
from pasta_0_modelos import CrudBDEventos
from pasta_1_participantes.crud_bd_participantes import CrudBDParticipantes

class CrudInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_inscricoes = CrudBDInscricoes(gerenciador_bd)
        self.crud_bd_eventos = CrudBDEventos(gerenciador_bd)
        self.crud_bd_participantes = CrudBDParticipantes(gerenciador_bd)
    
    def adicionar_inscricao(self):
        """Adiciona uma nova inscrição"""
        print("\n===== ADICIONAR NOVA INSCRIÇÃO =====")
        
        # Verificar se existem eventos e participantes
        eventos = self.crud_bd_eventos.ler_todos_eventos()
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        
        if not eventos:
            print("Não há eventos cadastrados. Uma inscrição deve estar associada a um evento.")
            return False
        
        if not participantes:
            print("Não há participantes cadastrados. Uma inscrição deve estar associada a um participante.")
            return False
        
        # Listar eventos para o usuário escolher
        print("\nEventos disponíveis:")
        for evento in eventos:
            print(f"[{evento.id}] {evento.titulo} ({evento.data})")
        
        # Solicitar ID do evento
        while True:
            id_evento = input("\nDigite o ID do evento para a inscrição: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                continue
            
            id_evento = int(id_evento)
            evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
            if not evento:
                print(f"Nenhum evento encontrado com ID {id_evento}. Tente novamente.")
                continue
            
            break
        
        # Listar participantes para o usuário escolher
        print("\nParticipantes disponíveis:")
        for participante in participantes:
            print(f"[{participante.id}] {participante.nome} ({participante.email})")
        
        # Solicitar ID do participante
        while True:
            id_participante = input("\nDigite o ID do participante para a inscrição: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                continue
            
            id_participante = int(id_participante)
            participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
            if not participante:
                print(f"Nenhum participante encontrado com ID {id_participante}. Tente novamente.")
                continue
            
            # Verificar se o participante já está inscrito no evento
            if self.crud_bd_inscricoes.verificar_inscricao(id_participante, id_evento):
                print(f"O participante {participante.nome} já está inscrito no evento {evento.titulo}.")
                return False
            
            break
        
        inscricao = Inscricao(id_participante=id_participante, id_evento=id_evento)
        resultado = self.crud_bd_inscricoes.criar_inscricao(inscricao)
        
        if resultado:
            print(f"Inscrição realizada com sucesso: {participante.nome} no evento {evento.titulo}.")
            return True
        else:
            print("Falha ao realizar a inscrição.")
            return False
    
    def ver_todas_inscricoes(self):
        """Ver todas as inscrições"""
        print("\n===== TODAS AS INSCRIÇÕES =====")
        
        inscricoes = self.crud_bd_inscricoes.ler_todas_inscricoes()
        
        if not inscricoes:
            print("Nenhuma inscrição encontrada.")
            return []
        else:
            print(f"Total de inscrições: {len(inscricoes)}")
            for inscricao in inscricoes:
                participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
                evento = self.crud_bd_eventos.ler_evento_por_id(inscricao.id_evento)
                
                nome_participante = participante.nome if participante else "Participante não encontrado"
                nome_evento = evento.titulo if evento else "Evento não encontrado"
                
                print(f"[{inscricao.id}] {nome_participante} → {nome_evento}")
            
            return inscricoes
    
    def ver_inscricoes_por_evento(self, id_evento=None):
        """Ver inscrições de um evento específico"""
        print("\n===== INSCRIÇÕES POR EVENTO =====")
        
        if id_evento is None:
            # Listar eventos para o usuário escolher
            eventos = self.crud_bd_eventos.ler_todos_eventos()
            if not eventos:
                print("Não há eventos cadastrados.")
                return []
            
            print("\nEventos disponíveis:")
            for evento in eventos:
                print(f"[{evento.id}] {evento.titulo} ({evento.data})")
            
            id_evento = input("\nDigite o ID do evento para listar suas inscrições: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return []
            
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}.")
            return []
        
        print(f"\nInscrições para o evento: {evento.titulo}")
        participantes = self.crud_bd_inscricoes.listar_participantes_por_evento(id_evento)
        
        if not participantes:
            print(f"Nenhuma inscrição encontrada para o evento '{evento.titulo}'.")
            return []
        
        print(f"Total de inscrições: {len(participantes)}")
        for participante in participantes:
            print(f"[{participante.id}] {participante.nome} ({participante.email})")
        
        return participantes
    
    def ver_inscricoes_por_participante(self, id_participante=None):
        """Ver inscrições de um participante específico"""
        print("\n===== INSCRIÇÕES POR PARTICIPANTE =====")
        
        if id_participante is None:
            # Listar participantes para o usuário escolher
            participantes = self.crud_bd_participantes.ler_todos_participantes()
            if not participantes:
                print("Não há participantes cadastrados.")
                return []
            
            print("\nParticipantes disponíveis:")
            for participante in participantes:
                print(f"[{participante.id}] {participante.nome} ({participante.email})")
            
            id_participante = input("\nDigite o ID do participante para listar suas inscrições: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return []
            
            id_participante = int(id_participante)
        
        participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
        if not participante:
            print(f"Nenhum participante encontrado com ID {id_participante}.")
            return []
        
        print(f"\nInscrições do participante: {participante.nome}")
        eventos = self.crud_bd_inscricoes.listar_eventos_por_participante(id_participante)
        
        if not eventos:
            print(f"Nenhuma inscrição encontrada para o participante '{participante.nome}'.")
            return []
        
        print(f"Total de inscrições: {len(eventos)}")
        for evento in eventos:
            print(f"[{evento.id}] {evento.titulo} ({evento.data})")
        
        return eventos
    
    def cancelar_inscricao(self):
        """Cancela uma inscrição"""
        print("\n===== CANCELAR INSCRIÇÃO =====")
        
        # Opção 1: Cancelar por ID de inscrição
        # Opção 2: Cancelar por combinação de participante e evento
        print("1. Cancelar por ID de inscrição")
        print("2. Cancelar por participante e evento")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            # Cancelar por ID de inscrição
            id_inscricao = input("Digite o ID da inscrição a ser cancelada: ")
            if not id_inscricao.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            
            id_inscricao = int(id_inscricao)
            inscricao = self.crud_bd_inscricoes.ler_inscricao_por_id(id_inscricao)
            
            if not inscricao:
                print(f"Nenhuma inscrição encontrada com ID {id_inscricao}.")
                return False
            
            # Obter informações para mostrar ao usuário
            participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
            evento = self.crud_bd_eventos.ler_evento_por_id(inscricao.id_evento)
            
            nome_participante = participante.nome if participante else "Participante não encontrado"
            nome_evento = evento.titulo if evento else "Evento não encontrado"
            
            print(f"\nInscrição a ser cancelada:")
            print(f"ID: {inscricao.id}")
            print(f"Participante: {nome_participante}")
            print(f"Evento: {nome_evento}")
            
            confirmar = input("\nTem certeza de que deseja cancelar esta inscrição? (s/n): ")
            
            if confirmar.lower() == 's':
                sucesso = self.crud_bd_inscricoes.deletar_inscricao(id_inscricao)
                if sucesso:
                    print("Inscrição cancelada com sucesso.")
                    return True
                else:
                    print("Falha ao cancelar inscrição.")
                    return False
            else:
                print("Cancelamento cancelado.")
                return False
            
        elif opcao == '2':
            # Cancelar por combinação de participante e evento
            # Listar participantes para o usuário escolher
            participantes = self.crud_bd_participantes.ler_todos_participantes()
            if not participantes:
                print("Não há participantes cadastrados.")
                return False
            
            print("\nParticipantes disponíveis:")
            for participante in participantes:
                print(f"[{participante.id}] {participante.nome} ({participante.email})")
            
            id_participante = input("\nDigite o ID do participante: ")
            if not id_participante.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            
            id_participante = int(id_participante)
            participante = self.crud_bd_participantes.ler_participante_por_id(id_participante)
            
            if not participante:
                print(f"Nenhum participante encontrado com ID {id_participante}.")
                return False
            
            # Listar eventos em que o participante está inscrito
            eventos = self.crud_bd_inscricoes.listar_eventos_por_participante(id_participante)
            
            if not eventos:
                print(f"O participante {participante.nome} não está inscrito em nenhum evento.")
                return False
            
            print(f"\nEventos em que {participante.nome} está inscrito:")
            for evento in eventos:
                print(f"[{evento.id}] {evento.titulo} ({evento.data})")
            
            id_evento = input("\nDigite o ID do evento para cancelar a inscrição: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            
            id_evento = int(id_evento)
            evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
            
            if not evento:
                print(f"Nenhum evento encontrado com ID {id_evento}.")
                return False
            
            # Verificar se o participante está inscrito no evento
            if not self.crud_bd_inscricoes.verificar_inscricao(id_participante, id_evento):
                print(f"O participante {participante.nome} não está inscrito no evento {evento.titulo}.")
                return False
            
            print(f"\nInscrição a ser cancelada:")
            print(f"Participante: {participante.nome}")
            print(f"Evento: {evento.titulo}")
            
            confirmar = input("\nTem certeza de que deseja cancelar esta inscrição? (s/n): ")
            
            if confirmar.lower() == 's':
                sucesso = self.crud_bd_inscricoes.deletar_inscricao_por_participante_evento(id_participante, id_evento)
                if sucesso:
                    print("Inscrição cancelada com sucesso.")
                    return True
                else:
                    print("Falha ao cancelar inscrição.")
                    return False
            else:
                print("Cancelamento cancelado.")
                return False
        else:
            print("Opção inválida.")
            return False
