-- Create view: faturas_com_bilhetes
CREATE OR REPLACE VIEW faturas_com_bilhetes AS
SELECT f.id, f.numero_unico, f.data_emissao, f.total, f.estado, c.nome AS cliente_nome,
       COUNT(fi.id) AS num_bilhetes
FROM ficha3_fatura f
JOIN ficha3_cliente c ON f.cliente_id = c.id
LEFT JOIN ficha3_faturasitem fi ON fi.fatura_id = f.id
GROUP BY f.id, c.nome;
