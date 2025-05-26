#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta, date, time

sys.path.append('.')

from compartilhado.gerenciador_bd import GerenciadorBD

def main():
    print("=" * 50)
    print("         RESET DATABASE - CRUD EVENTOS")
    print("=" * 50)
    print()
    
    db_path = "crud-eventos.db"
    if os.path.exists(db_path):
        print("Removendo banco de dados existente...")
        os.remove(db_path)
        print("Banco de dados removido com sucesso!")
    else:
        print("Nenhum banco de dados existente encontrado.")
    
    print()
    print("Criando novo banco de dados com dados iniciais...")
    
    gerenciador = GerenciadorBD(db_path)
    
    print("Inserindo dados iniciais...")
    
    eventos_exemplo = [
        (
            'Conferência de Tecnologia 2025',
            'Grande evento sobre as últimas tendências em tecnologia',
            '2025-06-15',
            '08:00',
            '2025-06-15',
            '18:00',
            'adulto',
            'presencial',
            'Centro de Convenções Tech, Av. Tecnologia, 123 - São Paulo/SP',
            500
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
            None
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
            INSERT INTO participantes (nome, cpf, email, telefone, data_cadastro)
            VALUES (?, ?, ?, ?, ?)
        ''', participante)
    
    atividades_exemplo = [
        ('Palestra: O Futuro da IA', 'Dr. João Tech', 'Auditório Principal', 1, '09:00', 100),
        ('Workshop: Machine Learning', 'Prof. Maria Data', 'Sala de Workshops A', 1, '14:00', 50),
        ('Mesa Redonda: Startups', 'Painel de CEOs', 'Sala de Conferências', 1, '16:00', 80),
        ('Introdução ao Python', 'Prof. Carlos Code', 'Laboratório 1', 2, '09:00', 25),
        ('Python Avançado', 'Prof. Ana Script', 'Laboratório 2', 2, '14:00', 25),
        ('Apresentação de Startups', 'Empreendedores Locais', 'Auditório Central', 3, '14:00', 50),
        ('Networking', 'Organizadores', 'Hall de Entrada', 3, '17:00', 200),
        ('Desenvolvimento de Apps', 'Mentores Tech', 'Laboratório de Desenvolvimento', 4, '18:00', 50),
        ('Pitch Final', 'Banca Avaliadora', 'Auditório Principal', 4, '16:00', 100),
        ('Palestra Principal', 'Dr. Roberto IA', 'Teatro Municipal', 5, '19:00', 300),
        ('Módulo 1: HTML Básico', 'Prof. Web Master', 'Plataforma Online', 6, '19:00', 0),
        ('Módulo 2: CSS Avançado', 'Prof. Style Expert', 'Plataforma Online', 6, '19:00', 0),
        ('Projeto Final', 'Mentores Online', 'Plataforma Online', 6, '20:00', 0),
        ('Experimentos Divertidos', 'Cientista Maluco', 'Laboratório Infantil', 7, '09:00', 30),
        ('Construindo Vulcões', 'Prof. Geologia Kids', 'Área Externa', 7, '11:00', 25),
        ('Show de Química', 'Dr. Reação', 'Anfiteatro', 7, '14:00', 80),
        ('Programação para Iniciantes', 'Coach Teen Tech', 'Sala de Computadores', 8, '14:00', 40),
        ('Criando Jogos', 'Game Master Jr', 'Laboratório de Jogos', 8, '09:00', 40),
        ('Carreira em Desenvolvimento', 'Senior Developer', 'Plataforma Zoom', 9, '20:00', 0),
        ('Montagem de Robôs', 'Eng. Robô Silva', 'Laboratório de Robótica', 10, '09:00', 15),
        ('Programação Arduino', 'Tech Arduino Master', 'Sala de Eletrônica', 10, '14:00', 15)
    ]
    
    for atividade in atividades_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO atividades (nome, facilitador, local, id_evento, hora_inicio, vagas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', atividade)
    
    inscricoes_exemplo = [
        (1, 1, '2025-05-20 10:30:00'),
        (1, 2, '2025-05-20 10:35:00'),
        (2, 1, '2025-05-20 11:00:00'),
        (2, 4, '2025-05-21 09:00:00'),
        (3, 4, '2025-05-21 09:15:00'),
        (3, 5, '2025-05-21 09:20:00'),
        (4, 6, '2025-05-21 14:30:00'),
        (4, 7, '2025-05-21 14:35:00'),
        (5, 8, '2025-05-22 08:00:00'),
        (6, 1, '2025-05-22 11:30:00'),
        (7, 10, '2025-05-23 12:00:00'),
        (8, 2, '2025-05-23 15:30:00'),
        (9, 8, '2025-05-24 08:30:00'),
        (10, 9, '2025-05-24 09:00:00'),
        (11, 11, '2025-05-25 19:30:00'),
        (11, 12, '2025-05-25 19:35:00'),
        (12, 14, '2025-05-25 08:30:00'),
        (12, 15, '2025-05-25 10:30:00'),
        (13, 17, '2025-05-26 13:30:00'),
        (13, 18, '2025-05-26 08:30:00'),
        (14, 19, '2025-05-26 19:45:00'),
        (15, 20, '2025-05-27 08:30:00'),
        (15, 21, '2025-05-27 13:30:00')
    ]
    
    for inscricao in inscricoes_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO inscricoes (id_participante, id_atividade, data_inscricao)
            VALUES (?, ?, ?)
        ''', inscricao)
    
    gerenciador.conn.commit()
    
    print("Dados iniciais inseridos com sucesso!")
    
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
    
    print(f'\nEventos por tipo:')
    gerenciador.cursor.execute('''
        SELECT tipo, COUNT(*) 
        FROM eventos 
        GROUP BY tipo
    ''')
    tipos_stats = gerenciador.cursor.fetchall()
    
    for tipo, count in tipos_stats:
        print(f'  - {tipo.capitalize()}: {count} evento(s)')
    
    print(f'\nEventos por público-alvo:')
    gerenciador.cursor.execute('''
        SELECT publico_alvo, COUNT(*) 
        FROM eventos 
        GROUP BY publico_alvo
    ''')
    publico_stats = gerenciador.cursor.fetchall()
    
    for publico, count in publico_stats:
        print(f'  - {publico.capitalize()}: {count} evento(s)')
    
    print(f'\nAtividades por local (top 5):')
    gerenciador.cursor.execute('''
        SELECT local, COUNT(*) as count
        FROM atividades 
        GROUP BY local
        ORDER BY count DESC
        LIMIT 5
    ''')
    local_stats = gerenciador.cursor.fetchall()
    
    for local, count in local_stats:
        print(f'  - {local}: {count} atividade(s)')
    
    gerenciador.fechar()
    
    print("\n" + "=" * 50)
    print("         RESET CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print("\nO banco de dados foi resetado e populado com dados de exemplo.")
    print("Dados incluídos:")
    print("  ✅ 10 eventos diversos (presenciais e online)")
    print("  ✅ 15 participantes")
    print("  ✅ 21 atividades com locais específicos")
    print("  ✅ 23 inscrições")
    print("\nTipos de eventos:")
    print("  🏢 Presenciais: conferências, workshops, seminários")
    print("  💻 Online: cursos e webinars")
    print("  👥 Públicos: adulto, juvenil, infantil")
    print("\nNova estrutura de atividades:")
    print("  📍 Campo 'local' adicionado a todas as atividades")
    print("  🎯 Locais específicos para cada tipo de atividade")
    print("  🔗 Relacionamento com eventos mantido via id_evento")
    print("\nVocê pode agora executar o programa principal com: python main.py")

if __name__ == "__main__":
    main()
