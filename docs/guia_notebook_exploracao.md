# Guia: como montar o notebook de exploração

Passo a passo para escrever o `notebooks/01_exploracao_dados.ipynb` do zero,
no Antigravity, usando Plotly nos gráficos.

## 1. Preparar o ambiente

1. Abra o `notebooks/01_exploracao_dados.ipynb`.
2. No canto superior direito, clique em **Select Kernel** → **Python Environments**
   e escolha a **`.venv`** do projeto.
3. Se o kernel já estava aberto antes de instalar uma biblioteca nova, reinicie
   o kernel (ícone ⟳ no topo do notebook).
4. Crie células com **+ Code** (código) ou **+ Markdown** (texto) e rode cada uma
   com **Shift+Enter**.

## 2. Roteiro das seções

| Seção | O que fazer | Ferramentas |
|---|---|---|
| 1. Carga dos dados | Importar e carregar o CSV pelo pacote, olhar as primeiras linhas | `load_raw()`, `df.head()` |
| 2. Qualidade dos dados | Tipos, valores ausentes e duplicatas, e anotar a decisão sobre os ausentes | `df.info()`, `df.isna().sum()`, `df.duplicated()` |
| 3. Visão geral | Estatísticas, contagem das categorias e distribuição das numéricas | `df.describe()`, `value_counts()`, `px.histogram` |
| 4. Pergunta 1 | Horas de uso × sono, estresse, saúde mental e GPA | `df.corr(method="spearman")`, `px.imshow` |
| 5. Pergunta 2 | Uso de madrugada × sono | `groupby(...).mean()`, `px.box` |
| 6. Pergunta 3 | Comparação social × saúde mental (ordem Nunca → Sempre) | `px.box` |
| 7. Pergunta 4 | % de impacto *Negativo* por plataforma | `value_counts(normalize=True)`, `px.bar` |
| 8. Conclusões | Escrever o que cada gráfico respondeu | célula Markdown |

Sempre carregue os dados com `load_raw()` (de `social_media_impact.data`), e
não com `pd.read_csv`. Assim os tipos e as checagens ficam iguais no notebook,
nos testes e no dashboard, e os dados já chegam em português: colunas
em `snake_case` (ex.: `horas_uso_diario`) e valores traduzidos (ex.: *Benéfico*).
As categorias com ordem natural (nível acadêmico, comparação social e impacto)
já vêm ordenadas, então os gráficos saem na sequência certa sem `category_orders`.

## 3. Achados já conhecidos do dataset

- 4.500 linhas e 16 colunas, sem linhas nem `id_estudante` duplicados.
- Valores ausentes: `estresse_percebido` (46) e `media_academica` (85),
  menos de 2% das linhas. Sugestão: descartá-los só na análise que usa a coluna
  (`dropna` local).
- `impacto_geral` é desbalanceado: 3.681 *Benéfico*, 654 *Neutro* e só
  165 *Negativo* (~3,7%). Na pergunta 4, compare **porcentagens** dentro de cada
  plataforma, não contagens.

## 4. Dicas de trabalho

- **Uma seção de cada vez:** rode, olhe o resultado e só depois siga.
- **Anote o que vê** numa célula Markdown logo após cada resultado. Esses
  achados viram as conclusões no final.
- **Erro não se apaga:** copie a mensagem e investigue (ou peça ajuda).
  Entender o erro ensina muito.
- **O roteiro é ponto de partida:** se quiser incluir outro gráfico ou outra
  pergunta, inclua.

## 5. Gráficos: Plotly no lugar de seaborn/matplotlib

| seaborn / matplotlib | Plotly Express |
|---|---|
| `sns.boxplot` | `px.box` |
| `sns.heatmap` | `px.imshow` |
| `df.hist` | `px.histogram` |
| `sns.barplot` | `px.bar` |

O gráfico criado com Plotly no notebook pode ir direto para o dashboard em Dash,
sem ser refeito.

## 6. Depois da exploração

- Os resumos que valerem a pena guardar (ex.: tabela da pergunta 4) vão para
  `src/social_media_impact/data.py`, com uma função `save_processed()` que grava
  em `data/processed/`.
- Os gráficos do dashboard vão para um `visualization.py`.
- Um `pipeline.py` roda tudo de ponta a ponta (`python -m social_media_impact.pipeline`),
  como no projeto DataFruit.
