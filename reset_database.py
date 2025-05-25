#!/usr/bin/env python3
"""
Script para resetar o banco de dados e inserir dados iniciais
CRUD Eventos - Sistema de Gerenciamento de Eventos
"""

import os
import sys
from datetime import datetime, timedelta, date, time

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append('.')

from compartilhado.gerenciador_bd import GerenciadorBD

def main():
    print("=" * 50)
    print("         RESET DATABASE - CRUD EVENTOS")
    print("=" * 50)
    print()
    
    # Verificar se o banco existe e removê-lo
    db_path = "crud-eventos.db"
    if os.path.exists(db_path):
        print("Removendo banco de dados existente...")
        os.remove(db_path)
        print("Banco de dados removido com sucesso!")
    else:
        print("Nenhum banco de dados existente encontrado.")
    
    print()
    print("Criando novo banco de dados com dados iniciais...")
    
    # Inicializar o gerenciador (isso criará as tabelas)
    gerenciador = GerenciadorBD(db_path)
    
    print("Inserindo dados iniciais...")
    
    # Inserir eventos de exemplo com nova estrutura
    eventos_exemplo = [
        (
            'Conferência de Tecnologia 2025',
            'Grande evento sobre as últimas tendências em tecnologia',
            '2025-06-15',  # data_inicio
            '08:00',       # hora_inicio
            '2025-06-15',  # data_fim
            '18:00',       # hora_fim
            'adulto',      # publico_alvo
            'presencial',  # tipo
            'Centro de Convenções Tech, Av. Tecnologia, 123 - São Paulo/SP',  # endereco
            500            # capacidade
        ),
        (
            'Workshop de Python',
            'Curso intensivo de programação Python para iniciantes',
            '2025-06-20',
            '09:00',
            '2025-06-20',
            '17:00',
            'adulto',
            'presencial',
            'Laboratório de Informática - UFPE, Rua da Universidade, 456 - Recife/PE',
            50
        ),
        (
            'Seminário de Inovação',
            'Discussões sobre inovação e empreendedorismo',
            '2025-07-10',
            '14:00',
            '2025-07-10',
            '18:00',
            'adulto',
            'presencial',
            'Auditório Central, Rua Inovação, 789 - Recife/PE',
            200
        ),
        (
            'Hackathon 48h',
            'Maratona de programação de 48 horas',
            '2025-07-25',
            '18:00',
            '2025-07-27',
            '18:00',
            'adulto',
            'presencial',
            'Campus Universitário, Av. Universidade, 321 - Recife/PE',
            100
        ),
        (
            'Palestra: IA e Futuro',
            'Discussão sobre Inteligência Artificial e seus impactos',
            '2025-08-05',
            '19:00',
            '2025-08-05',
            '21:00',
            'adulto',
            'presencial',
            'Teatro Municipal, Praça Central, 111 - Recife/PE',
            300
        ),
        (
            'Curso Online: Desenvolvimento Web',
            'Curso completo de desenvolvimento web com HTML, CSS e JavaScript',
            '2025-06-01',
            '19:00',
            '2025-06-30',
            '21:00',
            'adulto',
            'online',
            'Online',
            None  # capacidade ilimitada para online
        ),
        (
            'Festival Infantil de Ciências',
            'Atividades lúdicas e educativas sobre ciências para crianças',
            '2025-09-15',
            '08:00',
            '2025-09-15',
            '17:00',
            'infantil',
            'presencial',
            'Parque da Ciência, Rua das Descobertas, 555 - Recife/PE',
            150
        ),
        (
            'Encontro Juvenil de Programação',
            'Workshop de programação voltado para adolescentes',
            '2025-08-20',
            '14:00',
            '2025-08-21',
            '17:00',
            'juvenil',
            'presencial',
            'Centro Juvenil de Tecnologia, Av. Juventude, 888 - Recife/PE',
            80
        ),
        (
            'Webinar: Carreira em Tech',
            'Palestra online sobre oportunidades de carreira na área de tecnologia',
            '2025-07-30',
            '20:00',
            '2025-07-30',
            '21:30',
            'adulto',
            'online',
            'Online',
            None
        ),
        (
            'Oficina de Robótica',
            'Construção e programação de robôs para iniciantes',
            '2025-08-10',
            '09:00',
            '2025-08-12',
            '16:00',
            'juvenil',
            'presencial',
            'Laboratório de Robótica, Rua dos Inventores, 999 - Recife/PE',
            30
        )
    ]
    
    for evento in eventos_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO eventos (nome, descricao, data_inicio, hora_inicio, data_fim, hora_fim, 
                               publico_alvo, tipo, endereco, capacidade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', evento)
    
    # Inserir participantes de exemplo
    participantes_exemplo = [
        ('João Silva Santos', '123.456.789-01', 'joao.silva@email.com', '(81) 99999-1111', '2025-05-20'),
        ('Maria Oliveira Costa', '234.567.890-12', 'maria.oliveira@email.com', '(81) 99999-2222', '2025-05-20'),
        ('Pedro Santos Lima', '345.678.901-23', 'pedro.santos@email.com', '(81) 99999-3333', '2025-05-21'),
        ('Ana Carolina Souza', '456.789.012-34', 'ana.souza@email.com', '(81) 99999-4444', '2025-05-21'),
        ('Carlos Eduardo Pereira', '567.890.123-45', 'carlos.pereira@email.com', '(81) 99999-5555', '2025-05-22'),
        ('Fernanda Lima Ribeiro', '678.901.234-56', 'fernanda.lima@email.com', '(81) 99999-6666', '2025-05-22'),
        ('Ricardo Alves Nunes', '789.012.345-67', 'ricardo.alves@email.com', '(81) 99999-7777', '2025-05-23'),
        ('Juliana Ferreira Costa', '890.123.456-78', 'juliana.ferreira@email.com', '(81) 99999-8888', '2025-05-23'),
        ('Bruno Henrique Silva', '901.234.567-89', 'bruno.henrique@email.com', '(81) 99999-9999', '2025-05-24'),
        ('Camila Santos Rodrigues', '012.345.678-90', 'camila.santos@email.com', '(81) 99999-0000', '2025-05-24'),
        ('Lucas Martins Pereira', '111.222.333-44', 'lucas.martins@email.com', '(81) 98888-1111', '2025-05-25'),
        ('Isabella Costa Lima', '222.333.444-55', 'isabella.costa@email.com', '(81) 98888-2222', '2025-05-25'),
        ('Gabriel Santos Nunes', '333.444.555-66', 'gabriel.santos@email.com', '(81) 98888-3333', '2025-05-26'),
        ('Sophia Oliveira Silva', '444.555.666-77', 'sophia.oliveira@email.com', '(81) 98888-4444', '2025-05-26'),
        ('Rafael Lima Costa', '555.666.777-88', 'rafael.lima@email.com', '(81) 98888-5555', '2025-05-27')
    ]
    
    for participante in participantes_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO participantes (nome, cpf, email, telefone, data)
            VALUES (?, ?, ?, ?, ?)
        ''', participante)
    
    # Inserir atividades de exemplo
    atividades_exemplo = [
        # Atividades para Conferência de Tecnologia (id_evento = 1)
        ('Palestra: O Futuro da IA', 'Dr. João Tech', 1, '09:00', 100),
        ('Workshop: Machine Learning', 'Prof. Maria Data', 1, '14:00', 50),
        ('Mesa Redonda: Startups', 'Painel de CEOs', 1, '16:00', 80),
        
        # Atividades para Workshop de Python (id_evento = 2)
        ('Introdução ao Python', 'Prof. Carlos Code', 2, '09:00', 25),
        ('Python Avançado', 'Prof. Ana Script', 2, '14:00', 25),
        
        # Atividades para Seminário de Inovação (id_evento = 3)
        ('Apresentação de Startups', 'Empreendedores Locais', 3, '14:00', 50),
        ('Networking', 'Organizadores', 3, '17:00', 200),
        
        # Atividades para Hackathon (id_evento = 4)
        ('Desenvolvimento de Apps', 'Mentores Tech', 4, '18:00', 50),
        ('Pitch Final', 'Banca Avaliadora', 4, '16:00', 100),
        
        # Atividades para Palestra IA (id_evento = 5)
        ('Palestra Principal', 'Dr. Roberto IA', 5, '19:00', 300),
        
        # Atividades para Curso Online (id_evento = 6)
        ('Módulo 1: HTML Básico', 'Prof. Web Master', 6, '19:00', None),
        ('Módulo 2: CSS Avançado', 'Prof. Style Expert', 6, '19:00', None),
        ('Projeto Final', 'Mentores Online', 6, '20:00', None),
        
        # Atividades para Festival Infantil (id_evento = 7)
        ('Experimentos Divertidos', 'Cientista Maluco', 7, '09:00', 30),
        ('Construindo Vulcões', 'Prof. Geologia Kids', 7, '11:00', 25),
        ('Show de Química', 'Dr. Reação', 7, '14:00', 80),
        
        # Atividades para Encontro Juvenil (id_evento = 8)
        ('Programação para Iniciantes', 'Coach Teen Tech', 8, '14:00', 40),
        ('Criando Jogos', 'Game Master Jr', 8, '09:00', 40),
        
        # Atividades para Webinar (id_evento = 9)
        ('Carreira em Desenvolvimento', 'Senior Developer', 9, '20:00', None),
        
        # Atividades para Oficina de Robótica (id_evento = 10)
        ('Montagem de Robôs', 'Eng. Robô Silva', 10, '09:00', 15),
        ('Programação Arduino', 'Tech Arduino Master', 10, '14:00', 15)
    ]
    
    for atividade in atividades_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO atividades (nome, facilitador, id_evento, hora_inicio, vagas)
            VALUES (?, ?, ?, ?, ?)
        ''', atividade)
    
    # Inserir inscrições de exemplo
    inscricoes_exemplo = [
        # Inscrições para diferentes atividades
        (1, 1, '2025-05-20 10:30:00'),   # João na Palestra IA
        (1, 2, '2025-05-20 10:35:00'),   # João no Workshop ML
        (2, 1, '2025-05-20 11:00:00'),   # Maria na Palestra IA
        (2, 4, '2025-05-21 09:00:00'),   # Maria no Python Intro
        (3, 4, '2025-05-21 09:15:00'),   # Pedro no Python Intro
        (3, 5, '2025-05-21 09:20:00'),   # Pedro no Python Avançado
        (4, 6, '2025-05-21 14:30:00'),   # Ana na apresentação de startups
        (4, 7, '2025-05-21 14:35:00'),   # Ana no networking
        (5, 8, '2025-05-22 08:00:00'),   # Carlos no desenvolvimento de apps
        (6, 1, '2025-05-22 11:30:00'),   # Fernanda na Palestra IA
        (7, 10, '2025-05-23 12:00:00'),  # Ricardo na Palestra Principal
        (8, 2, '2025-05-23 15:30:00'),   # Juliana no Workshop ML
        (9, 8, '2025-05-24 08:30:00'),   # Bruno no desenvolvimento de apps
        (10, 9, '2025-05-24 09:00:00'),  # Camila no Pitch Final
        (11, 11, '2025-05-25 19:30:00'), # Lucas no HTML Básico
        (11, 12, '2025-05-25 19:35:00'), # Lucas no CSS Avançado
        (12, 14, '2025-05-25 08:30:00'), # Isabella nos Experimentos
        (12, 15, '2025-05-25 10:30:00'), # Isabella nos Vulcões
        (13, 17, '2025-05-26 13:30:00'), # Gabriel na Programação Teen
        (13, 18, '2025-05-26 08:30:00'), # Gabriel nos Jogos
        (14, 19, '2025-05-26 19:45:00'), # Sophia no Webinar
        (15, 20, '2025-05-27 08:30:00'), # Rafael na Montagem
        (15, 21, '2025-05-27 13:30:00')  # Rafael no Arduino
    ]
    
    for inscricao in inscricoes_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO inscricoes (id_participante, id_atividade, data_inscricao)
            VALUES (?, ?, ?)
        ''', inscricao)
    
    # Confirmar todas as alterações
    gerenciador.conn.commit()
    
    print("Dados iniciais inseridos com sucesso!")
    
    # Exibir estatísticas
    gerenciador.cursor.execute('SELECT COUNT(*) FROM eventos')
    total_eventos = gerenciador.cursor.fetchone()[0]
    
    gerenciador.cursor.execute('SELECT COUNT(*) FROM participantes')
    total_participantes = gerenciador.cursor.fetchone()[0]
    
    gerenciador.cursor.execute('SELECT COUNT(*) FROM atividades')
    total_atividades = gerenciador.cursor.fetchone()[0]
    
    gerenciador.cursor.execute('SELECT COUNT(*) FROM inscricoes')
    total_inscricoes = gerenciador.cursor.fetchone()[0]
    
    print(f'\nEstatísticas do banco de dados:')
    print(f'  - Eventos: {total_eventos}')
    print(f'  - Participantes: {total_participantes}')
    print(f'  - Atividades: {total_atividades}')
    print(f'  - Inscrições: {total_inscricoes}')
    
    # Mostrar alguns exemplos de eventos criados
    print(f'\nExemplos de eventos criados:')
    gerenciador.cursor.execute('''
        SELECT id, nome, data_inicio, tipo, publico_alvo 
        FROM eventos 
        ORDER BY data_inicio 
        LIMIT 5
    ''')
    eventos_exemplo_resultado = gerenciador.cursor.fetchall()
    
    for evento in eventos_exemplo_resultado:
        id_evento, nome, data_inicio, tipo, publico_alvo = evento
        print(f'  {id_evento}. {nome} - {data_inicio} ({tipo}, {publico_alvo})')
    
    # Mostrar estatísticas por tipo
    print(f'\nEventos por tipo:')
    gerenciador.cursor.execute('''
        SELECT tipo, COUNT(*) 
        FROM eventos 
        GROUP BY tipo
    ''')
    tipos_stats = gerenciador.cursor.fetchall()
    
    for tipo, count in tipos_stats:
        print(f'  - {tipo.capitalize()}: {count} evento(s)')
    
    # Mostrar estatísticas por público-alvo
    print(f'\nEventos por público-alvo:')
    gerenciador.cursor.execute('''
        SELECT publico_alvo, COUNT(*) 
        FROM eventos 
        GROUP BY publico_alvo
    ''')
    publico_stats = gerenciador.cursor.fetchall()
    
    for publico, count in publico_stats:
        print(f'  - {publico.capitalize()}: {count} evento(s)')
    
    gerenciador.fechar()
    
    print("\n" + "=" * 50)
    print("         RESET CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print("\nO banco de dados foi resetado e populado com dados de exemplo.")
    print("Dados incluídos:")
    print("  ✅ 10 eventos diversos (presenciais e online)")
    print("  ✅ 15 participantes")
    print("  ✅ 21 atividades")
    print("  ✅ 23 inscrições")
    print("\nTipos de eventos:")
    print("  🏢 Presenciais: conferências, workshops, seminários")
    print("  💻 Online: cursos e webinars")
    print("  👥 Públicos: adulto, juvenil, infantil")
    print("\nVocê pode agora executar o programa principal com: python main.py")

if __name__ == "__main__":
    main()
