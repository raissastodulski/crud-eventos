from pasta_0_modelos.evento import Evento
import os
import datetime

class MenuEventos:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu(self):
        """Exibe as opções do menu de gerenciamento de eventos"""
        self.limpar_tela()
        print("\n===== GERENCIAMENTO DE EVENTOS =====")
        print("1. Adicionar Novo Evento")
        print("2. Ver Todos os Eventos")
        print("3. Ver Detalhes do Evento")
        print("4. Atualizar Evento")
        print("5. Excluir Evento")
        print("6. Buscar Eventos")
        print("0. Voltar ao Menu Principal")
        print("===================================")
        return input("Digite sua escolha: ")
    
    def executar(self):
        """Executa a interface do menu"""
        while True:
            escolha = self.exibir_menu()
            
            if escolha == '1':
                self.adicionar_evento()
            elif escolha == '2':
                self.ver_todos_eventos()
            elif escolha == '3':
                self.ver_detalhes_evento()
            elif escolha == '4':
                self.atualizar_evento()
            elif escolha == '5':
                self.excluir_evento()
            elif escolha == '6':
                self.buscar_eventos()
            elif escolha == '0':
                print("Voltando ao menu principal...")
                break
            else:
                input("Escolha inválida. Pressione Enter para continuar...")
    
    def adicionar_evento(self):
        """Adiciona um novo evento"""
        self.limpar_tela()
        print("\n===== ADICIONAR NOVO EVENTO =====")
        
        titulo = input("Digite o título do evento: ")
        descricao = input("Digite a descrição do evento: ")
        
        # Validação de data
        while True:
            data_str = input("Digite a data do evento (AAAA-MM-DD): ")
            try:
                # Valida o formato da data
                if data_str:
                    datetime.datetime.strptime(data_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Formato de data inválido. Use AAAA-MM-DD.")
        
        local = input("Digite o local do evento: ")
        
        evento = Evento(titulo=titulo, descricao=descricao, data=data_str, local=local)
        self.gerenciador_bd.criar_evento(evento)
        
        input("\nPressione Enter para continuar...")
    
    def ver_todos_eventos(self):
        """Ver todos os eventos"""
        self.limpar_tela()
        print("\n===== TODOS OS EVENTOS =====")
        
        eventos = self.gerenciador_bd.ler_todos_eventos()
        
        if not eventos:
            print("Nenhum evento encontrado.")
        else:
            for evento in eventos:
                print(evento)
        
        input("\nPressione Enter para continuar...")
    
    def ver_detalhes_evento(self):
        """Ver detalhes de um evento específico"""
        self.limpar_tela()
        print("\n===== DETALHES DO EVENTO =====")
        
        id_evento = input("Digite o ID do evento: ")
        if not id_evento.isdigit():
            print("ID inválido. Por favor, digite um número.")
            input("\nPressione Enter para continuar...")
            return
        
        evento = self.gerenciador_bd.ler_evento_por_id(int(id_evento))
        
        if evento:
            print("\nDetalhes do Evento:")
            print(f"ID: {evento.id}")
            print(f"Título: {evento.titulo}")
            print(f"Descrição: {evento.descricao}")
            print(f"Data: {evento.data}")
            print(f"Local: {evento.local}")
        else:
            print(f"Nenhum evento encontrado com ID {id_evento}")
        
        input("\nPressione Enter para continuar...")
    
    def atualizar_evento(self):
        """Atualizar um evento existente"""
        self.limpar_tela()
        print("\n===== ATUALIZAR EVENTO =====")
        
        id_evento = input("Digite o ID do evento para atualizar: ")
        if not id_evento.isdigit():
            print("ID inválido. Por favor, digite um número.")
            input("\nPressione Enter para continuar...")
            return
        
        evento = self.gerenciador_bd.ler_evento_por_id(int(id_evento))
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            input("\nPressione Enter para continuar...")
            return
        
        print("\nDetalhes Atuais do Evento:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        print(f"Local: {evento.local}")
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_titulo = input(f"Novo título [{evento.titulo}]: ")
        if novo_titulo:
            evento.titulo = novo_titulo
        
        nova_descricao = input(f"Nova descrição [{evento.descricao}]: ")
        if nova_descricao:
            evento.descricao = nova_descricao
        
        # Validação de data
        while True:
            nova_data = input(f"Nova data [{evento.data}] (AAAA-MM-DD): ")
            if not nova_data:
                break
            try:
                # Valida o formato da data
                datetime.datetime.strptime(nova_data, "%Y-%m-%d")
                evento.data = nova_data
                break
            except ValueError:
                print("Formato de data inválido. Use AAAA-MM-DD.")
        
        novo_local = input(f"Novo local [{evento.local}]: ")
        if novo_local:
            evento.local = novo_local
        
        sucesso = self.gerenciador_bd.atualizar_evento(evento)
        if not sucesso:
            print("Falha ao atualizar o evento.")
        
        input("\nPressione Enter para continuar...")
    
    def excluir_evento(self):
        """Excluir um evento"""
        self.limpar_tela()
        print("\n===== EXCLUIR EVENTO =====")
        
        id_evento = input("Digite o ID do evento para excluir: ")
        if not id_evento.isdigit():
            print("ID inválido. Por favor, digite um número.")
            input("\nPressione Enter para continuar...")
            return
        
        evento = self.gerenciador_bd.ler_evento_por_id(int(id_evento))
        
        if not evento:
            print(f"Nenhum evento encontrado com ID {id_evento}")
            input("\nPressione Enter para continuar...")
            return
        
        print("\nEvento a ser excluído:")
        print(f"ID: {evento.id}")
        print(f"Título: {evento.titulo}")
        print(f"Descrição: {evento.descricao}")
        print(f"Data: {evento.data}")
        print(f"Local: {evento.local}")
        
        confirmar = input("\nTem certeza de que deseja excluir este evento? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.gerenciador_bd.deletar_evento(int(id_evento))
            if not sucesso:
                print("Falha ao excluir o evento.")
        else:
            print("Exclusão cancelada.")
        
        input("\nPressione Enter para continuar...")
    
    def buscar_eventos(self):
        """Buscar eventos"""
        self.limpar_tela()
        print("\n===== BUSCAR EVENTOS =====")
        
        termo_busca = input("Digite o termo de busca: ")
        
        if not termo_busca:
            print("O termo de busca não pode estar vazio.")
            input("\nPressione Enter para continuar...")
            return
        
        eventos = self.gerenciador_bd.buscar_eventos(termo_busca)
        
        if not eventos:
            print(f"Nenhum evento encontrado correspondente a '{termo_busca}'.")
        else:
            print(f"\nEncontrados {len(eventos)} eventos correspondentes:")
            for evento in eventos:
                print(evento)
        
        input("\nPressione Enter para continuar...")