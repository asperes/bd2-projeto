-- Create procedure: criar_fatura
CREATE OR REPLACE FUNCTION criar_fatura(
    p_cliente_id INTEGER,
    p_estado CHAR(1),
    p_bilhetes_ids INTEGER[]
) RETURNS INTEGER AS $$
DECLARE
    v_total NUMERIC := 0;
    v_fatura_id INTEGER;
    v_numero_unico UUID := gen_random_uuid();
    v_bilhete_id INTEGER;
BEGIN
    -- Check all bilhetes are eligible (not already in a fatura and belong to client)
    FOREACH v_bilhete_id IN ARRAY p_bilhetes_ids LOOP
        IF EXISTS (
            SELECT 1 FROM ficha3_faturasitem WHERE bilhete_id = v_bilhete_id
        ) THEN
            RAISE EXCEPTION 'Bilhete % já está associado a uma fatura.', v_bilhete_id;
        END IF;
        IF NOT EXISTS (
            SELECT 1 FROM ficha3_bilhete WHERE id = v_bilhete_id AND cliente_id = p_cliente_id
        ) THEN
            RAISE EXCEPTION 'Bilhete % não pertence ao cliente.', v_bilhete_id;
        END IF;
        v_total := v_total + COALESCE((SELECT preco_final FROM ficha3_bilhete WHERE id = v_bilhete_id), 0);
    END LOOP;

    INSERT INTO ficha3_fatura (cliente_id, numero_unico, data_emissao, total, estado)
    VALUES (p_cliente_id, v_numero_unico, NOW(), v_total, p_estado)
    RETURNING id INTO v_fatura_id;

    -- Add FaturasItem
    FOREACH v_bilhete_id IN ARRAY p_bilhetes_ids LOOP
        INSERT INTO ficha3_faturasitem (fatura_id, bilhete_id) VALUES (v_fatura_id, v_bilhete_id);
    END LOOP;

    RETURN v_fatura_id;
END;
$$ LANGUAGE plpgsql;
