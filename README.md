# LoL Analytics — Avaliação de Desempenho com Sistemas Nebulosos

Sistema que avalia o desempenho de um jogador de **League of Legends** usando **lógica fuzzy**. O desempenho dele é comparado com o de jogadores **Challenger** que jogaram na mesma rota e com a mesma classe de campeão.

O projeto tem duas partes independentes:

1. **Extração de dados** (`src/dataExtraction/`): uma CLI em Python que consulta a API oficial da Riot Games e gera datasets em CSV.
2. **Sistema nebuloso** (`src/LoLAnalytics.ipynb`): um notebook (desenvolvido no Google Colab) que monta automaticamente os conjuntos fuzzy e as regras a partir dos dados Challenger. Depois, ele dá uma nota de 0 a 1 a cada partida do jogador analisado.

> Trabalho acadêmico da disciplina de **Sistemas Nebulosos**. A apresentação e o resumo estruturado estão na raiz do repositório (`SISTEMAS NEBULOSOS - Apresentação.pdf` e `SISTEMAS NEBULOSOS - Resumo Estruturado.pdf`).

---

## Visão geral do fluxo

```
 API da Riot Games
        │
        ▼
┌───────────────────────────┐     dados_challenger.csv  (base de referência)
│  src/dataExtraction/      │ ──▶
│  main.py  (CLI)           │     dados_jogador.csv     (jogador a ser avaliado)
└───────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  src/LoLAnalytics.ipynb                                     │
│  1. Variável de saída "desempenho do jogador" (6 termos)    │
│  2. Fuzzy C-Means → funções de pertinência por grupo        │
│  3. Wang-Mendel adaptado → geração automática de regras     │
│  4. Um sistema de inferência por (lane × classe)            │
│  5. Inferência + defuzzificação nas partidas do jogador     │
│  6. Tabela final com a nota de desempenho (PNG)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Estrutura do repositório

```
LoLAnalytics/
├── SISTEMAS NEBULOSOS - Apresentação.pdf
├── SISTEMAS NEBULOSOS - Resumo Estruturado.pdf
└── src/
    ├── LoLAnalytics.ipynb          # Sistema nebuloso (Colab)
    ├── readMe.txt                  # Link para o notebook original no Colab
    └── dataExtraction/
        ├── main.py                 # Menu interativo (ponto de entrada)
        ├── analytics.py            # Chamadas à API da Riot, extração e filtragem
        ├── config.py               # Carrega/salva a chave da API
        ├── config.example.json     # Modelo do config.json (o real fica fora do Git)
        ├── requirements.txt
        ├── dados_challenger.csv    # ~400 partidas de jogadores Challenger (BR)
        └── dados_jogador.csv       # 5 partidas do jogador avaliado
```

---

## 1. Extração de dados

### Requisitos

- Python 3.9+
- Uma chave de desenvolvedor da Riot Games ([developer.riotgames.com](https://developer.riotgames.com/)). Ela começa com `RGAPI-` e **expira a cada 24h**.

```bash
cd src/dataExtraction
pip install -r requirements.txt
```

### Uso

Execute **de dentro de `src/dataExtraction/`**, porque o `config.json` e os CSVs são lidos e gravados no diretório atual:

```bash
python main.py
```

```
=== Menu Principal ===
1. Coletar dados da liga Challenger
2. Coletar dados de um jogador específico
3. Sair
4. Atualizar chave da API
```

| Opção | O que faz | Saída |
|---|---|---|
| **1** | Pega jogadores aleatórios da liga Challenger (BR1) e coleta até 3 partidas ranqueadas de cada um, até juntar 100 partidas válidas | `dados_challenger.csv` |
| **2** | Busca um jogador pelo Riot ID (`nome` + `tag` + região) e coleta as últimas 5 partidas ranqueadas válidas | `dados_jogador.csv` |
| **4** | Valida a nova chave contra a API e grava em `config.json` | — |

Na primeira execução, use a opção **4** para configurar a chave. Outra opção é copiar `config.example.json` para `config.json` e colar a chave nele. O `config.json` está no `.gitignore` e **nunca deve ser commitado**.

### Dados coletados por partida

| Coluna | Descrição |
|---|---|
| `match_id` | ID da partida |
| `kills`, `deaths`, `assists` | Abates, mortes e assistências |
| `cs` | Tropas + monstros neutros abatidos |
| `objective_participation` | `(kills + assists) / kills do time` (participação em abates) |
| `visionScore` | Placar de visão |
| `goldEarned` | Ouro obtido |
| `damageDealtToChampions` | Dano causado a campeões |
| `lane` | `TOP`, `JUNGLE`, `MIDDLE`, `BOTTOM`, `UTILITY` |
| `champion_class` | Mago, Assassino, Lutador, Atirador, Suporte, Tanque, Healer |
| `champion_name` | Nome do campeão |

A classe de cada campeão vem de um dicionário manual (`CHAMPION_CLASSES` em `analytics.py`). São **descartadas** as partidas com campeão sem classe mapeada ou com rota vazia/inválida.

As chamadas tratam o rate limit: num `429`, o código espera o `Retry-After` e tenta de novo. Além disso, há pausas fixas entre as requisições.

---

## 2. Sistema nebuloso

Use o notebook [`src/LoLAnalytics.ipynb`](src/LoLAnalytics.ipynb) ou a [versão original no Colab](https://colab.research.google.com/drive/1SHdkAcgUy6-JjllPO4vsrlF9CQbD0kJ9?usp=sharing). Ele depende de `scikit-fuzzy`, `pandas`, `numpy` e `matplotlib`.

Para rodar, coloque `dados_challenger.csv` e `dados_jogador.csv` na mesma pasta do notebook (no Colab, faça upload na sessão) e execute as células na ordem.

### Etapas

**1. Variável de saída: desempenho do jogador** (universo `[0, 1]`)

| Termo | Significado | Função |
|---|---|---|
| `MR` | Muito Ruim | trapezoidal `[0, 0, 0.1, 0.3]` |
| `R` | Ruim | triangular `[0.05, 0.2, 0.4]` |
| `M` | Médio | triangular `[0.3, 0.5, 0.7]` |
| `B` | Bom | triangular `[0.6, 0.7, 0.8]` |
| `MB` | Muito Bom | triangular `[0.7, 0.8, 0.9]` |
| `P` | Perfeito | trapezoidal `[0.8, 0.9, 1, 1]` |

**2. Variáveis de entrada via Fuzzy C-Means**

Os dados Challenger são agrupados por **(lane, classe do campeão)**. Em cada grupo, cada uma das 8 métricas é normalizada para `[0, 1]` e passa por um **Fuzzy C-Means** com 3 clusters. Os centros, ordenados, definem os termos `baixo` (trapezoidal), `médio` (triangular) e `alto` (trapezoidal). Assim, o que conta como "muitos abates" num Atirador bot é diferente do que conta num Suporte.

**3. Geração automática de regras (Wang-Mendel adaptado)**

Para cada partida do grupo:
- escolhe, para cada métrica, o termo de maior pertinência;
- calcula um desempenho de referência: a média das métricas normalizadas;
- junta as amostras que têm a mesma combinação de termos e mapeia a média para o termo de saída de maior pertinência.

Cada combinação única vira uma regra do tipo `SE kills é alto E deaths é baixo E … ENTÃO desempenho é B`.

**4. Sistemas de inferência**

É criado um `ControlSystem` (Mamdani, scikit-fuzzy) para cada grupo lane × classe.

**5. Avaliação do jogador**

As partidas de `dados_jogador.csv` são normalizadas e passam pelo sistema do grupo correspondente. A saída é defuzzificada por **centroide**. O resultado é uma nota de 0 a 1 por partida, mais a média geral.

**6. Resultado**

O notebook gera `tabela_desempenho_jogador.png` com as métricas de cada partida e a coluna `Desempenho`.

---

## Limitações conhecidas

- **Região fixa**: a coleta Challenger usa `br1` / `americas` (constantes `REGION` e `MATCH_REGION` em `analytics.py`).
- **Um grupo por avaliação**: o notebook escolhe o sistema fuzzy pela lane e classe da *primeira* partida do jogador e usa esse mesmo sistema em todas as partidas.
- **Normalização do jogador**: na etapa 5, os `min`/`max` usados vêm da variável `stats` da última iteração da etapa 3, não necessariamente do grupo do jogador.
- **Cobertura de regras**: com cerca de 400 amostras divididas em cerca de 35 grupos e 8 entradas, muitas combinações não têm regra. Quando nenhuma regra dispara, a partida recebe desempenho `0`.
- **Classes manuais**: campeões fora do dicionário `CHAMPION_CLASSES` são ignorados. Soraka e Sona aparecem em duas classes; vale a última definição (`Healer`).
- **Mudanças na API da Riot**: a coleta Challenger usa `summonerId` → `summoner/v4` → `puuid`. Se a Riot remover ou alterar esses campos/endpoints, adapte para usar o `puuid` que já vem nas entradas da liga.

---

## Tecnologias

Python · Requests · Pandas · NumPy · scikit-fuzzy · Matplotlib · Riot Games API · Google Colab

---

*League of Legends e Riot Games são marcas registradas da Riot Games, Inc. Este projeto não é endossado pela Riot Games.*
