# Reunião — Configuração da nova integração no Torre

**Data:** 21/09/2026 (segunda-feira)  
**Horário:** 8h30  
**Situação:** Agendada  
**Projeto:** CRM Rock (antiga BNEX)  
**Linha de trabalho:** Novo integrador de vendas via API da Rock  
**Unidade/associado:** Torre  
**Responsável pela preparação:** A confirmar  
**Participantes:** A confirmar

## Objetivo

Realizar a configuração da nova integração no Torre e alinhar as dependências técnicas necessárias entre Rock, Consinco e a equipe responsável pelo ambiente.

## Preparação necessária

| Ação | Situação | Responsável | Evidência esperada |
|---|---|---|---|
| Comunicar à Rock a intenção de configurar a nova integração no Torre e confirmar sua participação ou suporte. | Pendente | A confirmar | Confirmação da Rock e contato técnico disponível. |
| Solicitar apoio ao consultor de PDV da Consinco. | Pendente | A confirmar | Confirmação do consultor e disponibilidade para a reunião. |
| Coletar as informações técnicas necessárias para a configuração. | Pendente | A confirmar | Checklist técnico preenchido e validado antes da reunião. |

## Checklist técnico inicial

Os itens abaixo detalham a preparação e precisam ser confirmados com as equipes técnicas:

- URL e ambiente corretos da integração;
- endpoints, portas e protocolos utilizados;
- origens e destinos de rede que precisam de liberação;
- regras ou liberações de firewall e allowlist;
- método de autenticação e forma segura de disponibilizar credenciais;
- certificados, chaves ou requisitos de TLS, quando aplicável;
- parâmetros de identificação do Torre no Consinco e no CRM/Rock;
- dados ou transações de teste e resultado esperado;
- responsáveis técnicos de cada parte durante a configuração;
- forma de consultar logs e evidências de envio, recebimento e processamento;
- janela de ativação e procedimento de retorno à configuração anterior em caso de falha.

Credenciais, chaves e outros segredos não devem ser registrados neste documento.

## Resultado esperado da reunião

- nova integração configurada no Torre ou impedimentos técnicos claramente registrados;
- conectividade e autenticação validadas;
- transação de teste acompanhada de ponta a ponta, quando viável;
- próximos passos, responsáveis e prazos definidos;
- evidências da configuração e do teste vinculadas ao projeto.

## Pontos relacionados

- A URL de produção ainda precisa de confirmação formal da Rock, conforme os chamados `200955` e `Id Movidesk_202180`.
- A integridade das vendas deve ser validada antes de ampliar a migração, considerando a divergência registrada no chamado `202578`.

## Registro posterior

Após a reunião, registrar:

- participantes presentes;
- configurações realizadas;
- testes executados e respectivos resultados;
- impedimentos identificados;
- decisões tomadas;
- ações, responsáveis e prazos acordados.
