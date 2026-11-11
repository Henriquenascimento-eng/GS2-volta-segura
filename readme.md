# Volta Segura — Aplicação Python

**Disciplina:** Computational Thinking with Python — Global Solution 2026.2 (desafio CitizenTech)
**Curso:** Engenharia de Software, 1º ano — FIAP

## Integrantes

| Nome | RM |
|---|---|
| Andrey luigi | rm569575 |
| Nicolas Moreira | rm571510 |
| Lucas Trevisan | rm569731 |
| Gabriel Juarez | rm563680 |
| Henrique da Silva | rm569137 |

## O problema

Quem desce do metrô à noite nas estações Tatuapé, Belém e Bresser-Mooca (Linha 3-Vermelha, São Paulo) precisa caminhar até em casa por ruas com postes apagados e calçadas ruins, sem saber qual caminho é mais seguro.

## A solução

A **Volta Segura** é uma CitizenTech formada por um poste inteligente (ESP32), um app web e este programa em Python, que é o "cérebro" do sistema. Ele:

- cadastra os **trechos de rua** entre as estações e os destinos, com os postes e a condição da calçada;
- registra **ocorrências** reportadas pelos moradores (poste apagado, calçada quebrada, rua escura);
- calcula uma **nota de segurança** de 0 a 10 para cada trecho;
- recomenda a **rota mais segura** da estação até o destino;
- **simula o poste inteligente** com a mesma lógica do ESP32 e registra sozinho um poste apagado;
- gera um **relatório por bairro** com o indicador de impacto do projeto.

## Como executar

Requisito: **Python 3.10 ou mais recente** (por causa do `match/case`). Nenhuma biblioteca externa é necessária.

```bash
cd python
python main.py
```

No Linux ou Mac, pode ser necessário usar `python3 main.py`.

## Funcionalidades do menu

| Opção | O que faz |
|---|---|
| 1. Trechos de rua | Cadastrar, listar, editar e remover trechos |
| 2. Ocorrências | Registrar, listar, atualizar o status e remover ocorrências |
| 3. Simular poste inteligente | Informa se é noite, a leitura do sensor de luz e se há pedestre; mostra o estado do poste |
| 4. Nota de segurança | Mostra a nota de todos os trechos e o cálculo detalhado de um deles |
| 5. Rotas | Descobrir a rota mais segura, cadastrar, listar e remover rotas |
| 6. Relatório geral | Situação por bairro, ocorrências ativas e indicador de impacto |
| 0. Sair | Encerra o programa |

## Regras de negócio

### Nota de segurança do trecho (0 a 10)

| Parte | Cálculo | Máximo |
|---|---|---|
| Iluminação | (postes acesos ÷ postes no total) × 6 | +6,0 |
| Calçada | boa = 2,5 · regular = 1,5 · ruim = 0,5 | +2,5 |
| Ocorrências ativas | −0,5 por ocorrência aberta ou em análise | −1,5 |

A iluminação tem o maior peso porque é o principal fator de segurança para quem anda à noite.

| Nota | Classificação |
|---|---|
| 7 ou mais | VERDE (seguro) |
| de 4 a 6,9 | AMARELO (atenção) |
| abaixo de 4 | VERMELHO (evitar) |

### Rota mais segura: o elo mais fraco

Entre as rotas que ligam a mesma estação ao mesmo destino, vence a que tem a **maior nota mínima**, não a maior média. Um único trecho escuro já torna o caminho inseguro. Em caso de empate, vence a maior média.

Exemplo com os dados de demonstração (Tatuapé → Casa A):

| Rota | Notas dos trechos | Média | Mínima |
|---|---|---|---|
| 1 | 7,9 · **2,2** · 8,5 | 6,2 | 2,2 |
| 2 | 5,5 · 6,3 | 5,9 | **5,5** |

A rota 1 tem a média maior, mas passa por um trecho vermelho. O sistema recomenda a **rota 2**.

### Poste inteligente

Os limites são os mesmos usados no ESP32 (pasta `edge/`).

| Condição | Estado | Luz |
|---|---|---|
| Leitura do LDR fora de 0 a 1023 ou não numérica | LEITURA INVÁLIDA | 0% |
| Dia | DESLIGADO (DIA) | 0% |
| Noite e leitura abaixo de 200 | APAGADO / FALHA (gera alerta) | 0% |
| Noite, lâmpada funcionando, com pedestre | PEDESTRE | 100% |
| Noite, lâmpada funcionando, rua vazia | ECONOMIA | 30% |

No estado APAGADO / FALHA, o programa oferece registrar a ocorrência automaticamente, e o poste passa a contar como apagado no trecho, o que baixa a nota.

### Outras regras

- Um trecho com ocorrências ou que faz parte de uma rota **não pode ser removido**.
- Os postes apagados nunca podem ser mais que o total de postes.
- O número inicial do trecho precisa ser menor que o número final.
- Ids nunca são reaproveitados: o próximo id é sempre o maior existente + 1.
- Toda remoção pede confirmação.

## Estrutura dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada: menu principal, telas do poste e da nota |
| `dados.py` | Leitura e gravação dos arquivos JSON |
| `validacoes.py` | Leitura das entradas do usuário com validação |
| `interface.py` | Títulos, mensagens, pausas e tabelas no terminal |
| `trechos.py` | CRUD de trechos de rua |
| `ocorrencias.py` | CRUD de ocorrências |
| `rotas.py` | Telas de rotas e da rota mais segura |
| `seguranca.py` | Regras de negócio: nota, rota e estado do poste (só cálculos) |
| `relatorio.py` | Relatório geral por bairro |
| `data/*.json` | Dados salvos do sistema |

## Formato dos dados (JSON)

**trechos.json**
```json
{ "id": 1, "bairro": "Tatuapé", "rua": "Rua Tuiuti", "faixa": [100, 400],
  "postes_total": 10, "postes_apagados": 1, "calcada": "boa" }
```
A `faixa` é salva como lista, porque o JSON não tem tupla, e convertida para tupla `(100, 400)` ao carregar.

**ocorrencias.json**
```json
{ "id": 1, "trecho_id": 2, "tipo": "poste_apagado",
  "descricao": "Três postes apagados perto do número 150", "status": "aberta" }
```

**rotas.json**
```json
{ "id": 1, "estacao": "Tatuapé", "destino": "Casa A", "trechos": [1, 2, 3] }
```

## Origem dos dados

Todos os dados em `data/` são **simulados**, criados pelo grupo para a demonstração. Os nomes das ruas existem, mas a quantidade de postes, os postes apagados, as calçadas e as ocorrências são fictícios. O sistema **não coleta nenhum dado pessoal**: as ocorrências não guardam nome, telefone nem endereço de quem reporta.

Se algum arquivo JSON for apagado, o programa cria um novo vazio ao iniciar.

## ODS conectados

- **ODS 11** — Cidades e comunidades sustentáveis: espaços públicos mais seguros e acessíveis.
- **ODS 9** — Indústria, inovação e infraestrutura: manutenção mais rápida da iluminação pública.
- **ODS 10** — Redução das desigualdades: mostra quais bairros têm a pior infraestrutura.

## Uso de IA

Veja o arquivo `prompt.md`.
