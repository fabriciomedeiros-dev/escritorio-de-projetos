# Referências oficiais — Regra de incentivo do ERP no PDV

**Projeto:** CRM Rock (antiga BNEX)  
**Linha de trabalho:** Nova integração Consinco X ROCK  
**Data da consulta:** 30/09/2026  
**Demanda relacionada:** [CRM-008](../../../demandas/2026-10-01-regra-incentivo-erp-pdv.md)

## Central de Atendimento TOTVS

### Ativação da integração de regras cadastradas via ERP

- **Título:** Varejo Supermercados - Parâmetro - Como Ativar a Integração para Utilizar Regras de Incentivo Cadastradas via ERP
- **URL:** <https://centraldeatendimento.totvs.com/hc/pt-br/articles/7372606697495-Varejo-Supermercados-Parametro-Como-Ativar-a-Integra%C3%A7%C3%A3o-para-Utilizar-Regras-de-Incentivo-Cadastradas-via-ERP>
- **Orientação relevante:** configurar `REGRA_INTEGRADOERP_LINUX`, no grupo `CARGA_PDV`, com valor `S` e executar `Atualizar F4`.
- **Limitação identificada:** o artigo não detalha a carga, os cadastros dependentes, os logs nem a validação no PDV.

### Aplicação de regra em produto promocional

- **Título:** Varejo Supermercados - Regras de Negócios - Regras de Incentivo - Conceder descontos em regras de incentivos ou combos e preço diferenciado por embalagens em produtos promocionais
- **URL:** <https://centraldeatendimento.totvs.com/hc/pt-br/articles/4402803479959-Varejo-Supermercados-Regras-de-Neg%C3%B3cios-Regras-de-Incentivo-Conceder-descontos-em-regras-de-incentivos-combos-e-pre%C3%A7o-diferenciado-por-embalagens-em-produtos-promocionais>
- **Orientação relevante:** quando o cenário envolver produto promocional, validar a opção `Aplica regra de incentivo em preço promocional`, salvar, enviar a configuração ao PDV e reiniciar a aplicação.

## TDN TOTVS

### Auditoria da manutenção de regras de incentivo

- **Título:** Implementação de log para auditoria na aplicação de regras de incentivo
- **URL:** <https://tdn.totvs.com/pages/viewpage.action?pageId=850704269>
- **Uso na tratativa:** referência para solicitar os registros de alteração de produto, embalagem, percentual, preço de incentivo, preço-base e quantidade limite, conforme disponibilidade na versão instalada.

### Leiaute de exportação para frentes de caixa

- **Título:** Leiaute Exportação de dados do ERP TOTVS Varejo Supermercados para frentes de caixas de terceiros
- **URL:** <https://tdn.totvs.com/pages/viewpage.action?pageId=833937528>
- **Uso na tratativa:** referência para solicitar à TOTVS a confirmação das estruturas, campos e processos efetivamente utilizados pelo PDV Consinco no ambiente.

## Observação

As páginas acima são referências de apoio. A aplicabilidade de cada parâmetro, aplicação, tabela ou comportamento depende da versão e da arquitetura instaladas e deve ser confirmada no chamado da TOTVS.

