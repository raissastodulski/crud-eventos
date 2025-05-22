from pasta_3_atividades.activity import Activity
import datetime

class CrudActivity:
    def __init__(self, gerenciador_bd):
        self.gerenciador_bd = gerenciador_bd
    
    def adicionar_atividade(self):
        """Adiciona um novo evento"""
        print("\n===== ADICIONAR UMA NOVA ATIVIDADE =====")
        
        nome = input("\nDigite o nome da atividade: ")
        facilitador = input("Digite o nome do responsável da atividade: ")
        horario_str = input("Digite a hora que começa a atividade (hh:mm): ")
        horario = datetime.datetime.strptime(horario_str, "%H:%M").strftime("%H:%M")
        local = input("Digite o local da atividade: ")
        vagas = int(input("Digite a quantidade de vagas: "))

        
        activity = Activity(nome=nome, facilitador=facilitador, horario=horario, local=local, vagas=vagas)
        self.gerenciador_bd.criar_activity(activity)
        
        return True
    
    def ver_todas_atividades(self):
        
        print("\n===== TODOS AS ATIVIDADES =====")
        
        atividades = self.gerenciador_bd.ler_todas_atividades()
        
        if not atividades:
            print("Nenhuma atividade encontrada.")
            return []
        else:
            for atividade in atividades:
                print(atividade)
            return atividades
    
    def ver_detalhes_atividades(self, id_atividade=None):
        """Ver detalhes de um evento específico"""
        print("\n===== DETALHES DA ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return None
            id_atividade = int(id_atividade)
        
        atividade = self.gerenciador_bd.ler_atividade_por_id(id_atividade)
        
        if atividade:
            print("\nDetalhes da Atividade:")
            print(f"ID: {atividade.id}")
            print(f"Nome: {atividade.nome}")
            print(f"Facilitador: {atividade.facilitador}")
            print(f"Horário: {atividade.horario}")
            print(f"Local: {atividade.local}")
            print(f"Vagas: {atividade.vagas}")
            return atividade
        else:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return None
    
    def atualizar_atividade(self, id_atividade=None):
        """Atualizar um evento existente"""
        print("\n===== ATUALIZAR ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID de atividade para atualizar: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)
        
        atividade = self.gerenciador_bd.ler_atividade_por_id(id_atividade)
        
        if not atividade:
            print(f"Nenhuma atividade encontrada com ID {id_atividade}")
            return False
        
        print("\nDetalhes Atuais do Evento:")
        print(f"ID: {atividade.id}")
        print(f"Nome: {atividade.nome}")
        print(f"Facilitador: {atividade.facilitador}")
        print(f"Horário: {atividade.horario}")
        print(f"Local: {atividade.local}")
        print(f"Vagas: {atividade.vagas}")
        print("\nDigite os novos detalhes (deixe em branco para manter o valor atual):")
        
        novo_nome = input(f"Novo nome [{atividade.nome}]: ")
        if novo_nome:
            atividade.nome = novo_nome
        
        novo_facilitador = input(f"Novo facilitador [{atividade.facilitador}]: ")
        if novo_facilitador:
            atividade.facilitador = novo_facilitador
        
        novo_horario = input(f"Novo horário [{atividade.horario}]: ")
        if novo_horario:
            atividade.horario = novo_horario
        
        novo_local = input(f"Novo local [{atividade.local}]: ")
        if novo_local:
            atividade.local = novo_local
        
        novo_vagas = input(f"Quantidade de vagas [{atividade.vagas}]: ")
        if novo_vagas:
            atividade.vagas = novo_vagas

        sucesso = self.gerenciador_bd.atualizar_atividade(atividade)
        if not sucesso:
            print("Falha ao atualizar a atividade.")
            return False
        
        return True
    
    def excluir_atividade(self, id_atividade=None):
        """Excluir um evento"""
        print("\n===== EXCLUIR ATIVIDADE =====")
        
        if id_atividade is None:
            id_atividade = input("Digite o ID da atividade para excluir: ")
            if not id_atividade.isdigit():
                print("ID inválido. Por favor, digite um número.")
                return False
            id_atividade = int(id_atividade)
        
        atividade = self.gerenciador_bd.ler_atividade_por_id(id_atividade)
        
        if not atividade:
            print(f"Nenhuma atividade foi encontrada com ID {id_atividade}")
            return False
        
        print("\nEvento a ser excluído:")
        print(f"ID: {atividade.id}")
        print(f"Nome: {atividade.nome}")
        print(f"Facilitador: {atividade.facilitador}")
        print(f"Local: {atividade.local}")
        print(f"Horário: {atividade.horario}")
        print(f"Vagas: {atividade.vagas}")
        
        confirmar = input("\nTem certeza de que deseja excluir este evento? (s/n): ")
        
        if confirmar.lower() == 's':
            sucesso = self.gerenciador_bd.deletar_atividade(id_atividade)
            if not sucesso:
                print("Falha ao excluir a atividade.")
                return False
            return True
        else:
            print("Exclusão cancelada.")
            return False
    
    def buscar_atividade(self, termo_busca=None):
        """Buscar eventos"""
        print("\n===== BUSCAR ATIVIDADES =====")
        
        if termo_busca is None:
            termo_busca = input("Digite o termo de busca: ")
        
        if not termo_busca:
            print("O termo de busca não pode estar vazio.")
            return []
        
        atividades = self.gerenciador_bd.buscar_atividades(termo_busca)
        
        if not atividades:
            print(f"Nenhuma atividade encontrada correspondente a '{termo_busca}'.")
            return []
        else:
            print(f"\nEncontrados {len(atividades)} eventos correspondentes:")
            for atividade in atividades:
                print(atividade)
            return atividades