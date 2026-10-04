"""Exercita o schema real no cluster local. Dados sintéticos são revertidos.
Execute após start/migrate: python3 desenvolvimento/testes/verificar_esquema.py
"""
from pathlib import Path
import sys
import tempfile
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'local'))
import ambiente

TEST = '''
BEGIN;
SET LOCAL search_path=escritorio,pg_catalog;
INSERT INTO portfolios(id,nome) VALUES ('teste_v2','Teste sintético'),('teste_v2_outro','Outro teste');
INSERT INTO pessoas(id,nome) VALUES ('00000000-0000-0000-0000-000000000001','Pessoa sintética');
INSERT INTO membros(portfolio,pessoa,papel) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000001','gestor'),
 ('teste_v2_outro','00000000-0000-0000-0000-000000000001','gestor');
INSERT INTO operacoes(portfolio,id,ator,chave_repeticao,hash_pedido,comando,pedido) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000002','00000000-0000-0000-0000-000000000001','chave-teste',repeat('a',64),'capturar','{}');
INSERT INTO registros(portfolio,id,tipo,titulo,estado,criado_por,responsavel_total,criterio_conclusao) VALUES
 ('teste_v2','TESTE-TAR','tarefa','Entrega sintética','em_andamento','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000001','Relatório integrado');
DO $$ BEGIN
 BEGIN
  INSERT INTO operacoes(portfolio,ator,chave_repeticao,hash_pedido,comando,pedido)
   VALUES ('teste_v2','00000000-0000-0000-0000-000000000001','chave-teste',repeat('a',64),'capturar','{}');
  RAISE EXCEPTION 'Chave repetida aceita';
 EXCEPTION WHEN unique_violation THEN NULL; END;
 BEGIN
  INSERT INTO vinculos_registros VALUES ('teste_v2_outro','TESTE-TAR','OUTRO','parte_de');
  RAISE EXCEPTION 'Vínculo de outro domínio aceito';
 EXCEPTION WHEN foreign_key_violation THEN NULL; END;
 BEGIN
  UPDATE registros SET estado='concluida',versao=2 WHERE portfolio='teste_v2' AND id='TESTE-TAR';
  SET CONSTRAINTS ALL IMMEDIATE;
  RAISE EXCEPTION 'Conclusão sem evidência aceita';
 EXCEPTION WHEN check_violation THEN NULL; END;
 BEGIN
  INSERT INTO capacidades(portfolio,sprint,pessoa,horas,reserva,fonte)
   VALUES ('teste_v2',gen_random_uuid(),'00000000-0000-0000-0000-000000000001',5,6,'{}');
  RAISE EXCEPTION 'Reserva excedente aceita';
 EXCEPTION WHEN check_violation THEN NULL; END;
 UPDATE registros SET prazo_proposto='2026-10-09',versao=2 WHERE portfolio='teste_v2' AND id='TESTE-TAR' AND versao=1;
 UPDATE registros SET prazo_aceito='2026-10-10',versao=2 WHERE portfolio='teste_v2' AND id='TESTE-TAR' AND versao=1;
 IF FOUND THEN RAISE EXCEPTION 'Versão antiga sobrescreveu registro'; END IF;
END $$;
INSERT INTO artefatos(portfolio,id,nome,tipo_midia,chave_objeto,sha256,bytes,estado,verificado_em,origem,remetente) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000003','relatorio.txt','text/plain','teste/relatorio',repeat('b',64),10,'verificado',now(),'{}','00000000-0000-0000-0000-000000000001');
INSERT INTO fontes VALUES ('teste_v2','TESTE-TAR','00000000-0000-0000-0000-000000000003','evidencia','{}');
INSERT INTO lotes(portfolio,id,original) VALUES ('teste_v2','00000000-0000-0000-0000-000000000004','00000000-0000-0000-0000-000000000003');
INSERT INTO propostas(portfolio,id,versao,lote,tipo,conteudo,localizacao_fonte) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000005',1,'00000000-0000-0000-0000-000000000004','tarefa','{}','{}');
DO $$ BEGIN
 BEGIN
  INSERT INTO efetivacoes(portfolio,proposta,versao_proposta,operacao,registro) VALUES
   ('teste_v2','00000000-0000-0000-0000-000000000005',1,'00000000-0000-0000-0000-000000000002','TESTE-TAR');
  RAISE EXCEPTION 'Proposta efetivada sem aprovação';
 EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;
INSERT INTO aprovacoes(portfolio,proposta,versao_proposta,decisor,decisao,operacao) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000005',1,'00000000-0000-0000-0000-000000000001','aprovada','00000000-0000-0000-0000-000000000002');
INSERT INTO efetivacoes(portfolio,proposta,versao_proposta,operacao,registro) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000005',1,'00000000-0000-0000-0000-000000000002','TESTE-TAR');
INSERT INTO dependencias(portfolio,id,entrega,terceiro,motivo,responsavel_acao,proxima_acao,acompanhar_em,criterio_resolucao,estado) VALUES
 ('teste_v2','00000000-0000-0000-0000-000000000006','TESTE-TAR','API sintética','Integração pendente','00000000-0000-0000-0000-000000000001','Verificar API','2026-10-05','Integração validada','pendente');
DO $$ BEGIN
 BEGIN
  UPDATE registros SET estado='concluida',versao=3 WHERE portfolio='teste_v2' AND id='TESTE-TAR';
  INSERT INTO validacoes VALUES ('teste_v2','TESTE-TAR',3,'00000000-0000-0000-0000-000000000001','aceite_humano','Evidência examinada',now());
  SET CONSTRAINTS ALL IMMEDIATE;
  RAISE EXCEPTION 'Conclusão com dependência aceita';
 EXCEPTION WHEN check_violation THEN NULL; END;
END $$;
UPDATE dependencias SET estado='resolvida' WHERE portfolio='teste_v2';
UPDATE registros SET estado='concluida',versao=3 WHERE portfolio='teste_v2' AND id='TESTE-TAR';
INSERT INTO validacoes VALUES ('teste_v2','TESTE-TAR',3,'00000000-0000-0000-0000-000000000001','aceite_humano','Evidência examinada',now());
SET CONSTRAINTS ALL IMMEDIATE;
INSERT INTO historico(portfolio,registro,operacao,ator,acao,motivo,fonte) VALUES
 ('teste_v2','TESTE-TAR','00000000-0000-0000-0000-000000000002','00000000-0000-0000-0000-000000000001','conclusao','Teste','{}');
DO $$ BEGIN
 BEGIN
  DELETE FROM fontes WHERE portfolio='teste_v2';
  RAISE EXCEPTION 'Evidência de tarefa concluída removida';
 EXCEPTION WHEN check_violation THEN NULL; END;
 BEGIN
  UPDATE propostas SET conteudo='{"alterado":true}' WHERE portfolio='teste_v2';
  RAISE EXCEPTION 'Proposta aprovada reescrita';
 EXCEPTION WHEN raise_exception THEN
  IF SQLERRM NOT LIKE 'Registro imutável:%' THEN RAISE; END IF;
 END;
 BEGIN
  DELETE FROM historico WHERE portfolio='teste_v2';
  RAISE EXCEPTION 'Histórico apagado';
 EXCEPTION WHEN raise_exception THEN
  IF SQLERRM NOT LIKE 'Registro imutável:%' THEN RAISE; END IF;
 END;
END $$;
ROLLBACK;
'''


def main():
    if not ambiente.running():
        raise RuntimeError('Ambiente local deve estar iniciado.')
    assert ambiente.sql("SELECT count(*) FROM escritorio.portfolios WHERE id LIKE 'teste_v2%';") == '0'
    result = ambiente.sql(TEST)
    assert result.endswith('ROLLBACK')
    assert ambiente.sql("SELECT count(*) FROM escritorio.portfolios WHERE id LIKE 'teste_v2%';") == '0'
    # Restaurar o schema real em base temporária distinta, no cluster local.
    restored = 'ep_restore_' + uuid.uuid4().hex[:12]
    with tempfile.TemporaryDirectory(prefix='ep-schema-') as directory:
        archive = Path(directory) / 'escritorio.dump'
        ambiente.execute([ambiente.binary('pg_dump'), '-Fc', '-n', 'escritorio', '-f', str(archive)], ambiente.connection())
        ambiente.sql('CREATE DATABASE ' + restored + ';', database='postgres')
        try:
            env = ambiente.connection()
            env['PGDATABASE'] = restored
            ambiente.execute([ambiente.binary('pg_restore'), '--exit-on-error', '-d', restored, str(archive)], env)
            assert ambiente.sql('SELECT hash_sql FROM escritorio.migracoes WHERE versao=1;', database=restored) == ambiente.sql('SELECT hash_sql FROM escritorio.migracoes WHERE versao=1;')
            assert ambiente.sql('SELECT hash_sql FROM escritorio.migracoes WHERE versao=2;', database=restored) == ambiente.sql('SELECT hash_sql FROM escritorio.migracoes WHERE versao=2;')
            assert ambiente.sql(TEST, database=restored).endswith('ROLLBACK')
        finally:
            # Apenas a base de ensaio cujo nome foi gerado nesta execução.
            ambiente.sql('DROP DATABASE ' + restored + ';', database='postgres')
    print('PASSOU: dump/restauração do schema real e repetição dos testes na base restaurada.')
    print('PASSOU: restrições de portfólio, repetição, versão, capacidade e aprovação por revisão;')
    print('conclusão sem evidência ou com bloqueio rejeitada; conclusão válida aceita;')
    print('remoção de evidência e reescrita de proposta/histórico rejeitadas; dados sintéticos revertidos.')


if __name__ == '__main__':
    main()
