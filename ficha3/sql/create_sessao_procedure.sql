CREATE PROCEDURE criar_sessao(
    p_evento_id INTEGER,
    p_local_id INTEGER,
    p_inicio TIMESTAMP,
    p_fim TIMESTAMP,
    p_preco NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    
    IF NOT EXISTS (SELECT 1 FROM ficha3_evento WHERE id = p_evento_id) THEN
        RAISE EXCEPTION 'Evento com id % não existe.', p_evento_id;
    END IF;


    IF NOT EXISTS (SELECT 1 FROM ficha3_local WHERE id = p_local_id) THEN
        RAISE EXCEPTION 'Local com id % não existe.', p_local_id;
    END IF;

    
    IF p_inicio >= p_fim THEN
        RAISE EXCEPTION 'A data de início deve ser anterior à data de fim.';
    END IF;

    
    IF p_preco < 0 THEN
        RAISE EXCEPTION 'O preço deve ser positivo.';
    END IF;

    INSERT INTO ficha3_sessao (evento_id, local_id, inicio, fim, preco)
    VALUES (p_evento_id, p_local_id, p_inicio, p_fim, p_preco);
END;
$$;