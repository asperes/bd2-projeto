-- ====================================================================
-- VISTA 1: Organizador
-- ====================================================================

CREATE OR REPLACE VIEW vista_organizador_eventos AS
SELECT 
    o.nome AS Nome,
    e.titulo AS Titulo,
    AVG(a.nota) AS Avaliação,
    COUNT(DISTINCT b.id) AS Bilhetes_vendidos
FROM ficha3_organizador AS o
    LEFT JOIN ficha3_evento AS e ON o.id = e.organizador_id
    LEFT JOIN ficha3_sessao AS s ON e.id = s.evento_id
    LEFT JOIN ficha3_avaliacao AS a ON s.id = a.sessao_id
    LEFT JOIN ficha3_bilhete AS b ON s.id = b.sessao_id
GROUP BY e.titulo, o.nome
ORDER BY o.nome;

CREATE OR REPLACE VIEW vista_avaliacao AS
SELECT
    c.nome AS cliente,
    a.nota,
    a.comentario,
    e.titulo AS evento,
    s.inicio AS sessao
FROM ficha3_avaliacao AS a
    LEFT JOIN ficha3_cliente AS c ON a.cliente_id = c.id
    LEFT JOIN ficha3_evento AS e ON a.evento_id = e.id
    LEFT JOIN ficha3_sessao AS s ON a.sessao_id = s.id
ORDER BY a.criado_em;