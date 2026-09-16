# Módulos — SuperSync

**Navegação:** [Projeto](projeto.md) · [Governança](governanca.md) · [Desenvolvimento](desenvolvimento.md) · [Serviços compartilhados](servicos-compartilhados.md) · [Tarefas](tarefas.md)

Inventário gerencial resumido. Componentes técnicos podem estar separados no código sem constituírem módulos gerenciais distintos.

| Módulo | Situação | Área / dono funcional | Responsabilidades e próximos pontos |
|---|---|---|---|
| Acordos Comerciais | Produção com evolução | Área de Contratos; Thamires (sobrenome a confirmar) | Reúne contratos, apuração e auditoria. Núcleo quase concluído; melhorias previstas para o próximo ciclo. |
| Cadastro de Contratos | Descontinuado | Substituído por Acordos Comerciais | Manter apenas como legado técnico até decisão sobre retirada. |
| Apuração de Grades | Produção estável | Comercial; Filipe Fachetti | Filipe responde pelos dados; Alexandro pelo desenvolvimento. Sem melhorias solicitadas. |
| Pricing | Piloto parado | A confirmar | Código ativo como piloto/teste, sem evolução prevista. |
| Inconformidades | Refinamento e desenvolvimento | TI; Fabrício Medeiros | Gestão de falhas em servidores e integrações. Filipe mantém informações; novas implementações previstas. |
| Envio de Dados | Produção | Fabrício Medeiros | TI opera; Comercial gera oportunidades; Financeiro/Contratos administra cobranças. Vincular envios aos contratos e alertar ausência de contrato. |
| Relatórios | Produção; serviço compartilhado | TI; Alexandro Nascimento e Filipe Fachetti | Autonomia para atender áreas. Registrar demandas não planejadas e sinalizar risco ao planejamento. |
| Dashboard | Planejado; fora de produção | Fabrício Medeiros | Um painel por módulo. Filipe responde pelos dados; Alexandro pelo desenvolvimento; dono de cada módulo valida seus indicadores. |
| Social Listening | Prova de conceito funcional em produção restrita | TI; Fabrício Medeiros | Sem rotina agendada. Acesso restrito à TI. Componentes podem ser reaproveitados no SAC após decisão formal. Fabrício informa mudanças de status. |
| Central do Associado | Implementação parcial; homologação a confirmar | Fabrício Medeiros, Alexandro Nascimento e Filipe Fachetti | Portal, usuários, lojas e auditoria implementados na `master` em `8c0478c`; executar testes, homologar permissionamento e reconciliar as frentes restantes com o cronograma até 14/10/2026. |

## Ainda a classificar

- Usuários e autenticação;
- Associados;
- Lojas como módulo interno independente da visão exposta pela Central do Associado;
- Análise de Promoções;
- demais componentes que venham a ser reconhecidos como módulos gerenciais.
