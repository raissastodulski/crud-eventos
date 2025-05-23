#!/usr/bin/env python3
"""
Script para resetar o banco de dados e inserir dados iniciais
CRUD Eventos - Sistema de Gerenciamento de Eventos
"""

import os
import sys
from datetime import datetime, timedelta

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
    
    # Inserir eventos de exemplo
    eventos_exemplo = [
        ('Conferência de Tecnologia 2025', 'Grande evento sobre as últimas tendências em tecnologia', '2025-06-15', '08:00', '18:00', 'Profissionais de TI', 500, 'Centro de Convenções Tech', 'Av. Tecnologia, 123 - São Paulo/SP'),
        ('Workshop de Python', 'Curso intensivo de programação Python para iniciantes', '2025-06-20', '09:00', '17:00', 'Estudantes e profissionais', 50, 'Laboratório de Informática - UFPE', 'Rua da Universidade, 456 - Recife/PE'),
        ('Seminário de Inovação', 'Discussões sobre inovação e empreendedorismo', '2025-07-10', '14:00', '18:00', 'Empreendedores', 200, 'Auditório Central', 'Rua Inovação, 789 - Recife/PE'),
        ('Hackathon 48h', 'Maratona de programação de 48 horas', '2025-07-25', '18:00', '18:00', 'Desenvolvedores', 100, 'Campus Universitário', 'Av. Universidade, 321 - Recife/PE'),
        ('Palestra: IA e Futuro', 'Discussão sobre Inteligência Artificial e seus impactos', '2025-08-05', '19:00', '21:00', 'Público geral', 300, 'Teatro Municipal', 'Praça Central, 111 - Recife/PE')
    ]
    
    for evento in eventos_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO eventos (titulo, descricao, data, hora_inicio, hora_fim, publico_alvo, capacidade, local, endereco)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        ('Camila Santos Rodrigues', '012.345.678-90', 'camila.santos@email.com', '(81) 99999-0000', '2025-05-24')
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
        ('Palestra Principal', 'Dr. Roberto IA', 5, '19:00', 300)
    ]
    
    for atividade in atividades_exemplo:
        gerenciador.cursor.execute('''
            INSERT INTO atividades (nome, facilitador, id_evento, hora_inicio, vagas)
            VALUES (?, ?, ?, ?, ?)
        ''', atividade)
    
    # Inserir inscrições de exemplo
    inscricoes_exemplo = [
        # Inscrições para diferentes atividades
        (1, 1, '2025-05-20 10:30:00'),  # João na Palestra IA
        (1, 2, '2025-05-20 10:35:00'),  # João no Workshop ML
        (2, 1, '2025-05-20 11:00:00'),  # Maria na Palestra IA
        (2, 4, '2025-05-21 09:00:00'),  # Maria no Python Intro
        (3, 4, '2025-05-21 09:15:00'),  # Pedro no Python Intro
        (3, 5, '2025-05-21 09:20:00'),  # Pedro no Python Avançado
        (4, 6, '2025-05-21 14:30:00'),  # Ana na apresentação de startups
        (4, 7, '2025-05-21 14:35:00'),  # Ana no networking
        (5, 8, '2025-05-22 08:00:00'),  # Carlos no desenvolvimento de apps
        (6, 1, '2025-05-22 11:30:00'),  # Fernanda na Palestra IA
        (7, 10, '2025-05-23 12:00:00'), # Ricardo na Palestra Principal
        (8, 2, '2025-05-23 15:30:00'),  # Juliana no Workshop ML
        (9, 8, '2025-05-24 08:30:00'),  # Bruno no desenvolvimento de apps
        (10, 9, '2025-05-24 09:00:00')  # Camila no Pitch Final
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
    
    gerenciador.fechar()
    
    print("\n" + "=" * 50)
    print("         RESET CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print("\nO banco de dados foi resetado e populado com dados de exemplo.")
    print("Você pode agora executar o programa principal com: python main.py")

if __name__ == "__main__":
    main()
