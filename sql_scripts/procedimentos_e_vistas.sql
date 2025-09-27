-- ============================================================================
-- PROCEDIMENTOS PARA REGISTO DE DADOS
-- ============================================================================

-- Procedimento para inserir Cliente
CREATE OR REPLACE FUNCTION inserir_cliente(
    p_nome VARCHAR(100),
    p_email VARCHAR(254),
    p_telefone VARCHAR(20),
    p_morada VARCHAR(200)
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    cliente_id INTEGER;
BEGIN
    -- Verificar se o email já existe
    IF EXISTS (SELECT 1 FROM ficha3_cliente WHERE email = p_email) THEN
        RAISE EXCEPTION 'Email % já existe na base de dados', p_email;
    END IF;
    
    -- Inserir o cliente e retornar o ID
    INSERT INTO ficha3_cliente (nome, email, telefone, morada, data_registo)
    VALUES (p_nome, p_email, p_telefone, p_morada, NOW())
    RETURNING id INTO cliente_id;
    
    RAISE NOTICE 'Cliente % inserido com sucesso. ID: %', p_nome, cliente_id;
    RETURN cliente_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao inserir cliente: %', SQLERRM;
END;
$$;

-- Procedimento para inserir Local
CREATE OR REPLACE FUNCTION inserir_local(
    p_nome VARCHAR(100),
    p_morada VARCHAR(200),
    p_capacidade INTEGER,
    p_contacto VARCHAR(50)
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    local_id INTEGER;
BEGIN
    -- Validar capacidade
    IF p_capacidade <= 0 THEN
        RAISE EXCEPTION 'A capacidade deve ser maior que zero';
    END IF;
    
    -- Inserir o local e retornar o ID
    INSERT INTO ficha3_local (nome, morada, capacidade, contacto)
    VALUES (p_nome, p_morada, p_capacidade, p_contacto)
    RETURNING id INTO local_id;
    
    RAISE NOTICE 'Local % inserido com sucesso. ID: %', p_nome, local_id;
    RETURN local_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao inserir local: %', SQLERRM;
END;
$$;

-- ============================================================================
-- VISTAS
-- ============================================================================

-- Vista para listar clientes com informações resumidas
CREATE OR REPLACE VIEW vista_clientes AS
SELECT 
    id,
    nome,
    email,
    telefone,
    LEFT(morada, 50) || CASE 
        WHEN LENGTH(morada) > 50 THEN '...' 
        ELSE '' 
    END AS morada_resumida,
    DATE(data_registo) as data_registo,
    EXTRACT(DAYS FROM NOW() - data_registo) as dias_desde_registo,
    (SELECT COUNT(*) FROM ficha3_bilhete WHERE cliente_id = ficha3_cliente.id) as total_bilhetes
FROM ficha3_cliente
ORDER BY data_registo DESC;

-- Vista para listar locais com estatísticas de utilização
CREATE OR REPLACE VIEW vista_locais AS
SELECT 
    l.id,
    l.nome,
    l.morada,
    l.capacidade,
    l.contacto,
    COALESCE(s.total_sessoes, 0) as total_sessoes,
    COALESCE(s.proximas_sessoes, 0) as sessoes_futuras,
    CASE 
        WHEN l.capacidade < 100 THEN 'Pequeno'
        WHEN l.capacidade < 500 THEN 'Médio'
        WHEN l.capacidade < 1000 THEN 'Grande'
        ELSE 'Muito Grande'
    END as categoria_tamanho
FROM ficha3_local l
LEFT JOIN (
    SELECT 
        local_id,
        COUNT(*) as total_sessoes,
        COUNT(CASE WHEN inicio > NOW() THEN 1 END) as proximas_sessoes
    FROM ficha3_sessao
    GROUP BY local_id
) s ON l.id = s.local_id
ORDER BY l.nome;

-- ============================================================================
-- EXEMPLOS DE USO DOS PROCEDIMENTOS
-- ============================================================================

-- Exemplos comentados para testar os procedimentos:
/*
-- Inserir cliente
SELECT inserir_cliente('João Silva', 'joao@exemplo.com', '912345678', 'Rua das Flores, 123, Lisboa');

-- Inserir local  
SELECT inserir_local('Teatro Nacional', 'Praça Dom Pedro IV, Lisboa', 800, 'info@teatro.pt');

-- Consultar vistas
SELECT * FROM vista_clientes;
SELECT * FROM vista_locais;
*/