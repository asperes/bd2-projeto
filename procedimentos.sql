-- ====================================================================
-- PROCEDIMENTO 1: Registar Organizador
-- ====================================================================

CREATE OR REPLACE FUNCTION registar_organizador(
    nome VARCHAR(100),
    email VARCHAR(254),
    telefone VARCHAR(20)
)
RETURNS TABLE(
    organizador_id INTEGER,
    mensagem TEXT
) AS $$
DECLARE
    novo_organizador_id INTEGER;
    email_existe BOOLEAN;
BEGIN
    -- Verificar se o email já existe (unique constraint no modelo Django)
    SELECT EXISTS(SELECT 1 FROM ficha3_organizador WHERE email = registar_organizador.email) INTO email_existe;
    
    IF email_existe THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as organizador_id,
            'ERRO: Email já existe na base de dados.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Validações básicas
    IF nome IS NULL OR LENGTH(TRIM(nome)) = 0 THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as organizador_id,
            'ERRO: Nome é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    IF email IS NULL OR LENGTH(TRIM(email)) = 0 THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as organizador_id,
            'ERRO: Email é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Validação simples de formato de email
    IF email !~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as organizador_id,
            'ERRO: Formato de email inválido.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Inserir o novo organizador
    INSERT INTO ficha3_organizador (nome, email, telefone)
    VALUES (
        TRIM(nome),
        LOWER(TRIM(email)),
        COALESCE(TRIM(telefone), '')
    )
    RETURNING id INTO novo_organizador_id;
    
    -- Retornar sucesso
    RETURN QUERY SELECT 
        novo_organizador_id as organizador_id,
        format('SUCESSO: Organizador registado com ID %s.', novo_organizador_id)::TEXT as mensagem;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as organizador_id,
            format('ERRO: Falha ao registar organizador - %s', SQLERRM)::TEXT as mensagem;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- PROCEDIMENTO 2: Registar Evento
-- ====================================================================

CREATE OR REPLACE FUNCTION registar_evento(
    p_titulo VARCHAR(200),
    p_descricao TEXT,
    p_data_inicio TIMESTAMP,
    p_data_fim TIMESTAMP,
    p_organizador_id INTEGER,
    p_categoria_id INTEGER DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT TRUE
)
RETURNS TABLE(
    evento_id INTEGER,
    mensagem TEXT
) AS $$
DECLARE
    novo_evento_id INTEGER;
    organizador_existe BOOLEAN;
    categoria_existe BOOLEAN;
BEGIN
    -- Validações básicas
    IF p_titulo IS NULL OR LENGTH(TRIM(p_titulo)) = 0 THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: Título é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    IF p_data_inicio IS NULL THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: Data de início é obrigatória.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    IF p_data_fim IS NULL THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: Data de fim é obrigatória.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Verificar se data de início é anterior à data de fim
    IF p_data_inicio >= p_data_fim THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: Data de início deve ser anterior à data de fim.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Verificar se data de início não é no passado
    IF p_data_inicio < NOW() THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: Data de início não pode ser no passado.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Verificar se o organizador existe
    IF p_organizador_id IS NULL THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            'ERRO: ID do organizador é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;
    
    SELECT EXISTS(SELECT 1 FROM ficha3_organizador WHERE id = p_organizador_id) INTO organizador_existe;
    
    IF NOT organizador_existe THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            format('ERRO: Organizador com ID %s não encontrado.', p_organizador_id)::TEXT as mensagem;
        RETURN;
    END IF;
    
    -- Verificar se a categoria existe (se fornecida)
    IF p_categoria_id IS NOT NULL THEN
        SELECT EXISTS(SELECT 1 FROM ficha3_categoriaevento WHERE id = p_categoria_id) INTO categoria_existe;
        
        IF NOT categoria_existe THEN
            RETURN QUERY SELECT 
                NULL::INTEGER as evento_id,
                format('ERRO: Categoria com ID %s não encontrada.', p_categoria_id)::TEXT as mensagem;
            RETURN;
        END IF;
    END IF;
    
    -- Inserir o novo evento
    INSERT INTO ficha3_evento (titulo, descricao, data_inicio, data_fim, organizador_id, categoria_id, ativo)
    VALUES (
        TRIM(p_titulo),
        COALESCE(TRIM(p_descricao), ''),
        p_data_inicio,
        p_data_fim,
        p_organizador_id,
        p_categoria_id,
        COALESCE(p_ativo, TRUE)
    )
    RETURNING id INTO novo_evento_id;
    
    -- Retornar sucesso
    RETURN QUERY SELECT 
        novo_evento_id as evento_id,
        format('SUCESSO: Evento "%s" registado com ID %s.', TRIM(p_titulo), novo_evento_id)::TEXT as mensagem;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as evento_id,
            format('ERRO: Falha ao registar evento - %s', SQLERRM)::TEXT as mensagem;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- Procedimento 3: Registar avaliação
-- ====================================================================



CREATE OR REPLACE FUNCTION create_avaliacao(
    p_client_id  INTEGER,
    p_evento_id  INTEGER,
    p_sessao_id  INTEGER,
    p_comentario TEXT,
    p_nota       INTEGER DEFAULT 1
)
RETURNS TABLE (
    avaliacao_id INTEGER,
    mensagem     TEXT
) AS $$
DECLARE
    nova_avaliacao_id INTEGER;
    mensagem     TEXT;
    cliente_existe BOOLEAN;
    evento_existe  BOOLEAN;
    sessao_existe  BOOLEAN;
BEGIN
    IF p_client_id IS NULL
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERRO: ID do Cliente é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;

    IF p_evento_id IS NULL
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERRO: ID do Evento é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;

    IF p_sessao_id IS NULL
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERRO: ID da Sessao é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;

    IF p_nota IS NULL
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERROR: Nota é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;

    IF p_nota < 1 AND p_nota > 5
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERROR: Nota tem que estar entre 1-5.'::TEXT as mensagem;
        RETURN;
    END IF;

    IF p_comentario IS NULL OR LENGTH(TRIM(p_comentario)) = 0
    THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            'ERROR: Comentario é obrigatório.'::TEXT as mensagem;
        RETURN;
    END IF;

    SELECT EXISTS(SELECT 1 FROM ficha3_cliente WHERE id = p_client_id) INTO cliente_existe;

    IF NOT cliente_existe THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            format('ERROR: Cliente com ID %s não encontrado.', p_client_id)::TEXT as mensagem;
        RETURN;
    END IF;
    SELECT EXISTS(SELECT 1 FROM ficha3_evento WHERE id = p_evento_id) INTO evento_existe;

    IF NOT evento_existe THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            format('ERROR: Evento com ID %s não encontrado.', p_evento_id)::TEXT as mensagem;
        RETURN;
    END IF;
    SELECT EXISTS(SELECT 1 FROM ficha3_sessao WHERE id = p_sessao_id) INTO sessao_existe;

    IF NOT sessao_existe THEN
        RETURN QUERY SELECT
            NULL::INTEGER as avaliacao_id,
            format('ERROR: Sessao com ID %s não encontrado.', p_sessao_id)::TEXT as mensagem;
        RETURN;
    END IF;

    INSERT INTO ficha3_avaliacao (nota, comentario, cliente_id, evento_id, sessao_id)
    VALUES (
        p_nota,
        COALESCE(TRIM(p_comentario), ''),
        p_client_id,
        p_evento_id,
        p_sessao_id
    )
    RETURNING id INTO nova_avaliacao_id;
    
    -- Retornar sucesso
    RETURN QUERY SELECT 
        nova_avaliacao_id as avaliacao_id,
        format('SUCESSO: Avaliacao registada com ID %s.', nova_avaliacao_id)::TEXT as mensagem;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN QUERY SELECT 
            NULL::INTEGER as avaliacao_id,
            format('ERRO: Falha ao registar avaliacao - %s', SQLERRM)::TEXT as mensagem;
END;
$$ LANGUAGE plpgsql;