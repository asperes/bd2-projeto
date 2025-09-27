-- 1. Listar todos os bilhetes elegíveis (view)
SELECT * FROM bilhetes_elegiveis;

-- 2. Listar todas as faturas com o número de bilhetes e nome do cliente
SELECT * FROM faturas_com_bilhetes;

-- 3. Criar um novo bilhete para a Alice
SELECT criar_bilhete(
    (SELECT s.id::INTEGER FROM ficha3_sessao s JOIN ficha3_evento e ON s.evento_id = e.id WHERE e.titulo = 'Concerto X' LIMIT 1),
    (SELECT c.id::INTEGER FROM ficha3_cliente c WHERE c.nome = 'Alice' LIMIT 1),
    'NORMAL'::VARCHAR,
    'A4'::VARCHAR
);

-- 3A. Criar vários bilhetes para a Alice e logo a respetiva fatura, tudo numa transação
DO $$
DECLARE
    bilhete1_id INTEGER;
    bilhete2_id INTEGER;
    bilhetes_ids INTEGER[];
BEGIN
    -- Criar dois bilhetes para a Alice
    bilhete1_id := criar_bilhete(
        (SELECT s.id::INTEGER FROM ficha3_sessao s JOIN ficha3_evento e ON s.evento_id = e.id WHERE e.titulo = 'Concerto X' LIMIT 1),
        (SELECT c.id::INTEGER FROM ficha3_cliente c WHERE c.nome = 'Alice' LIMIT 1),
        'NORMAL'::VARCHAR,
        'A5'::VARCHAR
    );
    bilhete2_id := criar_bilhete(
        (SELECT s.id::INTEGER FROM ficha3_sessao s JOIN ficha3_evento e ON s.evento_id = e.id WHERE e.titulo = 'Concerto X' LIMIT 1),
        (SELECT c.id::INTEGER FROM ficha3_cliente c WHERE c.nome = 'Alice' LIMIT 1),
        'VIP'::VARCHAR,
        'A6'::VARCHAR
    );
    bilhetes_ids := ARRAY[bilhete1_id, bilhete2_id];

    -- Criar a fatura para a Alice com os novos bilhetes
    PERFORM criar_fatura(
        (SELECT id::INTEGER FROM ficha3_cliente WHERE nome = 'Alice' LIMIT 1),
        'P'::CHAR(1),
        bilhetes_ids
    );
END $$;

-- 4. Ver todas as faturas após a criação (view)
SELECT * FROM faturas_com_bilhetes;

-- 5. Ver todos os bilhetes da Carol
SELECT b.codigo_unico, b.tipo, b.preco_final, b.lugar
FROM ficha3_bilhete b
JOIN ficha3_cliente c ON b.cliente_id = c.id
WHERE c.nome = 'Carol';
