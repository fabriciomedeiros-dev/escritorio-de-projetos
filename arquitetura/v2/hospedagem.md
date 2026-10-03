# Comparação de hospedagem — versão 2

Data: 2026-10-03. Situação: comparação concluída; recomendação para decisão de Fabrício. Não há fornecedor aprovado, conta criada, contratação, implantação ou transferência de dados.

## Atualização — infraestrutura existente informada

Em 03/10/2026, após esta comparação, Fabrício informou servidor SuperSync com PostgreSQL e possibilidade de interfaces e controle de usuários. A recomendação atual passa a priorizar a avaliação dessa infraestrutura, com ambiente local isolado antes de mudanças e implementação por outra pessoa. Supabase permanece alternativa caso a infraestrutura existente não atenda aos requisitos; não houve contratação. Capacidade, versão, anexos e recuperação do servidor ainda não foram inspecionados. Consulte o [roteiro de implementação](implementacao-supersync.md).

## Requisitos e premissas

PostgreSQL central já foi escolhido. O escritório precisa ser acessível por vários computadores desde o início, com documentos originais centralizados, serviço autenticado e proteção independente. Inicialmente um usuário, depois três. O volume de dados, a infraestrutura interna disponível e a autorização para nuvem não foram estabelecidos. Valores abaixo são referências públicas em USD/mês, sem câmbio, impostos ou descontos temporários.

Banco, serviço, arquivos e cópia precisam de responsáveis e custos próprios. Recursos mínimos de provedores são referências de orçamento, não dimensionamento validado. Não comparar uma máquina sem proteção com um pacote gerenciado como se oferecessem o mesmo resultado.

## Alternativas

| Modelo | Desenho completo | Vantagem | Responsabilidade que permanece | Avaliação |
|---|---|---|---|---|
| Infraestrutura interna | Servidor/VM, PostgreSQL, serviço autenticado, arquivos, acesso remoto/VPN e cópia fora do host | Controle da infraestrutura e aproveitamento de recursos existentes | Patches, monitoramento, energia, conectividade, restauração, identidade e suporte | Preferir se já houver estrutura administrada com acesso e recuperação verificáveis |
| VM em nuvem autogerida | VM com serviço e PostgreSQL; arquivos em objetos ou volume; cópia em destino independente | Controle e custo direto inicial menor | Administração do SO e banco, capacidade, segurança de acesso, backups, falhas e restauração | Viável, mas transfere manutenção para a equipe; não é a recomendação inicial |
| PostgreSQL gerenciado + componentes separados | Banco gerenciado, VM/serviço de aplicação, armazenamento de objetos, identidade e cópia independente | Menos administração do banco, componentes substituíveis | Serviço, autenticação, modelo de dados, anexos, exportação e recuperação completa | Boa opção quando já houver uma plataforma de aplicação preferida |
| Plataforma gerenciada integrada | PostgreSQL, autenticação e armazenamento de objetos integrados; serviço próprio; cópia independente | Menos componentes para iniciar e preparar participação da equipe | Regras de negócio, permissões, serviço, exportação e proteção de arquivos | Recomendação inicial para avaliação de contratação, mantendo fronteiras portáveis |

O acesso remoto deve ocorrer pelo serviço do Escritório. Codex e outros agentes não precisam conhecer credenciais administrativas do banco. Não publicar o banco como interface dos usuários.

## Referências concretas e custos

### A — Supabase Pro, com serviço próprio

PostgreSQL, Auth e Storage gerenciados. Projeto na região de São Paulo é uma opção documentada; disponibilidade precisa ser verificada no provisionamento. O plano Pro parte de US$25/mês e contempla créditos suficientes para uma instância Micro, 8 GB de disco de banco e 100 GB de arquivos, sujeitos às franquias e excedentes. Backup diário do banco tem retenção de sete dias. [Preços](https://supabase.com/pricing), [regiões](https://supabase.com/docs/guides/platform/regions).

O serviço do Escritório pode rodar em runtime de funções ou host de aplicação. Não considerar que a API automática da plataforma substitui as operações de negócio. Funções têm limites de memória e tempo; extração extensa de documentos e exportações grandes precisam de execução adequada. Avaliar antes de definir runtime. [Limites de funções](https://supabase.com/docs/guides/functions/limits).

Orçamento comparável: US$25 para a plataforma + US$6–12 para um host pequeno do serviço, caso seja separado, + proteção independente e excedentes. Base indicativa US$31–37/mês; não é custo total contratado. O preço do host usa planos públicos da DigitalOcean apenas como referência; não recomenda separar regiões/provedores sem medir conectividade e tráfego. Se funções atenderem ao serviço, o host separado poderá ser dispensado; verificar franquias antes de recalcular. [Host de referência](https://www.digitalocean.com/pricing/droplets).

A documentação informa que backups do banco não incluem os objetos de Storage. PITR é adicional e não resolve essa lacuna de arquivos. Portanto, cópia própria de documentos e evidências é obrigatória para o desenho. [Backup e limitações](https://supabase.com/docs/guides/platform/backups).

Portabilidade: migrations SQL, esquema PostgreSQL, API própria e acesso a arquivos por adaptador. Storage oferece compatibilidade S3 com diferenças documentadas; compatibilidade não significa que todos os recursos de S3 estejam presentes. Dependência de Auth e identidade exige mapeamento de usuários e estratégia de substituição; não prometer migração transparente das credenciais. [Compatibilidade S3](https://supabase.com/docs/guides/storage/s3/compatibility).

### B — DigitalOcean PostgreSQL gerenciado + VM + Spaces

Composição indicativa: PostgreSQL de entrada anunciado a partir de US$15,15/mês, VM de 2 GiB a US$12/mês e Spaces a US$5/mês. Soma de referência US$32,15/mês, antes de eventuais componentes de disco configuráveis, proteção independente, excedentes e impostos. Conferir a configuração do banco na cotação; a tabela de preços apresenta disco ajustável. [Banco](https://www.digitalocean.com/pricing/managed-databases), [VM](https://www.digitalocean.com/pricing/droplets), [arquivos](https://www.digitalocean.com/pricing/spaces-object-storage).

Backup de PostgreSQL ocorre diariamente e é retido por sete dias; restauração cria novo nó primário. Isso não é a cópia dos arquivos em Spaces nem uma proteção em outra conta/provedor. O pacote de entrada não deve ser apresentado como alta disponibilidade garantida. Identidade e administração da VM de aplicação precisam ser resolvidas. [Restauração](https://docs.digitalocean.com/products/databases/postgresql/how-to/restore-from-backups/).

Escolher essa composição se houver preferência operacional por banco e aplicação separados. Verificar regiões comuns, latência e necessidade de localização no Brasil antes de contratar; esta avaliação não demonstrou uma região brasileira para todos esses componentes.

### C — VM autogerida

Referência: VM de 2 GiB a US$12/mês + armazenamento de arquivos Spaces a US$5/mês = US$17/mês de base, antes de snapshots, proteção independente, excedentes e impostos. Banco e serviço dividiriam a máquina; 2 GiB é apenas ponto de partida para ensaio, não capacidade comprovada. [VM](https://www.digitalocean.com/pricing/droplets), [arquivos](https://www.digitalocean.com/pricing/spaces-object-storage).

O custo direto menor não inclui horas de operação nem redundância. Falha do host interrompe banco e aplicação simultaneamente. Exige rotina verificável de backup consistente do PostgreSQL, versões suportadas, atualizações, alertas e restauração em outra máquina. Recomendação: considerar somente com responsável operacional definido e ensaio de recuperação.

### D — Infraestrutura interna

Não atribuir custo zero: incluir capacidade incremental, armazenamento, energia, VPN/conectividade, suporte, proteção externa e tempo de operação. O repositório documenta portal estático em Cloudflare Pages/Access, mas não demonstra um servidor interno PostgreSQL disponível nem sua capacidade. Portal de consulta não equivale a infraestrutura operacional pronta.

Inventário necessário para uma proposta interna: host disponível, memória/disco, responsável e substituto, acesso entre computadores, política de atualização, identidade, monitoramento, destino independente de proteção e tempo de restauração medido. Sem isso não há orçamento nem comparação de disponibilidade confiável.

## Proteção independente: banco e arquivos

Em todas as opções, definir exportação verificável de registros, histórico, aprovações e originais, com manifesto de IDs e checksums. Backup do provedor é uma camada de proteção, não substitui uma saída completa do sistema. Destino separado deve resistir a falha do host principal e evitar que uma mesma credencial de aplicação apague original e cópia.

Backblaze B2 é uma referência de destino, não fornecedor escolhido: preço anunciado a partir de US$6,95/TB/mês e primeiros 10 GB gratuitos, com custos/limites conforme operação e região. Preço baixo não autoriza assumir residência no Brasil ou compatibilidade com exigências da empresa. Alternativa: destino corporativo independente já existente, se comprovado. [Preços B2](https://www.backblaze.com/cloud-storage/pricing).

O volume faturável é o volume retido de cópias, não apenas a base atual. Exemplo sem franquias: 100 GB retidos × US$6,95/1.000 GB ≈ US$0,70/mês de armazenamento; tráfego, requisições, execução da rotina e impostos são separados. Não tratar essa conta como orçamento completo nem prometer custo zero.

Política inicial proposta para dimensionamento, ainda a validar: snapshot/exportação diária, proteção incremental mais frequente durante o uso, monitoramento de atraso e teste mensal de restauração. Backup diário sozinho permite perder registros posteriores à última cópia. A confirmação de gravação e o estado da proteção permanecem separados, conforme decisão já aprovada. Definir frequência e retenção com a tolerância real à perda, sem prometer perda zero.

## Recomendação original — anterior ao servidor informado

Minha recomendação arquitetural é começar a avaliação de contratação pelo Supabase Pro, com PostgreSQL, identidade e arquivos integrados, na região de São Paulo quando disponível. Ele reduz componentes administrados pela equipe e prepara o acesso dos subordinados. Preservar API de negócio própria, SQL versionado, originais exportáveis e cópia independente evita vincular a memória ao agente ou exclusivamente à plataforma.

Essa recomendação é inferência de adequação ao cenário de um a três usuários; não é aprovação de fornecedor, benchmark, SLA contratado nem prova de restauração hospedada. Se já existir infraestrutura corporativa administrada com recuperação comprovada, reavaliar a alternativa interna antes de contratar. Se for necessário SLA contratual, redundância ou outro limite de residência, recotar planos e regiões; não atribuir tais garantias aos pacotes mínimos.

## Decisão e próxima etapa

A comparação está pronta para revisão. Falta decidir interno versus gerenciado e definir orçamento mensal, responsável pela conta e operação e localização permitida dos dados/cópias. Nenhuma compra ou implantação será feita com essa recomendação apenas.

Enquanto a hospedagem estiver pendente, o esquema físico e o contrato das operações podem ser preparados independentemente do fornecedor. Depois de decidir, fazer piloto hospedado com dados sintéticos: autenticação de dois clientes diferentes, isolamento, gravação/verificação, perda de conexão/repetição, recuperação de anexos e restauração para destino novo. Só então migrar dados reais com conciliação e corte de autoridade.
