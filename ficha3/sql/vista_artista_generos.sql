CREATE VIEW vista_artista_generos AS
SELECT a.id AS artista_id, a.nome AS artista_nome, a.bio AS artista_bio, g.id AS genero_id, g.nome AS genero_nome
FROM ficha3_artista a
JOIN ficha3_generoartista g ON a.genero_id = g.id;

 