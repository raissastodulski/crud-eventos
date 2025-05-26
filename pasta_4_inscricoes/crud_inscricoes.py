from datetime import datetime
from .inscricao import Inscricao
from .crud_bd_inscricoes import CrudBdInscricoes
from pasta_2_eventos import CrudBdEventos
from pasta_1_participantes import CrudBdParticipantes
from pasta_3_atividades import CrudBdAtividades
from utils import FormatadorTabela

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
            dados_tabela = []
            for inscricao in inscricoes:
                participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
                atividade = self.crud_bd_atividades.ler_atividade_por_id(inscricao.id_atividade)
                
                nome_participante = participante.nome if participante else "Participante não encontrado"
                nome_atividade = atividade.nome if atividade else "Atividade não encontrada"
                
                evento = None
                if atividade:
                    evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
                
                nome_evento = evento.nome if evento else "Evento não encontrado"
                
                data_formatada = ""
                if inscricao.data_inscricao:
                    try:
                        if isinstance(inscricao.data_inscricao, str):
                            data_obj = datetime.strptime(inscricao.data_inscricao, "%Y-%m-%d %H:%M:%S")
                        else:
                            data_obj = inscricao.data_inscricao
                        data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
                    except:
                        data_formatada = str(inscricao.data_inscricao)
                
                dados_tabela.append([
                    inscricao.id,
                    FormatadorTabela.truncar_texto(nome_participante, 25),
                    FormatadorTabela.truncar_texto(nome_atividade, 30),
                    FormatadorTabela.truncar_texto(nome_evento, 25),
                    data_formatada
                ])
            
            cabecalhos = ["ID", "Participante", "Atividade", "Evento", "Data Inscrição"]
            larguras = [4, 25, 30, 25, 16]
            
            tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
            print(tabela)
            print(f"\nTotal: {len(inscricoes)} inscrição(ões)")
            
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
        
        print(f"\n📋 Inscrições para a atividade: {atividade.nome}")
        participantes = self.crud_bd_inscricoes.listar_participantes_por_atividade(id_atividade)
        
        if not participantes:
            print(f"Nenhuma inscrição encontrada para a atividade '{atividade.nome}'.")
            return []
        
        dados_tabela = []
        for participante in participantes:
            dados_tabela.append([
                participante.id,
                FormatadorTabela.truncar_texto(participante.nome, 30),
                FormatadorTabela.truncar_texto(participante.email or "", 35),
                FormatadorTabela.truncar_texto(participante.telefone or "", 15)
            ])
        
        cabecalhos = ["ID", "Nome", "Email", "Telefone"]
        larguras = [4, 30, 35, 15]
        
        tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
        print(tabela)
        print(f"\nTotal: {len(participantes)}/{atividade.vagas} vagas preenchidas")
        
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
        
        print(f"\n📋 Inscrições para o evento: {evento.nome}")
        participantes = self.crud_bd_inscricoes.listar_participantes_por_evento(id_evento)
        
        if not participantes:
            print(f"Nenhuma inscrição encontrada para o evento '{evento.nome}'.")
            return []
        
        dados_tabela = []
        for participante in participantes:
            dados_tabela.append([
                participante.id,
                FormatadorTabela.truncar_texto(participante.nome, 30),
                FormatadorTabela.truncar_texto(participante.email or "", 35),
                FormatadorTabela.truncar_texto(participante.telefone or "", 15)
            ])
        
        cabecalhos = ["ID", "Nome", "Email", "Telefone"]
        larguras = [4, 30, 35, 15]
        
        tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
        print(tabela)
        
        capacidade_info = evento.capacidade if evento.capacidade else "Ilimitada"
        print(f"\nTotal: {len(participantes)} participante(s) | Capacidade: {capacidade_info}")
        
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
        
        print(f"\n📋 Inscrições do participante: {participante.nome}")
        
        atividades = self.crud_bd_inscricoes.listar_atividades_por_participante(id_participante)
        
        if not atividades:
            print(f"Nenhuma inscrição encontrada para o participante '{participante.nome}'.")
            return []
        
        dados_tabela_atividades = []
        for atividade in atividades:
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            nome_evento = evento.nome if evento else "Evento não encontrado"
            
            dados_tabela_atividades.append([
                atividade.id,
                FormatadorTabela.truncar_texto(atividade.nome, 30),
                FormatadorTabela.truncar_texto(atividade.facilitador, 20),
                FormatadorTabela.truncar_texto(nome_evento, 25),
                atividade.data_inicio_formatada() if hasattr(atividade, 'data_inicio_formatada') else "N/A"
            ])
        
        cabecalhos_atividades = ["ID", "Atividade", "Facilitador", "Evento", "Data"]
        larguras_atividades = [4, 30, 20, 25, 12]
        
        tabela_atividades = FormatadorTabela.criar_tabela(dados_tabela_atividades, cabecalhos_atividades, larguras_atividades)
        print(f"\n🎯 Atividades inscritas:")
        print(tabela_atividades)
        
        eventos = self.crud_bd_inscricoes.listar_eventos_por_participante(id_participante)
        
        if eventos:
            dados_tabela_eventos = []
            for evento in eventos:
                data_exibicao = ""
                if hasattr(evento, 'data_inicio_formatada'):
                    data_exibicao = evento.data_inicio_formatada()
                elif hasattr(evento, 'data'):
                    data_exibicao = str(evento.data) if evento.data else "N/A"
                
                dados_tabela_eventos.append([
                    evento.id,
                    FormatadorTabela.truncar_texto(evento.nome, 35),
                    FormatadorTabela.truncar_texto(evento.local if hasattr(evento, 'local') else "N/A", 25),
                    data_exibicao
                ])
            
            cabecalhos_eventos = ["ID", "Evento", "Local", "Data"]
            larguras_eventos = [4, 35, 25, 12]
            
            tabela_eventos = FormatadorTabela.criar_tabela(dados_tabela_eventos, cabecalhos_eventos, larguras_eventos)
            print(f"\n📅 Eventos relacionados:")
            print(tabela_eventos)
        
        print(f"\nTotal: {len(atividades)} inscrição(ões) em atividades")
        
        return atividades
    
    def ver_detalhes_inscricao(self, id_inscricao=None):
        print("\n===== DETALHES DA INSCRIÇÃO =====")
        
        if id_inscricao is None:
            id_inscricao = input("Digite o ID da inscrição para ver detalhes: ")
            if not id_inscricao.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_inscricao = int(id_inscricao)
        
        inscricao = self.crud_bd_inscricoes.ler_inscricao_por_id(id_inscricao)
        if not inscricao:
            print(f"Nenhuma inscrição encontrada com ID {id_inscricao}.")
            return None
        
        participante = self.crud_bd_participantes.ler_participante_por_id(inscricao.id_participante)
        atividade = self.crud_bd_atividades.ler_atividade_por_id(inscricao.id_atividade)
        
        evento = None
        if atividade:
            evento = self.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
        
        data_formatada = ""
        if inscricao.data_inscricao:
            try:
                if isinstance(inscricao.data_inscricao, str):
                    data_obj = datetime.strptime(inscricao.data_inscricao, "%Y-%m-%d %H:%M:%S")
                else:
                    data_obj = inscricao.data_inscricao
                data_formatada = data_obj.strftime("%d/%m/%Y às %H:%M")
            except:
                data_formatada = str(inscricao.data_inscricao)
        
        dados_detalhes = {
            "ID da Inscrição": inscricao.id,
            "Data da Inscrição": data_formatada,
            "Participante": participante.nome if participante else "Não encontrado",
            "Email do Participante": participante.email if participante else "N/A",
            "Telefone do Participante": participante.telefone if participante else "N/A",
            "Atividade": atividade.nome if atividade else "Não encontrada",
            "Facilitador": atividade.facilitador if atividade else "N/A",
            "Local da Atividade": atividade.local if atividade else "N/A",
            "Evento": evento.nome if evento else "Não encontrado",
            "Local do Evento": evento.local if evento else "N/A"
        }
        
        if atividade and hasattr(atividade, 'data_inicio_formatada'):
            dados_detalhes["Data da Atividade"] = atividade.data_inicio_formatada()
        
        if atividade and hasattr(atividade, 'hora_inicio_formatada'):
            dados_detalhes["Hora da Atividade"] = atividade.hora_inicio_formatada()
        
        tabela_detalhes = FormatadorTabela.criar_tabela_detalhes(
            f"DETALHES DA INSCRIÇÃO (ID: {inscricao.id})",
            dados_detalhes
        )
        print(tabela_detalhes)
        
        return inscricao
    
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
    
    def mostrar_atividades_disponiveis(self):
        print("\n===== ATIVIDADES DISPONÍVEIS =====")
        
        atividades = self.crud_inscricoes.crud_bd_atividades.ler_todas_atividades()
        if not atividades:
            print("Nenhuma atividade cadastrada.")
            return []
        
        dados_tabela = []
        for atividade in atividades:
            evento = self.crud_inscricoes.crud_bd_eventos.ler_evento_por_id(atividade.id_evento)
            nome_evento = evento.nome if evento else "Evento não encontrado"
            
            participantes_inscritos = self.crud_inscricoes.crud_bd_inscricoes.contar_participantes_por_atividade(atividade.id)
            vagas_info = f"{participantes_inscritos}/{atividade.vagas}"
            
            dados_tabela.append([
                atividade.id,
                FormatadorTabela.truncar_texto(atividade.nome, 30),
                FormatadorTabela.truncar_texto(atividade.facilitador, 20),
                FormatadorTabela.truncar_texto(nome_evento, 25),
                vagas_info
            ])
        
        cabecalhos = ["ID", "Atividade", "Facilitador", "Evento", "Inscritos/Vagas"]
        larguras = [4, 30, 20, 25, 15]
        
        tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
        print(tabela)
        return atividades
    
    def mostrar_eventos_disponiveis(self):
        print("\n===== EVENTOS DISPONÍVEIS =====")
        
        eventos = self.crud_inscricoes.crud_bd_eventos.ler_todos_eventos()
        if not eventos:
            print("Nenhum evento cadastrado.")
            return []
        
        dados_tabela = []
        for evento in eventos:
            participantes_evento = self.crud_inscricoes.crud_bd_inscricoes.contar_participantes_por_evento(evento.id)
            capacidade_info = f"{participantes_evento}/{evento.capacidade}" if evento.capacidade else f"{participantes_evento}/Ilimitado"
            
            dados_tabela.append([
                evento.id,
                FormatadorTabela.truncar_texto(evento.nome, 35),
                evento.data_inicio_formatada() if hasattr(evento, 'data_inicio_formatada') else "N/A",
                FormatadorTabela.truncar_texto(evento.local, 25),
                capacidade_info
            ])
        
        cabecalhos = ["ID", "Evento", "Data", "Local", "Participantes/Cap."]
        larguras = [4, 35, 12, 25, 18]
        
        tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
        print(tabela)
        return eventos
    
    def mostrar_participantes_disponiveis(self):
        print("\n===== PARTICIPANTES DISPONÍVEIS =====")
        
        participantes = self.crud_inscricoes.crud_bd_participantes.ler_todos_participantes()
        if not participantes:
            print("Nenhum participante cadastrado.")
            return []
        
        dados_tabela = []
        for participante in participantes:
            atividades_participante = self.crud_inscricoes.crud_bd_inscricoes.listar_atividades_por_participante(participante.id)
            total_inscricoes = len(atividades_participante) if atividades_participante else 0
            
            dados_tabela.append([
                participante.id,
                FormatadorTabela.truncar_texto(participante.nome, 30),
                FormatadorTabela.truncar_texto(participante.email or "", 30),
                FormatadorTabela.truncar_texto(participante.telefone or "", 15),
                total_inscricoes
            ])
        
        cabecalhos = ["ID", "Nome", "Email", "Telefone", "Inscrições"]
        larguras = [4, 30, 30, 15, 10]
        
        tabela = FormatadorTabela.criar_tabela(dados_tabela, cabecalhos, larguras)
        print(tabela)
        return participantes
    
    def ver_inscricoes_por_atividade(self):
        self.limpar_tela()
        
        atividades = self.mostrar_atividades_disponiveis()
        if not atividades:
            return
        
        try:
            id_atividade = int(input("\nDigite o ID da atividade para ver suas inscrições: "))
            
            atividade_encontrada = any(ativ.id == id_atividade for ativ in atividades)
            if not atividade_encontrada:
                print(f"❌ Atividade com ID {id_atividade} não encontrada.")
                return
            
            self.limpar_tela()
            self.crud_inscricoes.ver_inscricoes_por_atividade(id_atividade)
            
        except ValueError:
            print("❌ ID inválido. Por favor, digite um número.")
    
    def ver_inscricoes_por_evento(self):
        self.limpar_tela()
        
        eventos = self.mostrar_eventos_disponiveis()
        if not eventos:
            return
        
        try:
            id_evento = int(input("\nDigite o ID do evento para ver suas inscrições: "))
            
            evento_encontrado = any(evt.id == id_evento for evt in eventos)
            if not evento_encontrado:
                print(f"❌ Evento com ID {id_evento} não encontrado.")
                return
            
            self.limpar_tela()
            self.crud_inscricoes.ver_inscricoes_por_evento(id_evento)
            
        except ValueError:
            print("❌ ID inválido. Por favor, digite um número.")
    
    def ver_inscricoes_por_participante(self):
        self.limpar_tela()
        
        participantes = self.mostrar_participantes_disponiveis()
        if not participantes:
            return
        
        try:
            id_participante = int(input("\nDigite o ID do participante para ver suas inscrições: "))
            
            participante_encontrado = any(part.id == id_participante for part in participantes)
            if not participante_encontrado:
                print(f"❌ Participante com ID {id_participante} não encontrado.")
                return
            
            self.limpar_tela()
            self.crud_inscricoes.ver_inscricoes_por_participante(id_participante)
            
        except ValueError:
            print("❌ ID inválido. Por favor, digite um número.")
    
    def ver_detalhes_inscricao(self):
        self.limpar_tela()
        
        inscricoes = self.crud_inscricoes.ver_todas_inscricoes()
        if not inscricoes:
            return
        
        try:
            id_inscricao = int(input("\nDigite o ID da inscrição para ver detalhes: "))
            
            inscricao_encontrada = any(insc.id == id_inscricao for insc in inscricoes)
            if not inscricao_encontrada:
                print(f"❌ Inscrição com ID {id_inscricao} não encontrada.")
                return
            
            self.limpar_tela()
            self.crud_inscricoes.ver_detalhes_inscricao(id_inscricao)
            
        except ValueError:
            print("❌ ID inválido. Por favor, digite um número.")
