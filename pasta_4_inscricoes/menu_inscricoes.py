import os
from pasta_4_inscricoes import CrudInscricoes
from compartilhado.formatador_tabela import FormatadorTabela

class MenuInscricoes:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
        self.crud_inscricoes = CrudInscricoes(gerenciador_bd)
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE INSCRIÇÕES =====")
        print("1. Adicionar inscrição")
        print("2. Ver todas as inscrições")
        print("3. Ver inscrições por atividade")
        print("4. Ver inscrições por evento")
        print("5. Ver inscrições por participante")
        print("6. Ver detalhes de uma inscrição")
        print("7. Cancelar inscrição")
        print("0. Voltar ao menu principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
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
    
    def executar(self):
        while True:
            escolha = self.exibir_menu()
            self.limpar_tela()
            
            if escolha == '1':
                self.crud_inscricoes.adicionar_inscricao()
            elif escolha == '2':
                self.crud_inscricoes.ver_todas_inscricoes()
            elif escolha == '3':
                self.ver_inscricoes_por_atividade()
            elif escolha == '4':
                self.ver_inscricoes_por_evento()
            elif escolha == '5':
                self.ver_inscricoes_por_participante()
            elif escolha == '6':
                self.ver_detalhes_inscricao()
            elif escolha == '7':
                self.crud_inscricoes.cancelar_inscricao()
                
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
                
            else:
                input("Escolha inválida.")
            input("\nPressione Enter para continuar...")
