from django.db import migrations
import os

SQL_DIR = os.path.join(os.path.dirname(__file__), '../sql')

SQL_FILES = [
    # (create_file, drop_file)
    ('create_criar_bilhete.sql', 'drop_criar_bilhete.sql'),
    ('create_criar_fatura.sql', 'drop_criar_fatura.sql'),
    ('create_bilhetes_elegiveis.sql', 'drop_bilhetes_elegiveis.sql'),
    ('create_faturas_com_bilhetes.sql', 'drop_faturas_com_bilhetes.sql'),
]

def read_sql(filename):
    path = os.path.join(SQL_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

def apply_sql_files(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        for create_file, _ in SQL_FILES:
            sql = read_sql(create_file)
            cursor.execute(sql)

def revert_sql_files(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        for _, drop_file in reversed(SQL_FILES):
            sql = read_sql(drop_file)
            cursor.execute(sql)

class Migration(migrations.Migration):
    dependencies = [
        ("ficha3", "0002_faturasitem"),
    ]
    operations = [
        migrations.RunPython(apply_sql_files, revert_sql_files),
    ]
