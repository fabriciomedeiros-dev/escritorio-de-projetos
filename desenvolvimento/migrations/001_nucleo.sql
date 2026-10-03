-- Escritório v2: aplicar somente no ambiente local autorizado.
-- Migração inicial transacional; não cria usuários nem altera schema public.
BEGIN;
SELECT pg_advisory_xact_lock(20261003, 1);
CREATE SCHEMA escritorio;
REVOKE ALL ON SCHEMA escritorio FROM PUBLIC;
SET LOCAL search_path = escritorio, pg_catalog;
CREATE TABLE migracoes (versao integer PRIMARY KEY, hash_sql text NOT NULL CHECK(hash_sql ~ '^[0-9a-f]{64}$'), aplicada_em timestamptz NOT NULL DEFAULT now());
CREATE TABLE portfolios (id text PRIMARY KEY CHECK (id ~ '^[a-z][a-z0-9_-]*$'), nome text NOT NULL,
 fuso text NOT NULL DEFAULT 'America/Sao_Paulo', configuracao jsonb NOT NULL DEFAULT '{}');
CREATE TABLE pessoas (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), nome text NOT NULL);
CREATE TABLE identidades (provedor text NOT NULL, sujeito text NOT NULL, pessoa uuid NOT NULL REFERENCES pessoas,
 PRIMARY KEY(provedor,sujeito));
CREATE TABLE membros (portfolio text REFERENCES portfolios, pessoa uuid REFERENCES pessoas,
 papel text NOT NULL CHECK (papel IN ('gestor','executor','consulta')), ativo boolean NOT NULL DEFAULT true,
 PRIMARY KEY(portfolio,pessoa));
CREATE TABLE operacoes (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 ator uuid NOT NULL, chave_repeticao text NOT NULL, hash_pedido text NOT NULL CHECK(hash_pedido ~ '^[0-9a-f]{64}$'),
 comando text NOT NULL, pedido jsonb NOT NULL, resultado jsonb,
 persistencia text NOT NULL DEFAULT 'pendente' CHECK(persistencia IN ('pendente','persistida','verificada','falhou')),
 protecao text NOT NULL DEFAULT 'pendente' CHECK(protecao IN ('pendente','confirmada','falhou')),
 erro jsonb, criada_em timestamptz NOT NULL DEFAULT now(), verificada_em timestamptz,
 PRIMARY KEY(portfolio,id), UNIQUE(portfolio,ator,chave_repeticao),
 FOREIGN KEY(portfolio,ator) REFERENCES membros(portfolio,pessoa),
 CHECK(persistencia <> 'verificada' OR (resultado IS NOT NULL AND verificada_em IS NOT NULL)));
CREATE TABLE artefatos (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 nome text NOT NULL, tipo_midia text NOT NULL, chave_objeto text NOT NULL,
 sha256 text NOT NULL CHECK(sha256 ~ '^[0-9a-f]{64}$'), bytes bigint NOT NULL CHECK(bytes >= 0),
 versao integer NOT NULL DEFAULT 1 CHECK(versao > 0),
 estado text NOT NULL DEFAULT 'preparado' CHECK(estado IN ('preparado','verificado','falhou')),
 recebido_em timestamptz NOT NULL DEFAULT now(), verificado_em timestamptz,
 origem jsonb NOT NULL, remetente uuid NOT NULL,
 PRIMARY KEY(portfolio,id), UNIQUE(portfolio,chave_objeto),
 FOREIGN KEY(portfolio,remetente) REFERENCES membros(portfolio,pessoa),
 CHECK(estado <> 'verificado' OR verificado_em IS NOT NULL));
CREATE TABLE entradas (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 operacao uuid NOT NULL, conteudo text, artefato uuid, origem jsonb NOT NULL,
 classificacao_proposta text, classificacao_confirmada text,
 estado text NOT NULL CHECK(estado IN ('recebida','triagem_pendente','vinculada')),
 recebida_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,operacao) REFERENCES operacoes,
 FOREIGN KEY(portfolio,artefato) REFERENCES artefatos,
 CHECK(conteudo IS NOT NULL OR artefato IS NOT NULL));
CREATE TABLE lotes (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 original uuid NOT NULL, criado_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,original) REFERENCES artefatos);
-- Revisões imutáveis: nova revisão = nova linha. Nunca substituir o texto revisado.
CREATE TABLE propostas (portfolio text NOT NULL, id uuid NOT NULL, versao integer NOT NULL CHECK(versao > 0),
 lote uuid NOT NULL, tipo text NOT NULL, conteudo jsonb NOT NULL, localizacao_fonte jsonb NOT NULL,
 criada_em timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(portfolio,id,versao),
 FOREIGN KEY(portfolio,lote) REFERENCES lotes);
CREATE TABLE aprovacoes (portfolio text NOT NULL, proposta uuid NOT NULL, versao_proposta integer NOT NULL,
 decisor uuid NOT NULL, decisao text NOT NULL CHECK(decisao IN ('aprovada','rejeitada')),
 operacao uuid NOT NULL, decidida_em timestamptz NOT NULL DEFAULT now(), justificativa text,
 PRIMARY KEY(portfolio,proposta,versao_proposta), UNIQUE(portfolio,proposta,versao_proposta,decisao),
 FOREIGN KEY(portfolio,proposta,versao_proposta) REFERENCES propostas,
 FOREIGN KEY(portfolio,decisor) REFERENCES membros(portfolio,pessoa),
 FOREIGN KEY(portfolio,operacao) REFERENCES operacoes);
CREATE TABLE registros (portfolio text REFERENCES portfolios, id text NOT NULL,
 tipo text NOT NULL CHECK(tipo IN ('ideia','solicitacao','projeto','tarefa')),
 titulo text NOT NULL CHECK(length(btrim(titulo)) > 0), estado text NOT NULL,
 responsavel_total uuid, resultado_esperado text, criterio_conclusao text,
 meta date, prazo_proposto date, prazo_aceito date,
 esforco_restante numeric(10,2) CHECK(esforco_restante >= 0),
 origem jsonb NOT NULL DEFAULT '{}', criado_por uuid NOT NULL,
 versao integer NOT NULL DEFAULT 1 CHECK(versao > 0), criado_em timestamptz NOT NULL DEFAULT now(),
 atualizado_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,id), UNIQUE(portfolio,id,tipo),
 FOREIGN KEY(portfolio,responsavel_total) REFERENCES membros(portfolio,pessoa),
 FOREIGN KEY(portfolio,criado_por) REFERENCES membros(portfolio,pessoa),
 CHECK ((tipo='tarefa' AND estado IN ('capturada','planejada','em_andamento','bloqueada','aguardando_validacao','concluida','cancelada'))
 OR (tipo='solicitacao' AND estado IN ('capturada','em_triagem','planejada','em_andamento','aguardando_validacao','concluida','cancelada'))
 OR (tipo='projeto' AND estado IN ('iniciacao','planejamento','execucao','encerrado','cancelado'))
 OR (tipo='ideia' AND estado IN ('capturada','descoberta','definicao','modelo_negocio','experimento','promovida','arquivada'))));
CREATE TABLE definicoes (portfolio text NOT NULL, registro text NOT NULL,
 objetivo text, escopo jsonb NOT NULL DEFAULT '{}', valor_esperado jsonb NOT NULL DEFAULT '{}',
 referencias_documentais jsonb NOT NULL DEFAULT '[]', autorizacao_preparacao jsonb,
 decisao_promocao jsonb, PRIMARY KEY(portfolio,registro), FOREIGN KEY(portfolio,registro) REFERENCES registros);
CREATE TABLE vinculos_registros (portfolio text NOT NULL, origem text NOT NULL, destino text NOT NULL,
 relacao text NOT NULL CHECK(relacao IN ('parte_de','originou','relacionado')),
 PRIMARY KEY(portfolio,origem,destino,relacao), FOREIGN KEY(portfolio,origem) REFERENCES registros,
 FOREIGN KEY(portfolio,destino) REFERENCES registros, CHECK(origem <> destino));
CREATE TABLE executores (portfolio text NOT NULL, tarefa text NOT NULL, tipo text NOT NULL DEFAULT 'tarefa' CHECK(tipo='tarefa'),
 pessoa uuid NOT NULL, PRIMARY KEY(portfolio,tarefa,pessoa),
 FOREIGN KEY(portfolio,tarefa,tipo) REFERENCES registros(portfolio,id,tipo),
 FOREIGN KEY(portfolio,pessoa) REFERENCES membros(portfolio,pessoa));
CREATE TABLE fontes (portfolio text NOT NULL, registro text NOT NULL, artefato uuid NOT NULL,
 finalidade text NOT NULL CHECK(finalidade IN ('documentacao','evidencia','origem')),
 localizacao jsonb NOT NULL DEFAULT '{}', PRIMARY KEY(portfolio,registro,artefato,finalidade),
 FOREIGN KEY(portfolio,registro) REFERENCES registros, FOREIGN KEY(portfolio,artefato) REFERENCES artefatos);
CREATE TABLE efetivacoes (portfolio text NOT NULL, proposta uuid NOT NULL, versao_proposta integer NOT NULL,
 decisao text NOT NULL DEFAULT 'aprovada' CHECK(decisao='aprovada'), operacao uuid NOT NULL,
 registro text NOT NULL, PRIMARY KEY(portfolio,proposta,versao_proposta),
 FOREIGN KEY(portfolio,proposta,versao_proposta,decisao) REFERENCES aprovacoes(portfolio,proposta,versao_proposta,decisao),
 FOREIGN KEY(portfolio,operacao) REFERENCES operacoes, FOREIGN KEY(portfolio,registro) REFERENCES registros);
CREATE TABLE atualizacoes (portfolio text NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(), registro text NOT NULL,
 operacao uuid NOT NULL, remetente uuid NOT NULL, autor_relato uuid REFERENCES pessoas, autor_informado text,
 entregue text, restante text, dificuldade text, esforco_restante numeric(10,2) CHECK(esforco_restante >= 0),
 prazo_proposto date, fontes jsonb NOT NULL DEFAULT '[]', criada_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,registro) REFERENCES registros,
 FOREIGN KEY(portfolio,remetente) REFERENCES membros(portfolio,pessoa), FOREIGN KEY(portfolio,operacao) REFERENCES operacoes,
 CHECK(entregue IS NOT NULL OR restante IS NOT NULL OR dificuldade IS NOT NULL));
CREATE TABLE dependencias (portfolio text NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
 entrega text NOT NULL, provedor text, terceiro text, motivo text NOT NULL,
 responsavel_acao uuid NOT NULL, proxima_acao text NOT NULL, acompanhar_em date NOT NULL,
 criterio_resolucao text NOT NULL, estado text NOT NULL CHECK(estado IN ('pendente','resolvida','dispensada')),
 PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,entrega) REFERENCES registros,
 FOREIGN KEY(portfolio,provedor) REFERENCES registros, FOREIGN KEY(portfolio,responsavel_acao) REFERENCES membros(portfolio,pessoa),
 CHECK(provedor IS NOT NULL OR terceiro IS NOT NULL), CHECK(provedor IS NULL OR provedor <> entrega));
CREATE TABLE validacoes (portfolio text NOT NULL, registro text NOT NULL, versao_registro integer NOT NULL CHECK(versao_registro > 0),
 validador uuid NOT NULL, modo text NOT NULL CHECK(modo IN ('verificacao','aceite_humano')),
 parecer text NOT NULL, validada_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,registro,versao_registro), FOREIGN KEY(portfolio,registro) REFERENCES registros,
 FOREIGN KEY(portfolio,validador) REFERENCES membros(portfolio,pessoa));
CREATE TABLE decisoes (portfolio text NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(), registro text NOT NULL,
 assunto text NOT NULL, justificativa text NOT NULL, decisor uuid NOT NULL, fonte_documental text NOT NULL,
 impacto jsonb NOT NULL DEFAULT '{}', decidida_em timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,registro) REFERENCES registros,
 FOREIGN KEY(portfolio,decisor) REFERENCES membros(portfolio,pessoa));
CREATE TABLE sprints (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 inicio date NOT NULL, fim date NOT NULL, linha_base jsonb NOT NULL, PRIMARY KEY(portfolio,id), CHECK(fim >= inicio));
CREATE TABLE itens_sprint (portfolio text NOT NULL, sprint uuid NOT NULL, registro text NOT NULL,
 PRIMARY KEY(portfolio,sprint,registro), FOREIGN KEY(portfolio,sprint) REFERENCES sprints,
 FOREIGN KEY(portfolio,registro) REFERENCES registros);
CREATE TABLE capacidades (portfolio text NOT NULL, sprint uuid NOT NULL, pessoa uuid NOT NULL,
 horas numeric(10,2) NOT NULL CHECK(horas >= 0), reserva numeric(10,2) NOT NULL CHECK(reserva >= 0 AND reserva <= horas),
 fonte jsonb NOT NULL, PRIMARY KEY(portfolio,sprint,pessoa), FOREIGN KEY(portfolio,sprint) REFERENCES sprints,
 FOREIGN KEY(portfolio,pessoa) REFERENCES membros(portfolio,pessoa));
CREATE TABLE previsoes (portfolio text NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(), registro text NOT NULL,
 data_prevista date, metodo text NOT NULL, entradas jsonb NOT NULL, lacunas jsonb NOT NULL,
 calculada_em timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(portfolio,id), FOREIGN KEY(portfolio,registro) REFERENCES registros);
CREATE TABLE alertas (portfolio text NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(), registro text NOT NULL,
 tipo text NOT NULL, causa text NOT NULL, gravidade text NOT NULL, estado text NOT NULL,
 chave_agrupamento text NOT NULL, primeira_ocorrencia timestamptz NOT NULL DEFAULT now(),
 ultima_ocorrencia timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(portfolio,id), UNIQUE(portfolio,chave_agrupamento),
 FOREIGN KEY(portfolio,registro) REFERENCES registros);
CREATE TABLE historico (portfolio text NOT NULL, id bigint GENERATED ALWAYS AS IDENTITY,
 registro text NOT NULL, operacao uuid NOT NULL, ator uuid NOT NULL, acao text NOT NULL,
 antes jsonb, depois jsonb, motivo text NOT NULL, fonte jsonb NOT NULL,
 ocorrido_em timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(portfolio,id),
 FOREIGN KEY(portfolio,registro) REFERENCES registros, FOREIGN KEY(portfolio,operacao) REFERENCES operacoes,
 FOREIGN KEY(portfolio,ator) REFERENCES membros(portfolio,pessoa));
CREATE TABLE exportacoes (portfolio text REFERENCES portfolios, id uuid NOT NULL DEFAULT gen_random_uuid(),
 destino text NOT NULL, manifesto jsonb NOT NULL, checksum text NOT NULL CHECK(checksum ~ '^[0-9a-f]{64}$'),
 estado text NOT NULL CHECK(estado IN ('preparada','verificada','falhou')), criada_em timestamptz NOT NULL DEFAULT now(),
 restauracao_testada_em timestamptz, PRIMARY KEY(portfolio,id));
CREATE INDEX registros_consulta ON registros(portfolio,tipo,estado,prazo_aceito);
CREATE INDEX registros_responsavel ON registros(portfolio,responsavel_total);
CREATE INDEX atualizacoes_registro ON atualizacoes(portfolio,registro,criada_em DESC);
CREATE INDEX historico_registro ON historico(portfolio,registro,ocorrido_em DESC);
CREATE INDEX dependencias_entrega ON dependencias(portfolio,entrega,estado);
CREATE INDEX propostas_lote ON propostas(portfolio,lote);
CREATE INDEX busca_registros ON registros USING gin(to_tsvector('portuguese', titulo || ' ' || coalesce(resultado_esperado,'')));
-- Evidência, aceite e pendências são verificados no estado final da transação.
-- Validação semântica da evidência e autorização continuam responsabilidade do serviço.
CREATE FUNCTION verificar_conclusoes() RETURNS trigger LANGUAGE plpgsql SET search_path=escritorio,pg_catalog AS $$
BEGIN
 IF EXISTS (SELECT 1 FROM registros r WHERE r.tipo='tarefa' AND r.estado='concluida' AND (
  r.responsavel_total IS NULL OR nullif(btrim(r.criterio_conclusao),'') IS NULL
  OR NOT EXISTS (SELECT 1 FROM validacoes v WHERE v.portfolio=r.portfolio AND v.registro=r.id AND v.versao_registro=r.versao)
  OR NOT EXISTS (SELECT 1 FROM fontes f JOIN artefatos a ON (a.portfolio,a.id)=(f.portfolio,f.artefato)
       WHERE f.portfolio=r.portfolio AND f.registro=r.id AND f.finalidade='evidencia' AND a.estado='verificado')
  OR EXISTS (SELECT 1 FROM dependencias d WHERE d.portfolio=r.portfolio AND d.entrega=r.id AND d.estado='pendente')
  OR EXISTS (SELECT 1 FROM vinculos_registros l JOIN registros filho ON (filho.portfolio,filho.id)=(l.portfolio,l.origem)
       WHERE l.portfolio=r.portfolio AND l.destino=r.id AND l.relacao='parte_de' AND filho.tipo='tarefa'
       AND filho.estado NOT IN ('concluida','cancelada'))
 )) THEN RAISE EXCEPTION 'Conclusão sem responsável, critério, validação, evidência ou com pendência' USING ERRCODE='23514'; END IF;
 RETURN NULL;
END $$;
DO $$ DECLARE nome text; BEGIN
 FOREACH nome IN ARRAY ARRAY['registros','validacoes','fontes','artefatos','dependencias','vinculos_registros'] LOOP
 EXECUTE format('CREATE CONSTRAINT TRIGGER integridade_conclusao AFTER INSERT OR UPDATE OR DELETE ON escritorio.%I DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION escritorio.verificar_conclusoes()',nome);
 END LOOP;
END $$;
CREATE FUNCTION rejeitar_reescrita() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Registro imutável: criar nova revisão/evento'; END $$;
DO $$ DECLARE nome text; BEGIN
 FOREACH nome IN ARRAY ARRAY['historico','propostas','aprovacoes','validacoes','decisoes'] LOOP
 EXECUTE format('CREATE TRIGGER imutavel BEFORE UPDATE OR DELETE ON escritorio.%I FOR EACH ROW EXECUTE FUNCTION escritorio.rejeitar_reescrita()',nome);
 END LOOP;
END $$;
CREATE FUNCTION versionar_registro() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.portfolio<>OLD.portfolio OR NEW.id<>OLD.id OR NEW.tipo<>OLD.tipo THEN
  RAISE EXCEPTION 'Identificador e tipo imutáveis'; END IF;
 IF NEW.versao<>OLD.versao+1 THEN RAISE EXCEPTION 'Atualização requer incremento unitário de versão'; END IF;
 NEW.atualizado_em=now(); RETURN NEW;
END $$;
CREATE TRIGGER versionar BEFORE UPDATE ON registros FOR EACH ROW EXECUTE FUNCTION versionar_registro();
INSERT INTO migracoes(versao,hash_sql) VALUES(1,:'hash_sql');
COMMIT;
