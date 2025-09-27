from django.db import migrations, connection

def populate_test_data(apps, schema_editor):
    # Remove all existing data (order matters due to FKs)
    with connection.cursor() as cursor:
        cursor.execute('''
            DELETE FROM ficha3_faturasitem;
            DELETE FROM ficha3_fatura;
            DELETE FROM ficha3_bilhete;
            DELETE FROM ficha3_sessao;
            DELETE FROM ficha3_artista;
            DELETE FROM ficha3_generoartista;
            DELETE FROM ficha3_evento;
            DELETE FROM ficha3_categoriaevento;
            DELETE FROM ficha3_local;
            DELETE FROM ficha3_organizador;
            DELETE FROM ficha3_cliente;
        ''')

    from datetime import datetime, timedelta
    now = datetime.now().isoformat(sep=' ', timespec='seconds')
    # Insert Organizadores
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_organizador (nome, email, telefone) VALUES
                ('Org1', 'org1@example.com', '+351900000001');
        """)
    # Insert Locais
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_local (nome, morada, capacidade, contacto) VALUES
                ('Local1', 'Rua Local 1', 100, '+351900000010');
        """)
    # Insert Categorias
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_categoriaevento (nome) VALUES
                ('Concerto');
        """)
    # Insert Evento
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO ficha3_evento (titulo, descricao, data_inicio, data_fim, organizador_id, ativo, categoria_id) VALUES
                ('Concerto X', 'Desc Concerto', '{now}', '{now}', 1, TRUE, 1);
        """)
    # Insert GeneroArtista
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_generoartista (nome) VALUES
                ('Pop');
        """)
    # Insert Artista
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_artista (nome, bio, genero_id) VALUES
                ('Artista1', 'Bio do artista', 1);
        """)
    # Insert Sessao
    sessao_inicio = (datetime.now() + timedelta(days=1)).isoformat(sep=' ', timespec='seconds')
    sessao_fim = (datetime.now() + timedelta(days=1, hours=2)).isoformat(sep=' ', timespec='seconds')
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO ficha3_sessao (evento_id, local_id, inicio, fim, preco) VALUES
                (1, 1, '{sessao_inicio}', '{sessao_fim}', 50.0);
        """)
    # Insert Clientes
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO ficha3_cliente (nome, email, telefone, morada, data_registo) VALUES
                ('Alice', 'alice@example.com', '+351111111111', 'Rua A, 1', '{now}'),
                ('Bob', 'bob@example.com', '+351222222222', 'Rua B, 2', '{now}'),
                ('Carol', 'carol@example.com', '+351333333333', 'Rua C, 3', '{now}');
        """)
    # Insert Fatura
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO ficha3_fatura (cliente_id, numero_unico, data_emissao, total, estado) VALUES
                (1, 'fatura-uuid-1', '{now}', 50.0, 'P'),
                (2, 'fatura-uuid-2', '{now}', 35.0, 'N');
        """)
    # Insert Bilhetes
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO ficha3_bilhete (sessao_id, cliente_id, codigo_unico, tipo, usado, comprado_em, preco_final, lugar) VALUES
                (1, 1, 'bilhete-uuid-1', 'NORMAL', FALSE, '{now}', 50.0, 'A1'),
                (1, 2, 'bilhete-uuid-2', 'ESTUDANTE', FALSE, '{now}', 35.0, 'A2'),
                (1, 3, 'bilhete-uuid-3', 'VIP', FALSE, '{now}', 45.0, 'B1');
        """)
    # Insert FaturasItem
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficha3_faturasitem (fatura_id, bilhete_id) VALUES
                (1, 1),
                (2, 2);
        """)
    # Reset sequences for all tables with serial PKs
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('ficha3_organizador', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_organizador;
            SELECT setval(pg_get_serial_sequence('ficha3_local', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_local;
            SELECT setval(pg_get_serial_sequence('ficha3_categoriaevento', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_categoriaevento;
            SELECT setval(pg_get_serial_sequence('ficha3_evento', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_evento;
            SELECT setval(pg_get_serial_sequence('ficha3_generoartista', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_generoartista;
            SELECT setval(pg_get_serial_sequence('ficha3_artista', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_artista;
            SELECT setval(pg_get_serial_sequence('ficha3_sessao', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_sessao;
            SELECT setval(pg_get_serial_sequence('ficha3_cliente', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_cliente;
            SELECT setval(pg_get_serial_sequence('ficha3_fatura', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_fatura;
            SELECT setval(pg_get_serial_sequence('ficha3_bilhete', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_bilhete;
            SELECT setval(pg_get_serial_sequence('ficha3_faturasitem', 'id'), COALESCE(MAX(id), 1), true) FROM ficha3_faturasitem;
        """)

def unpopulate_test_data(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('''
            DELETE FROM ficha3_faturasitem;
            DELETE FROM ficha3_fatura;
            DELETE FROM ficha3_bilhete;
            DELETE FROM ficha3_sessao;
            DELETE FROM ficha3_cliente;
        ''')

class Migration(migrations.Migration):
    dependencies = [
        ("ficha3", "0090_sql_objects_from_files"),
    ]
    operations = [
        migrations.RunPython(populate_test_data, unpopulate_test_data),
    ]
