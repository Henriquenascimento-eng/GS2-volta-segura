# Uso de Inteligência Artificial

Este arquivo documenta como o grupo usou ferramentas de IA no desenvolvimento da aplicação Python da Volta Segura, como pede a disciplina Computational Thinking with Python.

## 1. Ferramentas de IA utilizadas

| Ferramenta | Finalidade |
|---|---|
| Claude (claude.ai) | Ler o PDF do desafio, levantar ideias de tema, ajudar o grupo a escolher a Volta Segura, montar a especificação do programa e gerar a primeira versão do código, dos dados simulados e da documentação |
| Claude Code | Revisar e corrigir o código gerado, analisar se todos os requisitos da disciplina foram atendidos e ajustar o que o grupo pediu |

## 2. Prompts utilizados

### 2.1 Escolha do tema (Claude)

> "Leia este PDF, entenda o que está sendo pedido e me faça perguntas para te guiar. No final precisamos decidir um tema específico em que vamos focar: me mande 5 opções e eu vou avaliar cada uma delas."

Depois das perguntas sobre o grupo, os bairros, as pessoas que podíamos entrevistar e os problemas do dia a dia, a IA trouxe duas rodadas de opções. O grupo pediu ideias novas ("eu preciso ter novas ideias, porque estas não estão boas") e escolheu a opção **Volta Segura**.

### 2.2 Estrutura do programa (Claude)

> "Agora nós vamos focar na estrutura Python. Cada um terá sua matéria e a nossa será Python."

> "Vamos começar a fazer o prompt para o Claude Code fazer a parte em Python e as pastas, commits, branches, dentre outras coisas."

O resultado foi a especificação completa da seção 2.4, que define requisitos, estrutura de arquivos, modelo de dados, regras de negócio, branches e commits.

### 2.3 Geração do código (Claude)

> "Faça o projeto daqui. Depois a gente pede para o Claude Code corrigir e analisar o que foi feito."

### 2.4 Especificação usada para gerar o código

<details>
<summary>Clique para ver a especificação completa</summary>

## Contexto

Você vai construir a parte **Python** de um projeto de faculdade (FIAP, Engenharia de Software, 1º ano), da disciplina **Computational Thinking with Python**, dentro da Global Solution 2026.2 (desafio CitizenTech). O prazo é 19/11/2026.

O projeto do grupo se chama **Volta Segura**: um poste inteligente + app que ajuda quem desce do metrô à noite (estações Tatuapé, Belém e Bresser-Mooca, em São Paulo) a voltar a pé para casa pelo caminho mais iluminado e seguro.

**Problema, em uma frase:** quem desce do metrô à noite caminha por ruas com postes apagados e calçadas ruins, sem saber qual caminho é mais seguro.

A parte Python é o "cérebro" do sistema, rodando no terminal: cadastra trechos de rua, registra ocorrências (poste apagado, calçada quebrada), calcula uma nota de segurança por trecho, recomenda a rota mais segura e simula a lógica do poste inteligente (a mesma lógica do ESP32 da disciplina de Edge Computing).

**Quem vai ler e explicar este código são alunos do 1º ano.** O professor pode pedir para qualquer integrante explicar qualquer linha. Então:
- código simples, didático e bem comentado **em português**;
- nada de truques, compreensões de lista aninhadas, lambdas, classes, decorators ou bibliotecas externas;
- prefira clareza a elegância.

## Restrições obrigatórias da disciplina

Use **apenas** a biblioteca padrão, e dela somente `json` e `os`. Nada de `pip install`. Python 3.10+ (por causa do `match/case`).

O código **precisa** demonstrar, de forma visível, cada item abaixo:

| Requisito | Onde deve aparecer |
|---|---|
| Menu de opções | menu principal + submenus |
| Validação das entradas do usuário | funções de leitura que repetem a pergunta até a entrada ser válida (número fora do intervalo, texto vazio, id inexistente, opção inválida) |
| `try/except` | conversão de texto para `int`/`float`; leitura de JSON quando o arquivo não existe ou está corrompido |
| `if/elif/else` | faixas da nota de segurança e estados do poste |
| `match/case` | escolha das opções do menu e tratamento do tipo de ocorrência |
| `while` | loop do menu e repetição da pergunta até a entrada ser válida |
| `for` | percorrer trechos, ocorrências e rotas; montar relatórios |
| Funções com parâmetros e retorno | todas as regras de negócio (ex.: `calcular_nota(trecho, ocorrencias) -> float`) |
| Listas | listas de trechos, ocorrências e rotas |
| Tuplas | a `faixa` de numeração do trecho, como `(100, 400)`, e as opções fixas como `TIPOS_OCORRENCIA = ("poste_apagado", ...)` |
| Dicionários | cada trecho, ocorrência e rota |
| JSON (leitura **e** gravação) | dados salvos em arquivos `.json` a cada alteração e carregados ao iniciar |
| Boas práticas | nomes claros em português, constantes em MAIÚSCULO, funções curtas, uma responsabilidade por função, comentários e docstrings simples |
| Boa experiência do usuário | mensagens claras, títulos de seção, confirmação antes de excluir, "Pressione Enter para continuar", tabelas alinhadas no terminal |

⚠️ **Módulos:** a estrutura abaixo usa vários arquivos `.py` com `import`. Se o grupo avisar que `import` entre arquivos próprios não foi visto em aula, faça tudo em um único `main.py`, separado em seções comentadas, mantendo as mesmas funções.

## Estrutura do repositório

O repositório é do grupo inteiro, com uma pasta por disciplina. Você cuida **só da pasta `python/`** e do esqueleto da raiz. Não mexa nas pastas das outras disciplinas além de criá-las vazias com um `.gitkeep`.

```
volta-segura/
├── README.md                 # visão geral do projeto + Ficha da CitizenTech
├── .gitignore
├── python/
│   ├── main.py               # ponto de entrada: menu principal e loop while
│   ├── dados.py              # carregar_json / salvar_json (com try/except)
│   ├── validacoes.py         # ler_inteiro, ler_float, ler_texto, ler_opcao, confirmar
│   ├── trechos.py            # CRUD de trechos de rua
│   ├── ocorrencias.py        # CRUD de ocorrências
│   ├── seguranca.py          # nota do trecho, rota mais segura, estado do poste
│   ├── relatorio.py          # relatório geral por bairro
│   ├── interface.py          # títulos, linhas, pausar, limpar tela, imprimir tabelas
│   ├── data/
│   │   ├── trechos.json
│   │   ├── ocorrencias.json
│   │   └── rotas.json
│   ├── readme.md             # descritivo do projeto Python (entregável)
│   ├── prompt.md             # documentação do uso de IA (entregável)
│   └── docs/
│       └── guia_de_estudo.md # explicação de cada arquivo para o grupo estudar (NÃO vai no ZIP)
├── edge/.gitkeep
├── dps/.gitkeep
├── frontend/.gitkeep
├── tx-design/.gitkeep
└── storytelling/.gitkeep
```

## Modelo de dados

**Trecho** (`trechos.json`, lista de dicionários):
```json
{
  "id": 1,
  "bairro": "Tatuapé",
  "rua": "Rua Tuiuti",
  "faixa": [100, 400],
  "postes_total": 8,
  "postes_apagados": 3,
  "calcada": "ruim"
}
```
- `faixa` é salva como lista no JSON (JSON não tem tupla) e **convertida para tupla ao carregar**. Comente isso no código: é uma ótima pergunta de apresentação.
- `calcada` só aceita valores da tupla `CONDICOES_CALCADA = ("boa", "regular", "ruim")`.
- Valide: `postes_apagados <= postes_total`, `faixa[0] < faixa[1]`, números não negativos.

**Ocorrência** (`ocorrencias.json`):
```json
{ "id": 1, "trecho_id": 1, "tipo": "poste_apagado", "descricao": "Poste em frente ao 250", "status": "aberta" }
```
- `tipo` ∈ `TIPOS_OCORRENCIA = ("poste_apagado", "calcada_quebrada", "rua_escura", "outro")`
- `status` ∈ `STATUS_OCORRENCIA = ("aberta", "em_analise", "resolvida")`
- Use `match/case` sobre o `tipo` para gerar uma orientação diferente para cada um (ex.: poste apagado → "encaminhar para a concessionária de iluminação").
- Não peça nome, telefone ou qualquer dado pessoal de quem reporta.

**Rota** (`rotas.json`): uma rota é uma sequência de trechos da estação até um destino.
```json
{ "id": 1, "estacao": "Tatuapé", "destino": "Casa A", "trechos": [1, 3, 4] }
```

**IDs:** gere sempre o próximo id como "maior id existente + 1". Nunca reutilize id.

## Regras de negócio

Coloque todos os números abaixo como **constantes no topo de `seguranca.py`**, com um comentário explicando cada uma.

### 1. Nota de segurança do trecho (0 a 10)
- **Iluminação:** `(postes acesos / postes total) × 6`. Se `postes_total == 0`, iluminação = 0.
- **Calçada:** boa = 2,5 · regular = 1,5 · ruim = 0,5
- **Ocorrências abertas** ou em análise naquele trecho: −0,5 cada, desconto máximo de −1,5
- **Resultado:** limitado entre 0 e 10, arredondado para 1 casa decimal.
- **Classificação** (com `if/elif/else`): `>= 7` → "VERDE (seguro)" · `>= 4` → "AMARELO (atenção)" · senão → "VERMELHO (evitar)"

### 2. Rota mais segura
- O usuário escolhe a estação. O programa lista os destinos disponíveis para ela e, para cada rota, calcula a nota de cada trecho.
- **A rota vencedora é a que tem a maior nota mínima**, não a maior média. Um único trecho escuro já torna o caminho inseguro: é o "elo mais fraco". Mostre também a média como informação extra.
- Em caso de empate na nota mínima, vence a maior média.
- Exiba um passo a passo: trecho por trecho, com a nota e a classificação.

### 3. Simulação do poste (mesma lógica do ESP32)
O usuário informa: se é noite (s/n), a leitura de luz do LDR (0 a 1023) e se há pedestre (s/n). O programa devolve o estado e a ação:

| Condição | Estado | Ação |
|---|---|---|
| Leitura fora de 0–1023, ou não numérica | LEITURA INVÁLIDA | "Verificar sensor" |
| Dia | DESLIGADO (DIA) | lâmpada desligada |
| Noite, leitura < `LIMITE_LAMPADA_APAGADA` (ex.: 200) | APAGADO / FALHA | "Alerta enviado: lâmpada queimada" + oferece registrar uma ocorrência automaticamente no trecho escolhido |
| Noite, lâmpada ok, com pedestre | PEDESTRE | luz em 100% |
| Noite, lâmpada ok, sem pedestre | ECONOMIA | luz em 30% |

Deixe os limites como constantes com o comentário: `# Mesmo valor usado no código do ESP32 (pasta edge/). Se mudar aqui, avise quem cuida do Edge.`

### 4. Relatório geral
Por bairro: número de trechos, nota média, trecho mais crítico, ocorrências abertas por tipo e % de postes apagados. Feche com uma linha de "indicador de impacto": % de trechos verdes no total.

## Menu

```
================ VOLTA SEGURA ================
  Caminho iluminado da estação até em casa
==============================================
1. Trechos de rua        (cadastrar, listar, editar, remover)
2. Ocorrências           (registrar, listar, atualizar status, remover)
3. Simular poste inteligente
4. Nota de segurança de um trecho
5. Rota mais segura
6. Relatório geral
0. Sair
```
- Use `match/case` para tratar a opção escolhida.
- Os submenus têm "0. Voltar".
- Antes de remover qualquer coisa, peça confirmação (s/n).
- Ao remover um trecho que tem ocorrências ou está em rotas, avise e não deixe remover (é uma regra de negócio para justificar no TX Design).
- O programa nunca pode quebrar com uma entrada errada: todo `input` passa pelas funções de `validacoes.py`.

## Dados iniciais (simulados)

Popule os JSON com dados **fictícios, mas plausíveis**, para a demonstração:
- 8 a 10 trechos em ruas próximas às estações Tatuapé, Belém e Bresser-Mooca, com notas variadas: alguns verdes, alguns amarelos, alguns vermelhos;
- 5 ocorrências em status diferentes;
- 4 rotas (pelo menos 2 saindo da mesma estação para o mesmo destino, para a comparação fazer sentido).

Escreva no `readme.md` que os dados são **simulados**, criados para demonstração, sem dados pessoais. Se os arquivos JSON não existirem ao iniciar, o programa cria com lista vazia, sem quebrar.

## Git: branches e commits

Trabalhe como um time profissional, para o histórico mostrar a evolução do projeto.

**Branches:**
- `main`: só código estável e entregável
- `develop`: integração
- `feature/<nome>`: uma por funcionalidade, criada a partir da `develop`. Use, nesta ordem:
  1. `feature/estrutura-inicial`: pastas, `.gitignore`, README raiz, `dados.py`, `interface.py`
  2. `feature/validacoes`
  3. `feature/crud-trechos`
  4. `feature/crud-ocorrencias`
  5. `feature/nota-seguranca`
  6. `feature/rota-segura`
  7. `feature/simulacao-poste`
  8. `feature/relatorio`
  9. `feature/documentacao`: `readme.md`, `prompt.md`, `guia_de_estudo.md`
- Ao terminar cada feature: merge na `develop` com `--no-ff`. No fim, merge da `develop` na `main` e uma tag `v1.0-entrega-gs`.

**Commits:** pequenos e frequentes (vários por feature), em português, no padrão Conventional Commits:
- `feat: adiciona cadastro de trechos com validação de faixa`
- `fix: impede postes apagados maiores que o total`
- `refactor: extrai função de leitura de inteiro`
- `docs: adiciona ficha da CitizenTech ao README`
- `chore: cria estrutura de pastas do projeto`

Cada commit deve deixar o programa rodando. Nunca faça commit de arquivos `__pycache__`.

⚠️ **Remoto:** se o repositório ainda não tiver remoto no GitHub, trabalhe só localmente e me diga no fim os comandos para eu conectar. **Pergunte antes de qualquer `git push`.** O repositório deve ser privado, porque os professores serão adicionados depois.

## Documentação

### README.md (raiz)
Comece com a **Ficha da CitizenTech** em tabela:

| Campo | Conteúdo |
|---|---|
| Nome da CitizenTech | Volta Segura |
| Cidade e bairro | São Paulo — Tatuapé, Belém e Mooca (entorno das estações da Linha 3) |
| Cidadão beneficiado | Quem volta a pé da estação à noite: estudantes, mães, trabalhadores do turno noturno |
| Problema, em uma frase | Quem desce do metrô à noite caminha por ruas com postes apagados e calçadas ruins, sem saber qual caminho é mais seguro |
| Como funciona | Sensor no poste detecta lâmpada apagada e presença de pedestre; dados vão para um painel; app mostra a rota mais iluminada e recebe denúncias dos moradores |
| O que cada parte faz | Python: cadastra trechos e calcula a nota de segurança e a rota. Edge: poste inteligente no ESP32. DPS: modelo matemático de luz e energia. Front-end/Web: app React com rota e denúncias. TX Design: jornada e requisitos. Storytelling: pitch e marca |
| Link do repositório | (preencher) |
| Indicador de impacto | % de trechos iluminados na rota; tempo médio até o conserto de um poste; kWh economizados por poste |
| ODS conectados | 11, 9 e 10 |

Depois: uma descrição curta de cada pasta e um espaço "Integrantes" com nome e RM em branco para o grupo preencher.

### python/readme.md (entregável)
Projeto, problema, como executar (`python main.py` dentro de `python/`, Python 3.10+), funcionalidades do menu, regras de negócio explicadas, estrutura dos arquivos, formato dos JSON, origem dos dados (simulados) e integrantes (nome e RM em branco).

### python/prompt.md (entregável — obrigatório)
Precisa ter exatamente estas seções:
1. **Ferramentas de IA utilizadas** e a finalidade de cada uma (Claude, para planejamento e definição do tema; Claude Code, para gerar e revisar o código)
2. **Prompts utilizados**: inclua este prompt inteiro e os pedidos de ajuste feitos depois
3. **Funcionalidades desenvolvidas, sugeridas ou modificadas com IA**
4. **Como o grupo verificou, testou e ajustou** (deixe um roteiro de testes manuais em tabela: entrada → resultado esperado → resultado obtido, com a última coluna em branco para o grupo preencher)
5. **Análise crítica**: benefícios, limitações e dificuldades (um rascunho honesto que o grupo vai revisar)

### python/docs/guia_de_estudo.md (para o grupo; não vai no ZIP)
Para cada arquivo `.py`: o que ele faz, cada função em uma frase, e as linhas mais "perguntáveis" pelo professor explicadas (por que `try/except` aqui, por que tupla e não lista, por que nota mínima e não média). Termine com **10 perguntas prováveis do professor, com as respostas**.

## Testes e verificação

Antes de cada merge, rode o programa com entradas simuladas (por exemplo, `printf "1\n2\n0\n0\n" | python main.py`) e confira que:
- nenhuma entrada inválida quebra o programa (letra onde se espera número, id inexistente, opção 9, texto vazio);
- os JSON são gravados e relidos corretamente;
- a faixa volta como tupla depois de carregar;
- a rota mais segura escolhe pela nota mínima.

Não deixe arquivos de teste automatizado na entrega. Se criar algum script de teste, apague antes do merge final.

## Entrega final

No fim:
1. Gere `entrega/volta_segura_python.zip` contendo **só**: os arquivos `.py`, a pasta `data/` com os JSON, `readme.md` e `prompt.md`. Sem `docs/`, sem `__pycache__`. Coloque a pasta `entrega/` no `.gitignore`.
2. Me mostre um resumo: árvore final de arquivos, lista de branches, `git log --oneline --graph` e o checklist de requisitos da tabela lá de cima, marcando onde cada item aparece (arquivo e função).

## Como trabalhar comigo

- Antes de escrever código, me mostre o plano em poucas linhas e espere meu "ok".
- Depois vá feature por feature, me avisando ao concluir cada uma.
- Se algo nesta especificação estiver ambíguo, pergunte em vez de inventar.

</details>

### 2.5 Pedidos de ajuste ao Claude Code

(Preencher com os prompts usados na revisão: o que foi pedido e o que mudou.)

| Data | Prompt | O que mudou no código |
|---|---|---|
| | | |
| | | |

## 3. Funcionalidades desenvolvidas, sugeridas ou modificadas com IA

| Funcionalidade | Papel da IA | Papel do grupo |
|---|---|---|
| Estrutura em arquivos separados (`dados`, `validacoes`, `trechos`...) | Sugeriu e gerou | Aprovou a divisão |
| CRUD de trechos, ocorrências e rotas | Gerou o código | Testou os fluxos |
| Nota de segurança (iluminação + calçada − ocorrências) | Sugeriu os pesos | Definiu o tema e validou se os pesos fazem sentido |
| Rota mais segura pela nota mínima ("elo mais fraco") | Sugeriu o critério | Validou com o exemplo dos dados simulados |
| Simulação do poste com os mesmos estados do ESP32 | Sugeriu a integração com o Edge | Combinou os limites com quem faz o Edge |
| Registro automático de ocorrência quando o poste falha | Sugeriu | Aprovou |
| Relatório por bairro e indicador de impacto | Gerou | Ligou o indicador à Ficha da CitizenTech |
| Dados simulados das ruas do Tatuapé, Belém e Mooca | Gerou | Conferiu que não há dados pessoais |
| `readme.md` e este `prompt.md` | Gerou o rascunho | Revisou e completou |

## 4. Como o grupo verificou, testou e ajustou

1. Executamos cada opção do menu com os dados simulados.
2. Testamos entradas erradas de propósito para garantir que o programa não quebra.
3. Conferimos as notas calculando à mão alguns trechos (exemplo: Rua Itapura → 3 de 8 postes acesos = 2,25 + calçada ruim 0,5 − 1 ocorrência 0,5 = 2,25 ≈ 2,2).
4. Apagamos e corrompemos os arquivos JSON para ver se o programa se recupera.
5. Pedimos ao Claude Code uma revisão do código e dos requisitos e avaliamos cada sugestão antes de aceitar.

### Roteiro de testes manuais

| # | Entrada | Resultado esperado | Resultado obtido |
|---|---|---|---|
| 1 | No menu principal, digitar `abc` | Mensagem de erro e a pergunta se repete | |
| 2 | No menu principal, digitar `9` | "O valor máximo é 6" | |
| 3 | Cadastrar trecho com número final menor que o inicial | Erro e nova pergunta | |
| 4 | Cadastrar 5 postes e 7 apagados | "O valor máximo é 5" | |
| 5 | Deixar o nome da rua vazio | "Este campo não pode ficar vazio" | |
| 6 | Remover o trecho 2 (tem ocorrência) | Remoção bloqueada com explicação | |
| 7 | Editar um id que não existe (ex.: 99) | "Não existe registro com id 99" | |
| 8 | Nota do trecho 2 | 2.2 VERMELHO, com o cálculo detalhado | |
| 9 | Rota mais segura Tatuapé → Casa A | Recomenda a rota 2 (mínima 5,5), mesmo com média menor | |
| 10 | Rota mais segura Belém → Escola | Recomenda a rota 4 | |
| 11 | Simular poste: dia | DESLIGADO (DIA) | |
| 12 | Simular poste: noite, leitura `abc` | LEITURA INVÁLIDA | |
| 13 | Simular poste: noite, leitura 2000 | LEITURA INVÁLIDA | |
| 14 | Simular poste: noite, leitura 600, com pedestre | PEDESTRE, luz 100% | |
| 15 | Simular poste: noite, leitura 600, sem pedestre | ECONOMIA, luz 30% | |
| 16 | Simular poste: noite, leitura 100, registrar no trecho 2 | APAGADO / FALHA, nova ocorrência e nota do trecho cai | |
| 17 | Atualizar uma ocorrência para "resolvida" e ver a nota | A nota do trecho sobe 0,5 | |
| 18 | Apagar `data/rotas.json` e abrir o programa | Aviso e arquivo recriado vazio | |
| 19 | Fechar o programa e abrir de novo | Os dados cadastrados continuam lá (JSON) | |
| 20 | Apertar Ctrl+C no meio do programa | "Programa encerrado" sem mensagem de erro | |

## 5. Análise crítica

(Rascunho para o grupo revisar e reescrever com a própria experiência.)

**Benefícios.** A IA acelerou a parte de transformar a ideia em uma especificação organizada: a tabela de requisitos da disciplina virou um checklist que guiou o código inteiro. Ela também sugeriu ideias que melhoraram o projeto, como escolher a rota pela nota mínima e repetir no Python a lógica do poste do ESP32, conectando as disciplinas.

**Limitações.** A IA não conhece as ruas de verdade: os números de postes e as condições das calçadas são inventados e precisam ser substituídos por dados das nossas observações e entrevistas. Os pesos da nota (6 para iluminação, 2,5 para calçada) são uma proposta razoável, não um estudo. Ela também não sabe exatamente o que foi visto em aula, então precisamos conferir se cada recurso usado foi ensinado.

**Dificuldades.** O código gerado funciona, mas entender cada linha levou tempo, e o professor pode perguntar sobre qualquer parte. Para isso, estudamos o guia de cada arquivo e testamos tudo à mão. Também tivemos que tomar cuidado para não aceitar sugestões sem entender o motivo.

**Conclusão.** A IA funcionou como um copiloto: ajudou a planejar, gerar e revisar, mas as decisões sobre o problema, o cidadão e as regras foram do grupo, e a responsabilidade pelo código entregue também.
