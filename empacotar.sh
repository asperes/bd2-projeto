#!/bin/bash
# Script para empacotar a aplicação Django para envio

echo "🚀 Empacotando aplicação Django..."

# Criar diretório temporário
mkdir -p /tmp/bd2-projeto-entrega

# Copiar ficheiros essenciais
cp manage.py /tmp/bd2-projeto-entrega/
cp -r bilheteira /tmp/bd2-projeto-entrega/
cp -r ficha3 /tmp/bd2-projeto-entrega/
cp README.md /tmp/bd2-projeto-entrega/
cp -r sql_scripts /tmp/bd2-projeto-entrega/
cp .env.example /tmp/bd2-projeto-entrega/

# Criar ficheiro requirements.txt
echo "django>=4.2,<5.0" > /tmp/bd2-projeto-entrega/requirements.txt
echo "psycopg2-binary>=2.9.0" >> /tmp/bd2-projeto-entrega/requirements.txt
echo "python-dotenv>=0.19.0" >> /tmp/bd2-projeto-entrega/requirements.txt

echo "✅ Aplicação empacotada em: /tmp/bd2-projeto-entrega"
echo ""
echo "📁 Ficheiros incluídos:"
ls -la /tmp/bd2-projeto-entrega
echo ""
echo "🗂️ Estrutura das pastas:"
find /tmp/bd2-projeto-entrega -type d

echo ""
echo "💡 Para criar um ZIP:"
echo "cd /tmp && zip -r bd2-projeto-entrega.zip bd2-projeto-entrega/"