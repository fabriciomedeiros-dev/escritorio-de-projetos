-- Incremento local: dependência necessária à entrega versus impedimento de avanço.
BEGIN;
SELECT pg_advisory_xact_lock(20261003, 1);
SET LOCAL search_path = escritorio, pg_catalog;
ALTER TABLE dependencias ADD COLUMN impede_avanco boolean NOT NULL DEFAULT false;
ALTER TABLE registros ADD COLUMN estado_antes_bloqueio text;
ALTER TABLE registros ADD CONSTRAINT retomada_bloqueio CHECK (
 estado_antes_bloqueio IS NULL OR
 (tipo='tarefa' AND estado='bloqueada' AND estado_antes_bloqueio IN ('capturada','planejada','em_andamento','aguardando_validacao')));
INSERT INTO migracoes(versao,hash_sql) VALUES(2,:'hash_sql');
COMMIT;
