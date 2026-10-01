# Demanda — Regra de incentivo do ERP no PDV

**Data do registro:** 01/10/2026  
**Projeto:** CRM Rock (antiga BNEX)  
**Linha de trabalho:** Nova integração Consinco X ROCK  
**ID de acompanhamento:** CRM-008  
**Situação:** Em tratamento — documentação consolidada para abertura de chamado na TOTVS  
**Prioridade:** Alta, a validar na triagem  
**Responsável pelo acompanhamento:** A confirmar  
**Número do chamado TOTVS:** Pendente

## Contexto

A nova integração entre o TOTVS Consinco e o CRM ROCK já possui um fluxo documentado de identificação do cliente e envio de eventos do PDV. A tratativa atual busca concluir a configuração das regras de incentivo cadastradas no ERP para que o preço de incentivo, tratado no material técnico como Preço 2, seja carregado e aplicado corretamente no PDV quando o cliente estiver elegível.

O principal ponto pendente é a documentação do caminho entre o cadastro da regra no ERP, a geração da carga, o recebimento pelo Acrux Monitor e pelo PDV e a associação da regra ao cliente identificado pelo CRM ROCK.

## Situação observada

- o parâmetro dinâmico `REGRA_INTEGRADOERP_LINUX`, do grupo `CARGA_PDV`, está registrado com valor `S` em escopo geral;
- a orientação pública da TOTVS informa que, após a definição do parâmetro, deve ser executada a atualização com `F4`;
- o material existente descreve os eventos `/start`, `/sub-total` e `/finalization`, além da identificação do cliente no IntegradorGSWS;
- o material não descreve de forma completa a geração, o transporte, a persistência e o diagnóstico da regra de incentivo entre ERP e PDV;
- também precisa ser confirmada a separação entre a regra de incentivo nativa do PDV e os descontos exclusivos retornados pelo parceiro externo no subtotal.

## Objetivo da tratativa

Obter da TOTVS o procedimento oficial e completo para configurar, carregar, validar e diagnosticar regras de incentivo cadastradas no ERP Consinco, garantindo que o PDV aplique o preço correto ao cliente identificado pelo CRM ROCK.

## Escopo do chamado preparado

O documento de abertura solicita à TOTVS:

1. fluxo técnico oficial entre ERP, carga, Acrux Monitor e PDV;
2. relação completa dos parâmetros obrigatórios e seus escopos;
3. sequência de atualização, geração de carga, envio de configuração e reinício;
4. aplicação e campos corretos para cadastro da regra na versão instalada;
5. forma de associação entre cliente identificado e Preço 2;
6. definição do papel do CRM ROCK na elegibilidade e na concessão de descontos;
7. consultas, arquivos e logs para rastreamento ponta a ponta;
8. versões e service packs homologados;
9. tratamento de conflitos com preço promocional, combos e outras promoções;
10. exemplo completo de homologação.

## Documentação preservada

- [Documento preparado para abertura do chamado](../referencias/tecnicas/regra-incentivo-erp-pdv/chamado-totvs-integracao-consinco-crm-rock.docx);
- [evidência do parâmetro REGRA_INTEGRADOERP_LINUX](../referencias/tecnicas/regra-incentivo-erp-pdv/evidencia-parametro-regra-integradoerp-linux.png);
- [registro das referências oficiais consultadas](../referencias/tecnicas/regra-incentivo-erp-pdv/referencias-oficiais.md);
- [documentação técnica original da integração PDV](../referencias/tecnicas/totvs-documentacao-integracao-pdv.pdf);
- [resumo e checklist da documentação original](../referencias/tecnicas/resumo-integracao-pdv.md).

## Próximas ações

1. Confirmar versões do ERP, Acrux Monitor, PDV e service packs do ambiente afetado.
2. Informar empresa, loja, PDV, sequencial da regra, produto, embalagem e preços do caso de teste.
3. Confirmar se foram executados `Atualizar F4`, geração de carga, envio ao PDV e reinício.
4. Abrir o chamado na TOTVS e registrar o número nesta demanda.
5. Executar o teste de homologação orientado pela TOTVS com cliente elegível e não elegível.
6. Preservar os logs do ERP, carga, Acrux, PDV e integrador no mesmo intervalo de tempo.
7. Registrar causa, correção, evidências e resultado final nesta demanda.

## Condição de encerramento

A demanda poderá ser encerrada quando:

- o procedimento de configuração estiver documentado e validado;
- a regra de teste puder ser localizada na carga e no PDV;
- o cliente elegível receber o preço de incentivo nas condições cadastradas;
- os registros técnicos permitirem rastrear o fluxo ponta a ponta;
- o comportamento com outras promoções estiver definido;
- o chamado da TOTVS contiver a solução e as evidências de homologação.

## Segurança da informação

O PDF técnico contém credenciais padrão de homologação. Esses valores não devem ser reproduzidos no chamado, em capturas ou em registros versionados. Caso a TOTVS precise de acesso, as credenciais devem ser transmitidas pelo canal seguro definido para o atendimento.

