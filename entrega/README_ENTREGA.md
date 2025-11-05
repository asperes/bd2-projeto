# Projeto BD II - Ficha 3
## Sistema de Bilheteira com Django + PostgreSQL

### Entidades Implementadas: Cliente e Local

**Aluno:** [Seu Nome]  
**Curso:** [Seu Curso]  
**Data:** 27 de Setembro 2025

---

## 📋 Requisitos Implementados

### ✅ b) Tabelas no PostgreSQL
- Tabela `ficha3_cliente` criada através das migrações Django
- Tabela `ficha3_local` criada através das migrações Django

### ✅ c) Procedimentos SQL (PL/pgSQL)
- `inserir_cliente(nome, email, telefone, morada)` → Retorna ID do cliente
- `inserir_local(nome, morada, capacidade, contacto)` → Retorna ID do local

### ✅ d) Vistas SQL
- `vista_clientes` → Lista clientes com estatísticas (dias desde registo, total bilhetes)
- `vista_locais` → Lista locais com estatísticas (sessões totais, futuras, categoria tamanho)

### ✅ e) Aplicação Django
- **Interface Web** completa com Bootstrap
- **Formulários** que utilizam os procedimentos SQL
- **Listagens** que utilizam as vistas SQL
- **Páginas de detalhes** para cada entidade
- **API JSON** disponível

---

## 🚀 Como Executar

### 1. Configurar Ambiente
```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Base de Dados
```bash
# Criar ficheiro .env com as suas credenciais PostgreSQL:
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=sua_bd
PG_USER=seu_user
PG_PASSWORD=sua_password
```

### 3. Executar Migrações
```bash
python manage.py migrate
```

### 4. Criar Procedimentos e Vistas SQL
```bash
# Executar o script SQL na sua base de dados:
psql -U seu_user -d sua_bd -f sql_scripts/procedimentos_e_vistas.sql
```

### 5. Iniciar Servidor
```bash
python manage.py runserver
```

### 6. Aceder à Aplicação
- **Página Principal:** http://127.0.0.1:8000/
- **Lista Clientes:** http://127.0.0.1:8000/clientes/
- **Lista Locais:** http://127.0.0.1:8000/locais/
- **Admin Django:** http://127.0.0.1:8000/admin/

---

## 📁 Estrutura do Projeto

```
bd2-projeto/
├── manage.py                 # Script principal Django
├── requirements.txt          # Dependências Python
├── bilheteira/              # Configurações Django
│   ├── settings.py          # Configurações (BD, apps, etc.)
│   ├── urls.py             # URLs principais
│   └── ...
├── ficha3/                  # App principal
│   ├── models.py           # Modelos (Cliente, Local, etc.)
│   ├── views.py            # Views (listagem, criação)
│   ├── forms.py            # Formulários Django
│   ├── urls.py             # URLs da app
│   ├── admin.py            # Configuração admin
│   ├── templates/          # Templates HTML
│   └── migrations/         # Migrações BD
└── sql_scripts/            # Scripts SQL
    └── procedimentos_e_vistas.sql
```

---

## 🔧 Funcionalidades Técnicas

### Procedimentos SQL
- **Validação de dados** (email único, capacidade > 0)
- **Tratamento de erros** com `RAISE EXCEPTION`
- **Retorno de IDs** dos registos criados
- **Mensagens informativos** com `RAISE NOTICE`

### Vistas SQL
- **Estatísticas calculadas** (dias desde registo, total bilhetes)
- **Joins** entre tabelas relacionadas
- **Categorização automática** (tamanho do local)
- **Agregações** (COUNT, etc.)

### Interface Django
- **Design responsivo** com Bootstrap 5
- **Paginação** nas listagens
- **Validação de formulários** client e server-side
- **Mensagens de feedback** para utilizador
- **Navigation breadcrumb** 

---

## 🎯 Pontos de Destaque

1. **Integração SQL-Django:** Procedimentos e vistas SQL utilizados diretamente nas views Django
2. **Validação Robusta:** Validações tanto no PostgreSQL como nos forms Django
3. **Interface Profissional:** Design moderno e responsivo
4. **Arquitetura Limpa:** Código bem organizado seguindo padrões Django
5. **Documentação Completa:** Scripts SQL bem comentados

---

**Nota:** Este projeto demonstra a integração entre Django ORM e SQL direto, utilizando o melhor dos dois mundos para criar uma aplicação robusta e performante.