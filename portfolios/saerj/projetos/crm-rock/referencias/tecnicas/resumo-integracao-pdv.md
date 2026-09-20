# Resumo técnico e checklist — Integração TOTVS PDV com CRM

**Documento de origem:** [TOTVS — Documentação integração PDV](totvs-documentacao-integracao-pdv.pdf)  
**Classificação:** Referência técnica de instalação/configuração  
**Efeito gerencial:** Não constitui tarefa, decisão, cronograma ou aceite do projeto  
**Revisão do resumo:** 14/09/2026

## Finalidade do documento

Orientar a configuração da integração externa de vendas no TOTVS Acrux Monitor e validar, em ambiente de homologação, o fluxo do PDV com o `integrator-totvs` e o IntegradorGSWS.

Embora chamado de documentação de integração/instalação, o conteúdo se concentra na parametrização do PDV e em um roteiro de teste de venda. O documento não descreve provisionamento de infraestrutura, instalação de componentes, observabilidade, contingência, retorno de versão ou implantação em produção.

## Resumo do fluxo

1. No Acrux Monitor, configura-se a integração externa de vendas do PDV com código de parceiro, autenticação e URLs dos eventos.
2. O checkout é associado ao endereço IP do PDV.
3. Ao iniciar uma venda, o PDV chama `/start` e recebe a pergunta de identificação de cliente fidelidade.
4. Se o cliente se identificar, o integrador consulta `setIdentificaCliente` no IntegradorGSWS.
5. Na etapa de pagamento, o PDV chama `/sub-total`; o integrador consulta novamente o cliente e recupera eventuais descontos.
6. Ao concluir o pagamento, o PDV chama `/finalization` com itens, pagamentos e descontos.
7. O `integrator-totvs` converte e trata os dados, monta o XML e notifica a venda no IntegradorGSWS.

## Pontos técnicos essenciais

- A reserva de desconto no IntegradorGSWS deve permanecer desabilitada segundo o documento, pois a identificação do cliente ocorre mais de uma vez durante a venda.
- O código de parceiro precisa ser único entre os parceiros configurados na TOTVS.
- A autenticação utiliza `idvarejista` e `x-api-key`; os valores devem ser obtidos por canal seguro.
- As URLs de callback devem apontar para os eventos correspondentes no `integrator-totvs`.
- A configuração do checkout depende do IP efetivo do PDV.
- No ambiente de teste descrito, a ausência de retaguarda limita o pagamento à opção dinheiro.
- As imagens de evidência de desconto foram produzidas em momentos distintos e podem não refletir exatamente a mesma execução.

## Checklist de configuração e validação

Este checklist serve como apoio à execução técnica. Marcar seus itens não altera o status das tarefas do projeto.

### Preparação

- [ ] Confirmar que o ambiente é de homologação e identificar o PDV/check-out que será utilizado.
- [ ] Obter por canal seguro as credenciais vigentes do Acrux Monitor e do PDV; não copiá-las para evidências ou documentos versionados.
- [ ] Obter o `idvarejista`, a `x-api-key`, o código de parceiro e as URLs do ambiente correto.
- [ ] Confirmar que o código de parceiro é único na configuração TOTVS.
- [ ] Confirmar o endereço IP do PDV com `IPCONFIG` ou mecanismo equivalente.
- [ ] Registrar os valores atuais da parametrização para possibilitar restauração em caso de falha.
- [ ] Confirmar com os responsáveis que a reserva de desconto do IntegradorGSWS pode permanecer desabilitada durante o fluxo.

### Configuração no Acrux Monitor

- [ ] Acessar o Acrux Monitor no endereço do ambiente autorizado.
- [ ] Navegar até `Configurações > Configurações de PDVs > Integrações Externas > Vendas > Integração 001`.
- [ ] Informar o código de parceiro validado.
- [ ] Configurar `idvarejista` e `x-api-key` sem expor os valores em capturas ou logs.
- [ ] Configurar as URLs de integração dos eventos do `integrator-totvs`.
- [ ] Salvar a configuração e confirmar que não houve erro de validação.
- [ ] Navegar até `Cadastro > Empresas > Checkouts`.
- [ ] Configurar o IP correto do PDV e salvar.

### Preparação do teste no PDV

- [ ] Abrir o caixa no PDV.
- [ ] Se houver aviso de terminal desatualizado, autenticar com uma credencial autorizada e registrar a versão observada.
- [ ] Informar o suprimento/troco solicitado até concluir a abertura.
- [ ] Selecionar um produto com unidade e estoque disponíveis.

### Validação de início da venda (`/start`)

- [ ] Iniciar a venda e confirmar que o PDV apresenta a pergunta de fidelidade configurada.
- [ ] Testar a resposta negativa e confirmar que o fluxo retorna `completed`, permitindo continuar sem identificação.
- [ ] Testar a resposta positiva e confirmar a solicitação de CPF/CNPJ.
- [ ] Informar um documento de teste pertencente ao clube e confirmar o retorno esperado de cliente fidelidade.
- [ ] Informar um documento de teste não pertencente ao clube e confirmar o tratamento esperado sem incentivo.
- [ ] Verificar nos registros técnicos que as chamadas a `/start` e `setIdentificaCliente` ocorreram sem expor dados pessoais na evidência.

### Validação de subtotal e descontos (`/sub-total`)

- [ ] Selecionar pagamento em dinheiro no ambiente de teste descrito.
- [ ] Confirmar a chamada a `/sub-total`.
- [ ] Para cliente identificado, confirmar a nova consulta a `setIdentificaCliente`.
- [ ] Usar produto e regra de incentivo válidos para o ambiente atual; não depender dos valores ilustrativos do PDF.
- [ ] Confirmar que o desconto esperado é aplicado e que subtotal, desconto e total permanecem consistentes.

### Validação da finalização (`/finalization`)

- [ ] Concluir o pagamento.
- [ ] Confirmar a chamada a `/finalization`.
- [ ] Validar que itens, pagamentos, descontos e identificadores necessários foram enviados.
- [ ] Confirmar que o `integrator-totvs` gerou o XML sem erro.
- [ ] Confirmar o recebimento/notificação da venda no IntegradorGSWS.
- [ ] Confrontar o total da venda no PDV com o total recebido no destino.

### Evidências e encerramento

- [ ] Registrar data, ambiente, PDV, checkout, versões e responsáveis pelo teste.
- [ ] Preservar identificadores de correlação, horários e resultados das APIs necessários à rastreabilidade.
- [ ] Ocultar credenciais, CPF/CNPJ e outros dados sensíveis das evidências.
- [ ] Registrar cenários testados e resultados: cliente fidelidade, não fidelidade, desconto e finalização.
- [ ] Registrar qualquer divergência entre a documentação e o comportamento da versão instalada.
- [ ] Se houver falha, restaurar a parametrização anterior conforme o procedimento autorizado e preservar os registros para análise.

## Lacunas da documentação original

Antes de uma implantação produtiva, são necessárias referências complementares para:

- URLs e credenciais específicas por ambiente;
- matriz de compatibilidade e versões suportadas;
- requisitos de rede, firewall, certificados e DNS;
- instalação e configuração do próprio `integrator-totvs`;
- logs, métricas, alertas e identificadores de correlação;
- política de tentativas, duplicidade, idempotência e reprocessamento;
- contingência, retorno à versão anterior e recuperação de vendas não notificadas;
- critérios formais de homologação e aceite;
- proteção e retenção de CPF/CNPJ, credenciais e demais dados sensíveis;
- procedimento de implantação em produção e responsabilidades entre Rede, Rock, TOTVS/Consinco.

Essas lacunas são observações técnicas para futuras consultas. Elas não foram convertidas em tarefas do projeto.
