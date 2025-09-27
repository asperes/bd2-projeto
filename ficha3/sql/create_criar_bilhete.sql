-- Create procedure: criar_bilhete
CREATE OR REPLACE FUNCTION criar_bilhete(
    p_sessao_id INTEGER,
    p_cliente_id INTEGER,
    p_tipo VARCHAR,
    p_lugar VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    v_preco_base NUMERIC;
    v_multiplicador NUMERIC := 1.0;
    v_preco_final NUMERIC;
    v_codigo_unico UUID := gen_random_uuid();
    v_bilhete_id INTEGER;
BEGIN
    SELECT preco INTO v_preco_base FROM ficha3_sessao WHERE id = p_sessao_id;
    IF p_tipo = 'ESTUDANTE' THEN v_multiplicador := 0.7;
    ELSIF p_tipo = 'SENIOR' THEN v_multiplicador := 0.8;
    ELSIF p_tipo = 'VIP' THEN v_multiplicador := 1.5;
    ELSIF p_tipo = 'CRIANCA' THEN v_multiplicador := 0.5;
    END IF;
    v_preco_final := v_preco_base * v_multiplicador;

    INSERT INTO ficha3_bilhete (sessao_id, cliente_id, codigo_unico, tipo, usado, comprado_em, preco_final, lugar)
    VALUES (p_sessao_id, p_cliente_id, v_codigo_unico, p_tipo, FALSE, NOW(), v_preco_final, p_lugar)
    RETURNING id INTO v_bilhete_id;

    RETURN v_bilhete_id;
END;
$$ LANGUAGE plpgsql;
