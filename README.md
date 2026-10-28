# Social Media Impact

Análise do impacto das redes sociais na vida de estudantes: uso diário, sono, estresse, saúde mental e desempenho acadêmico (GPA).

## Dados

`data/raw/Social_media_impact_on_life.csv` — 4.500 estudantes, 16 colunas:

| Coluna | Descrição |
|---|---|
| Student_ID | Identificador do estudante |
| Age, Gender, Academic_Level | Perfil |
| Primary_Platform, Device_Type | Plataforma e aparelho mais usados |
| Daily_Usage_Hours, Weekend_Extra_Hours | Horas de uso |
| Sleep_Duration_Hours, Sleep_Quality_Score | Sono |
| Late_Night_Usage | Usa de madrugada (True/False) |
| Social_Comparison_Frequency | Frequência de comparação social |
| Perceived_Stress_Score, Mental_Health_Index | Bem-estar |
| Academic_Performance_GPA | Desempenho acadêmico |
| Overall_Impact | Impacto geral (Beneficial / Neutral / ...) |

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

## Como rodar os testes

```bash
pytest
```
