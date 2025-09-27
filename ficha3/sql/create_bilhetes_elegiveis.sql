-- Create view: bilhetes_elegiveis
CREATE OR REPLACE VIEW bilhetes_elegiveis AS
SELECT b.*
FROM ficha3_bilhete b
LEFT JOIN ficha3_faturasitem fi ON b.id = fi.bilhete_id
WHERE fi.id IS NULL;
