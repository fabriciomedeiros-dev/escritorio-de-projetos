from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
W, H = 1920, 1080
BG = '#0b1730'
CARD = '#132645'
CARD2 = '#183151'
WHITE = '#f4f7fb'
MUTED = '#a9bad1'
CYAN = '#39d8c2'
GOLD = '#ffbd59'
PURPLE = '#b793ff'
RED = '#ff817d'
GREEN = '#75df9f'


def text(x, y, value, size=32, color=WHITE, weight=500, anchor='start', letter=0):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" letter-spacing="{letter}">{escape(value)}</text>'

def rect(x,y,w,h,fill=CARD,rx=26,stroke='none',sw=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def circle(cx,cy,r,fill,stroke='none',sw=0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1,y1,x2,y2,color,sw=4,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" fill="none"{d}/>'

def base(n, label, headline, sub=''):
    e=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',
       '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1730"/><stop offset="1" stop-color="#132b4d"/></linearGradient><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#39d8c2" stop-opacity=".24"/><stop offset="1" stop-color="#b793ff" stop-opacity=".08"/></linearGradient></defs>',
       '<rect width="1920" height="1080" fill="url(#bg)"/>',
       circle(1690,120,300,'url(#glow)'), circle(160,920,360,'#0f2340'),
       text(108,74,'ESCRITÓRIO DE PROJETOS  /  ESTRATÉGIA DE TI',20,MUTED,700,letter=2),
       text(108,157,label.upper(),20,CYAN,700,letter=2),
       text(108,244,headline,62,WHITE,700)]
    if sub: e.append(text(110,300,sub,28,MUTED,400))
    e.append(line(108,1017,1812,1017,'#355072',2))
    e.append(text(108,1054,'OKRs orientam o roadmap. Valoração demonstra a contribuição.',20,MUTED,500))
    e.append(text(1812,1054,f'{n:02d}  /  08',20,MUTED,700,'end',1))
    return e

def save(n, elements):
    (OUT/f'slide-{n:02d}.svg').write_text(''.join(elements+['</svg>']))

# 1 — Opening
s=base(1,'Decisão estratégica','OKRs + VALORAÇÃO DE TI','Da estratégia ao roadmap — e do projeto à evidência.')
s += [rect(110,390,785,375,CARD,32),
      text(160,472,'O que queremos mudar?',35,MUTED,500),
      text(160,552,'Objetivos claros.',48,WHITE,700),
      text(160,615,'Resultados que importam.',48,WHITE,700),
      text(160,678,'Projetos escolhidos por contribuição.',34,CYAN,600),
      circle(1390,575,218,'#112846','#335576',3),circle(1390,575,158,'none',CYAN,8),circle(1390,575,96,'none',GOLD,8),circle(1390,575,30,CYAN),
      line(1390,575,1582,436,GOLD,7),circle(1582,436,16,GOLD),
      text(1390,846,'VALOR COMPROVADO',24,CYAN,700,'middle',2),
      text(1390,888,'alinha · compara · mede',24,MUTED,500,'middle')]
save(1,s)

# 2 — OKR components
s=base(2,'A lógica do OKR','A estratégia organiza as escolhas','Cada peça tem uma função — e uma pergunta própria.')
items=[('01','OBJETIVO','Qual macro resultado|a empresa busca?',CYAN),('02','RESULTADOS-CHAVE','Quais mudanças mostram|que chegamos ao resultado?',GOLD),('03','INDICADORES','Que medida mostra o|avanço e o resultado?',PURPLE),('04','AÇÕES / PROJETOS','Que iniciativa pode|contribuir para os KRs?',GREEN)]
for i,(num,head,desc,col) in enumerate(items):
    x=108+i*432
    s += [rect(x,395,392,342,CARD,28,stroke=col,sw=2),circle(x+58,456,28,col),text(x+58,465,num,18,BG,800,'middle'),text(x+34,529,head,25,col,700)]
    for j,desc_line in enumerate(desc.split('|')):
        s += [text(x+34,590+j*38,desc_line,24,WHITE,500)]
    if i<3:
        s += [line(x+394,566,x+424,566,'#607b9c',4),text(x+410,555,'›',44,MUTED,600,'middle')]
s += [rect(108,798,1704,118,'#10213c',24),text(150,870,'Regra prática',24,GOLD,700),text(385,870,'O projeto entra como ação candidata. O resultado de negócio continua sendo o KR.',30,WHITE,600)]
save(2,s)

# 3 — roadmap gate
s=base(3,'Seleção do roadmap','Projeto é ação. KR é resultado.','A proposta precisa mostrar o caminho entre a entrega e o objetivo estratégico.')
# vertical flow
s += [rect(120,390,420,138,CARD,25,stroke=CYAN,sw=3),text(160,446,'OBJETIVO',21,CYAN,700,letter=2),text(160,496,'Resultado macro da empresa',28,WHITE,600),
      line(330,530,330,584,'#7691b3',5),text(360,566,'↓',42,CYAN,700),
      rect(120,590,420,138,CARD,25,stroke=GOLD,sw=3),text(160,646,'KR',21,GOLD,700,letter=2),text(160,696,'Mudança mensurável desejada',28,WHITE,600),
      line(540,660,710,660,CYAN,6),text(630,632,'CONTRIBUI',18,CYAN,700,'middle',1),
      rect(710,512,300,292,CARD2,28),text(860,575,'PROJETO',22,PURPLE,700,'middle',2),text(860,640,'Ação',36,WHITE,700,'middle'),text(860,692,'candidata',30,WHITE,500,'middle'),text(860,753,'Como move o KR?',24,MUTED,500,'middle'),
      line(1010,660,1120,660,'#7691b3',5),text(1070,630,'?',38,GOLD,800,'middle'),
      rect(1120,390,660,138,CARD,25),text(1160,447,'AVALIAÇÃO PARA O ROADMAP',22,CYAN,700,letter=1),text(1160,498,'Contribuição · evidência · custo · capacidade · risco',25,WHITE,500),
      rect(1120,590,660,138,CARD,25),text(1160,647,'DECISÃO HUMANA',22,GOLD,700,letter=1),text(1160,698,'Priorizar · pilotar · aguardar dados · não priorizar',25,WHITE,500),
      text(120,876,'Sem vínculo claro a um objetivo e a um KR, reavaliamos a proposta antes de reservar capacidade.',28,MUTED,500)]
save(3,s)

# 4 — concrete example
s=base(4,'Exemplo de aplicação','Acordos com fornecedores','Objetivo de negócio → resultado desejado → indicadores → projeto candidato.')
s += [rect(108,375,770,540,CARD,30),text(158,442,'OBJETIVO',21,CYAN,700,letter=2),text(158,498,'Aumentar o cumprimento e a',36,WHITE,700),text(158,547,'transparência dos acordos.',36,WHITE,700),
      line(158,589,823,589,'#355072',2),text(158,645,'KR',21,GOLD,700,letter=2),text(158,696,'Ampliar a visibilidade das compras',29,WHITE,600),text(158,739,'frente aos volumes negociados.',29,WHITE,600),
      text(158,806,'INDICADORES',19,PURPLE,700,letter=2),text(158,852,'% do volume cumprido · tempo para tratar desvios',24,MUTED,500),
      rect(945,375,867,540,'#10213c',30),text(1000,442,'AÇÃO CANDIDATA',21,GREEN,700,letter=2),text(1000,499,'Visibilidade de contratos',38,WHITE,700),text(1000,550,'e automação da apuração',32,WHITE,500),
      # three illustrative nodes and small bars
      circle(1095,680,42,CYAN),text(1095,692,'1',30,BG,800,'middle'),circle(1375,680,42,GOLD),text(1375,692,'2',30,BG,800,'middle'),circle(1650,680,42,PURPLE),text(1650,692,'3',30,BG,800,'middle'),
      line(1137,680,1333,680,'#6c86a7',4),line(1417,680,1608,680,'#6c86a7',4),
      text(1095,756,'REGISTRAR',19,MUTED,700,'middle'),text(1375,756,'COMPARAR',19,MUTED,700,'middle'),text(1650,756,'CORRIGIR',19,MUTED,700,'middle'),
      rect(1000,806,755,62,'#1b3655',18),text(1377,846,'Aprovar se a contribuição, o custo e a capacidade fizerem sentido',21,WHITE,600,'middle')]
save(4,s)

# 5 — broad value dimensions
s=base(5,'O que conta como valor','Valor vai além da receita','Benefícios econômicos e operacionais podem mover os resultados estratégicos.')
# left cards
cards=[('EFICIÊNCIA','Menos tempo por atendimento',CYAN),('QUALIDADE','Mais acuracidade; menos erros',GOLD),('CAPACIDADE','Menos retrabalho; mais entrega',PURPLE),('CONFIANÇA','Menos risco; melhor serviço',GREEN)]
for i,(title,desc,col) in enumerate(cards):
    x=108+(i%2)*462;y=390+(i//2)*192
    s += [rect(x,y,425,154,CARD,25),circle(x+48,y+48,12,col),text(x+80,y+57,title,21,col,700,letter=1),text(x+34,y+112,desc,25,WHITE,500)]
# illustrative chart right
s += [rect(1080,390,732,540,'#10213c',30),text(1130,450,'EXEMPLO ILUSTRATIVO',19,GOLD,700,letter=2),text(1130,508,'Tempo de atendimento',32,WHITE,700),
      text(1150,588,'ANTES',18,MUTED,700,letter=1),rect(1300,558,390,40,'#293e5c',14),
      text(1150,675,'DEPOIS',18,MUTED,700,letter=1),rect(1300,645,195,40,CYAN,14),
      text(1730,587,'10 min',24,WHITE,700,'end'),text(1730,674,'5 min',24,CYAN,700,'end'),
      circle(1398,807,54,'#153b4b'),text(1398,817,'−50%',26,CYAN,800,'middle'),text(1480,816,'menos tempo por atendimento',24,MUTED,500),
      text(108,886,'A redução de quadro não se presume: só é benefício quando o resultado for confirmado e validado.',24,MUTED,500)]
save(5,s)
# Keyframes for the illustrative before/after chart reveal.
svg5=(OUT/'slide-05.svg').read_text()
for step,(bar,label) in enumerate([(390,'10 min'),(340,'8,7 min'),(292,'7,5 min'),(244,'6,3 min'),(195,'5 min')]):
    frame=svg5.replace('x="1300" y="645" width="195" height="40"','x="1300" y="645" width="%d" height="40"'%bar)
    color=WHITE if step<4 else CYAN
    frame=frame.replace('x="1730" y="674" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="%s" text-anchor="end">5 min'%CYAN, 'x="1730" y="674" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="%s" text-anchor="end">%s'%(color,label))
    (OUT/f'slide-05-step-{step}.svg').write_text(frame)

# 6 — make or buy
s=base(6,'Comparar alternativas','Desenvolver ou contratar?','Avaliar o mesmo escopo e horizonte; comparar custo total e capacidade.')
# vendor card
s += [rect(108,380,800,510,CARD,30,stroke=GOLD,sw=2),text(158,446,'SOLUÇÃO EXTERNA',22,GOLD,700,letter=2),text(158,514,'R$ 10.000',43,WHITE,700),text(158,551,'implantação',20,MUTED,500),text(495,514,'+',38,MUTED,700),text(560,514,'R$ 800',43,WHITE,700),text(560,551,'por mês',20,MUTED,500),
      line(158,594,856,594,'#355072',2),text(158,673,'R$ 19.600',58,GOLD,800),text(158,715,'no primeiro ano',25,WHITE,500),text(158,790,'antes de tributos, integração e outros custos',22,MUTED,500),
      rect(1010,380,802,510,CARD,30,stroke=CYAN,sw=2),text(1060,446,'DESENVOLVIMENTO INTERNO',22,CYAN,700,letter=2),text(1060,514,'Não é custo zero',43,WHITE,700),
      text(1060,592,'Horas da equipe + infraestrutura',27,WHITE,500),text(1060,642,'Suporte + manutenção + evolução',27,WHITE,500),text(1060,692,'Capacidade desviada de outras prioridades',27,WHITE,500),
      # meters
      rect(1060,761,634,20,'#243c5d',10),rect(1060,761,452,20,CYAN,10),text(1060,825,'Calcular TCO no mesmo horizonte',23,CYAN,700),
      text(108,944,'Exemplo financeiro ilustrativo. Cenário interno e custos recorrentes devem ser levantados antes da decisão.',22,MUTED,500)]
save(6,s)

# 7 — decision gate
s=base(7,'Decisão de roadmap','Contribuição + viabilidade','A gestão decide com uma visão comparável — sem reduzir valor a uma só cifra.')
criteria=[('ALINHAMENTO','Objetivo e KR claros',CYAN),('IMPACTO','Resultado e indicador',GOLD),('EVIDÊNCIA','Base, fonte e método',PURPLE),('CUSTO TOTAL','Interno e externo',GREEN),('CAPACIDADE','Prazo e prioridades',CYAN),('RISCO','Dependências e adoção',GOLD)]
for i,(head,desc,col) in enumerate(criteria):
    x=108+(i%3)*570;y=385+(i//3)*180
    s += [rect(x,y,530,140,CARD,24),circle(x+48,y+48,13,col),text(x+80,y+57,head,20,col,700,letter=1),text(x+34,y+107,desc,25,WHITE,500)]
opts=[('PRIORIZAR',GREEN),('PILOTAR',CYAN),('AGUARDAR DADOS',GOLD),('NÃO PRIORIZAR',RED)]
for i,(label,col) in enumerate(opts):
    x=108+i*430
    s += [rect(x,790,392,92,'#122742',22,stroke=col,sw=2),text(x+196,847,label,22,col,700,'middle',1)]
save(7,s)

# 8 — post-delivery loop
s=base(8,'Acompanhar resultado','Medir depois. Aprender. Repriorizar.','A valoração continua após a aprovação e a entrega do projeto.')
# timeline
xpoints=[255,710,1165,1620]
steps=[('OBJETIVO','Direção estratégica',CYAN),('LINHA DE BASE','Antes do projeto',GOLD),('ENTREGA','Ação executada',PURPLE),('RESULTADO','KR medido depois',GREEN)]
for i,(head,desc,col) in enumerate(steps):
    x=xpoints[i]
    s += [circle(x,520,72,'#142b49',col,4),text(x,512,str(i+1),34,col,800,'middle'),text(x,653,head,21,col,700,'middle',1),text(x,698,desc,22,WHITE,500,'middle')]
    if i<3: s += [line(x+78,520,xpoints[i+1]-82,520,'#6682a4',5),text((x+xpoints[i+1])/2,499,'›',44,MUTED,700,'middle')]
# labels
labels=[('CONFIRMADO',GREEN),('ESTIMADO',GOLD),('HIPÓTESE',PURPLE)]
for i,(label,col) in enumerate(labels):
    x=350+i*455
    s += [rect(x,795,340,68,'#132846',18,stroke=col,sw=2),circle(x+31,829,8,col),text(x+58,837,label,20,col,700,letter=1)]
s += [text(960,932,'OKRs orientam a escolha. Evidências mostram se o valor esperado aconteceu.',27,WHITE,600,'middle')]
save(8,s)
