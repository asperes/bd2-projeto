CREATE PROCEDURE criar_artista(
    p_nome VARCHAR,
    p_bio TEXT,
    p_genero_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF NOT EXISTS (SELECT 1 FROM genero WHERE id = p_genero_id) THEN
        RAISE EXCEPTION 'Gênero com id % não existe.', p_genero_id;
    END IF;

    INSERT INTO ficha3_artista (nome, bio, genero_id)
    VALUES (p_nome, p_bio, p_genero_id);
END;
$$;
