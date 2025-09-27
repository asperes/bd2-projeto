CREATE VIEW vista_eventos_artista AS
SELECT
    a.id AS artista_id,
    a.nome AS artista_nome,
    s.id AS evento_id,
    s.inicio,
    s.fim,
    l.nome
FROM
    ficha3_artista a
JOIN
    ficha3_performance p ON a.id = p.artista_id
JOIN
    ficha3_sessao s ON p.sessao_id = s.id
JOIN
    ficha3_local l ON s.local_id = l.id;