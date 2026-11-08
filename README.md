# Social Media Impact

Análise do impacto das redes sociais na vida de estudantes: uso diário, sono, estresse, saúde mental e desempenho acadêmico (GPA).

## Dados

`data/raw/Social_media_impact_on_life.csv` — 4.500 estudantes, 16 colunas.

O CSV original fica em inglês, como veio da fonte. A função `load_raw()`
(em `src/social_media_impact/data.py`) traduz os nomes das colunas e os valores,
com as tabelas de `src/social_media_impact/traducao.py`,
para português logo na leitura:

| Coluna no projeto | Coluna no CSV | Descrição |
|---|---|---|
| id_estudante | Student_ID | Identificador do estudante |
| idade, genero, nivel_academico | Age, Gender, Academic_Level | Perfil |
| plataforma_principal, tipo_dispositivo | Primary_Platform, Device_Type | Plataforma e aparelho mais usados |
| horas_uso_diario, horas_extras_fim_de_semana | Daily_Usage_Hours, Weekend_Extra_Hours | Horas de uso |
| horas_sono, qualidade_sono | Sleep_Duration_Hours, Sleep_Quality_Score | Sono |
| uso_madrugada | Late_Night_Usage | Usa de madrugada (True/False) |
| frequencia_comparacao_social | Social_Comparison_Frequency | Frequência de comparação social (Nunca → Sempre) |
| estresse_percebido, indice_saude_mental | Perceived_Stress_Score, Mental_Health_Index | Bem-estar |
| media_academica | Academic_Performance_GPA | Desempenho acadêmico (GPA) |
| impacto_geral | Overall_Impact | Impacto geral (Negativo / Neutro / Benéfico) |

## Estrutura

```
data/raw/            dados originais (fora do git)
data/processed/      dados tratados (fora do git)
notebooks/           exploração em Jupyter
src/social_media_impact/  código do projeto
tests/               testes (pytest)
reports/figures/     gráficos gerados
```

## Como instalar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .          # instala o pacote src/social_media_impact na .venv
cp .env.example .env
```

## Como abrir o painel (Dash)

```bash
python -m social_media_impact.dashboard
```

Depois abra http://127.0.0.1:8050 no navegador (Ctrl+C no terminal para parar).
Endereço, porta e modo de desenvolvimento ficam no `.env` (`DASH_HOST`,
`DASH_PORT`, `DASH_DEBUG`).

Os gráficos ficam em `src/social_media_impact/visualization.py` e são os mesmos
no notebook e no painel.

## Como rodar os testes

```bash
pytest
```
