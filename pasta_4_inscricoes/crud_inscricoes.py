from datetime import datetime
from pasta_4_inscricoes.inscricao import Inscricao
from pasta_4_inscricoes.crud_bd_inscricoes import CrudBdInscricoes
from pasta_2_eventos import CrudBdEventos
from pasta_1_participantes.crud_bd_participantes import CrudBdParticipantes
from pasta_3_atividades.crud_bd_atividades import CrudBdAtividades

class CrudInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_bd_inscricoes = CrudBdInscricoes(gerenciador_bd)
        self.crud_bd_eventos = CrudBdEventos(gerenciador_bd)
        self.crud_bd_participantes = CrudBdParticipantes(gerenciador_bd)
        self.crud_bd_atividades = CrudBdAtividades(gerenciador_bd)
    
    def adicionar_inscricao(self):
        print("\n===== ADICIONAR NOVA INSCRIÇÃO =====")
        
        atividades = self.crud_bd_atividades.ler_todas_atividades()
        participantes = self.crud_bd_participantes.ler_todos_participantes()
        
        if not atividades:
            print("Não há atividades cadastradas. Uma inscrição deve estar associada a uma atividade.")
            return False
        
        if not participantes:
            print("Não há participantes cadastrados. Uma inscrição deve estar associada a um participante.")
            return False
        
        print("\nAtividades disponíveis:")
        for atividade in atividades:
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            evento_nome = evento.nome if evento else "Evento não encontrado"
            
            participantes_inscritos = self.crud_bd_inscricoes.contar_participantes_por_atividade(atividade.id)
            vagas_disponiveis = atividade.vagas - participantes_inscritos
            
            print(f"[{atividade.id}] {atividade.nome} | Facilitador: {atividade.facilitador} | "
                  f"Evento: {evento_nome} | Vagas disponíveis: {vagas_disponiveis}/{atividade.vagas}")
        
        while True:
            id_atividade = input("\nDigite o ID da atividade para a inscrição: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                continue
            
            id_atividade = int(id_atividade)
            atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
            if not atividade:
                print(f"Nenhuma atividade encontrada com ID {id_atividade}. Tente novamente.")
                continue
            
            participantes_inscritos = self.crud_bd_inscricoes.contar_participantes_por_atividade(id_atividade)
            if participantes_inscritos >= atividade.vagas:
                print(f"Não há vagas disponíveis para a atividade '{atividade.nome}'.")
                return False
            
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            if not evento:
                print(f"Evento associado à atividade não encontrado.")
                continue
            
            break
        
        print("\nParticipantes disponíveis:")
        for participante in participantes:
            print(f"[{participante.id}] {participante.nome} ({participante.email})")
        
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
            
            if self.crud_bd_inscricoes.verificar_inscricao_atividade(id_participante, id_atividade):
                print(f"O participante {participante.nome} já está inscrito na atividade '{atividade.nome}'.")
                return False
            
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            participante_ja_no_evento = self.crud_bd_inscricoes.verificar_inscricao_evento(id_participante, evento.id)
            
            if not participante_ja_no_evento:
                participantes_evento = self.crud_bd_inscricoes.contar_participantes_por_evento(evento.id)
                if participantes_evento >= evento.capacidade and evento.capacidade is not None:
                    print(f"O evento '{evento.nome}' já atingiu sua capacidade máxima de {evento.capacidade} participantes.")
                    print("Como você não está inscrito em nenhuma atividade deste evento, não é possível realizar a inscrição.")
                    return False
            
            break
        
        data_inscricao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        inscricao = Inscricao(id_participante=id_participante, id_atividade=id_atividade, data_inscricao=data_inscricao)
        resultado = self.crud_bd_inscricoes.criar_inscricao(inscricao)
        
        if resultado:
            print(f"Inscrição realizada com sucesso: {participante.nome} na atividade '{atividade.nome}'.")
            return True
        else:
            print("Falha ao realizar a inscrição.")
            return False
    
    def ver_todas_inscricoes(self):
        print("\n===== TODAS AS INSCRIÇÕES =====")
        
        inscricoes = self.crud_bd_inscricoes.ler_todas_inscricoes()
        
        if not inscricoes:
            print("Nenhuma inscrição encontrada.")
            return []
        else:
            print(f"Total de inscrições: {len(inscricoes)}")
            for inscricao in inscricoes:
                participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
                atividade = self.crud_bd_atividades.ler_atividade_por_id(inscricao.id_atividade)
                
                nome_participante = participante.nome if participante else "Participante não encontrado"
                nome_atividade = atividade.nome if atividade else "Atividade não encontrada"
                
                evento = None
                if atividade:
                    evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
                
                nome_evento = evento.nome if evento else "Evento não encontrado"
                
                print(f"[{inscricao.id}] {nome_participante} → Atividade: {nome_atividade} | Evento: {nome_evento} | Data: {inscricao.data_inscricao}")
            
            return inscricoes
    
    def ver_inscricoes_por_atividade(self, id_atividade=None):
        print("\n===== INSCRIÇÕES POR ATIVIDADE =====")
        
        if id_atividade is None:
            atividades = self.crud_bd_atividades.ler_todas_atividades()
            if not atividades:
                print("Não há atividades cadastradas.")
                return []
            
            print("\nAtividades disponíveis:")
            for atividade in atividades:
                evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
                nome_evento = evento.nome if evento else "Evento não encontrado"
                print(f"[{atividade.id}] {atividade.nome} | Evento: {nome_evento}")
            
            id_atividade = input("\nDigite o ID da atividade para listar suas inscrições: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return []
            
            id_atividade = int(id_atividade)
        
        atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
        if not atividade:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}.")
            return []
        
        print(f"\nInscrições para a atividade: {atividade.nome}")
        participantes = self.crud_bd_inscricoes.listar_participantes_por_atividade(id_atividade)
        
        if not participantes:
            print(f"Nenhuma inscrição encontrada para a atividade '{atividade.nome}'.")
            return []
        
        print(f"Total de inscrições: {len(participantes)}/{atividade.vagas} vagas")
        for participante in participantes:
            print(f"[{participante.id}] {participante.nome} ({participante.email})")
        
        return participantes
    
    def ver_inscricoes_por_evento(self, id_evento=None):
        print("\n===== INSCRIÇÕES POR EVENTO =====")
        
        if id_evento is None:
            eventos = self.crud_bd_eventos.ler_todos_eventos()
            if not eventos:
                print("Não há eventos cadastrados.")
                return []
            
            print("\nEventos disponíveis:")
            for evento in eventos:
                data_exibicao = evento.data if hasattr(evento, 'data') else None
                print(f"[{evento.id}] {evento.nome} ({data_exibicao})")
            
            id_evento = input("\nDigite o ID do evento para listar suas inscrições: ")
            if not id_evento.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return []
            
            id_evento = int(id_evento)
        
        evento = self.crud_bd_eventos.ler_evento_por_id(id_evento)
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}.")
            return []
        
        print(f"\nInscrições para o evento: {evento.nome}")
        participantes = self.crud_bd_inscricoes.listar_participantes_por_evento(id_evento)
        
        if not participantes:
            print(f"Nenhuma inscrição encontrada para o evento '{evento.nome}'.")
            return []
        
        print(f"Total de participantes: {len(participantes)}/{evento.capacidade} capacidade")
        for participante in participantes:
            print(f"[{participante.id}] {participante.nome} ({participante.email})")
        
        return participantes
    
    def ver_inscricoes_por_participante(self, id_participante=None):
        print("\n===== INSCRIÇÕES POR PARTICIPANTE =====")
        
        if id_participante is None:
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
        
        atividades = self.crud_bd_inscricoes.listar_atividades_por_participante(id_participante)
        
        if not atividades:
            print(f"Nenhuma inscrição encontrada para o participante '{participante.nome}'.")
            return []
        
        print(f"Total de inscrições: {len(atividades)}")
        print("Atividades:")
        for atividade in atividades:
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            nome_evento = evento.nome if evento else "Evento não encontrado"
            print(f"[{atividade.id}] {atividade.nome} | Evento: {nome_evento}")
        
        eventos = self.crud_bd_inscricoes.listar_eventos_por_participante(id_participante)
        
        if eventos:
            print("\nEventos:")
            for evento in eventos:
                data_exibicao = evento.data if hasattr(evento, 'data') else None
                print(f"[{evento.id}] {evento.nome} ({data_exibicao})")
        
        return atividades
    
    def cancelar_inscricao(self):
        print("\n===== CANCELAR INSCRIÇÃO =====")
        
        print("1. Cancelar por ID de inscrição")
        print("2. Cancelar por participante e atividade")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            id_inscricao = input("Digite o ID da inscrição a ser cancelada: ")
            if not id_inscricao.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            
            id_inscricao = int(id_inscricao)
            inscricao = self.crud_bd_inscricoes.ler_inscricao_por_id(id_inscricao)
            
            if not inscricao:
                print(f"Nenhuma inscrição encontrada com ID {id_inscricao}.")
                return False
            
            participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
            atividade = self.crud_bd_atividades.ler_atividade_por_id(inscricao.id_atividade)
            
            nome_participante = participante.nome if participante else "Participante não encontrado"
            nome_atividade = atividade.nome if atividade else "Atividade não encontrada"
            
            evento = None
            if atividade:
                evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            
            nome_evento = evento.nome if evento else "Evento não encontrado"
            
            print(f"\nInscrição a ser cancelada:")
            print(f"ID: {inscricao.id}")
            print(f"Participante: {nome_participante}")
            print(f"Atividade: {nome_atividade}")
            print(f"Evento: {nome_evento}")
            print(f"Data de inscrição: {inscricao.data_inscricao}")
            
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
            
            atividades = self.crud_bd_inscricoes.listar_atividades_por_participante(id_participante)
            
            if not atividades:
                print(f"O participante {participante.nome} não está inscrito em nenhuma atividade.")
                return False
            
            print(f"\nAtividades em que {participante.nome} está inscrito:")
            for atividade in atividades:
                evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
                nome_evento = evento.nome if evento else "Evento não encontrado"
                print(f"[{atividade.id}] {atividade.nome} | Evento: {nome_evento}")
            
            id_atividade = input("\nDigite o ID da atividade para cancelar a inscrição: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            
            id_atividade = int(id_atividade)
            atividade = self.crud_bd_atividades.ler_atividade_por_id(id_atividade)
            
            if not atividade:
                print(f"Nenhuma atividade encontrada com ID {id_atividade}.")
                return False
            
            if not self.crud_bd_inscricoes.verificar_inscricao_atividade(id_participante, id_atividade):
                print(f"O participante {participante.nome} não está inscrito na atividade {atividade.nome}.")
                return False
            
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            nome_evento = evento.nome if evento else "Evento não encontrado"
            
            print(f"\nInscrição a ser cancelada:")
            print(f"Participante: {participante.nome}")
            print(f"Atividade: {atividade.nome}")
            print(f"Evento: {nome_evento}")
            
            confirmar = input("\nTem certeza de que deseja cancelar esta inscrição? (s/n): ")
            
            if confirmar.lower() == 's':
                sucesso = self.crud_bd_inscricoes.deletar_inscricao_por_participante_atividade(id_participante, id_atividade)
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