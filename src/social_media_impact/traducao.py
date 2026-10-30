# =============================================================================
# Tradução dos dados para português
# -----------------------------------------------------------------------------
# O CSV original continua em inglês (dado bruto não se edita). Aqui ficam só
# as tabelas de tradução e a função que as aplica; o load_raw() chama
# translate() logo depois de ler o arquivo.
# =============================================================================
import pandas as pd

# Colunas do CSV original (em inglês) e o nome que cada uma ganha no projeto.
# A ordem é a do arquivo; as chaves servem para conferir se o CSV mudou.
COLUMN_NAMES = {
    "Student_ID": "id_estudante",
    "Age": "idade",
    "Gender": "genero",
    "Academic_Level": "nivel_academico",
    "Primary_Platform": "plataforma_principal",
    "Daily_Usage_Hours": "horas_uso_diario",
    "Weekend_Extra_Hours": "horas_extras_fim_de_semana",
    "Device_Type": "tipo_dispositivo",
    "Sleep_Duration_Hours": "horas_sono",
    "Sleep_Quality_Score": "qualidade_sono",
    "Late_Night_Usage": "uso_madrugada",
    "Social_Comparison_Frequency": "frequencia_comparacao_social",
    "Perceived_Stress_Score": "estresse_percebido",
    "Mental_Health_Index": "indice_saude_mental",
    "Academic_Performance_GPA": "media_academica",
    "Overall_Impact": "impacto_geral",
}

# Tradução dos valores das colunas de texto. Os nomes das plataformas
# (Instagram, TikTok...) ficam como estão, porque são marcas.
# Nas colunas com ordem natural, a ordem dos itens é a ordem usada nos gráficos.
VALUE_TRANSLATIONS = {
    "genero": {
        "Female": "Feminino",
        "Male": "Masculino",
        "Non-Binary": "Não binário",
        "Prefer not to say": "Prefere não dizer",
    },
    "nivel_academico": {
        "High School": "Ensino médio",
        "Undergraduate": "Graduação",
        "Postgraduate": "Pós-graduação",
    },
    "tipo_dispositivo": {
        "Smartphone": "Celular",
        "Tablet": "Tablet",
        "Laptop/PC": "Notebook/PC",
    },
    "frequencia_comparacao_social": {
        "Never": "Nunca",
        "Rarely": "Raramente",
        "Sometimes": "Às vezes",
        "Frequently": "Frequentemente",
        "Always": "Sempre",
    },
    "impacto_geral": {
        "Negative": "Negativo",
        "Neutral": "Neutro",
        "Beneficial": "Benéfico",
    },
}


def translate(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia as colunas e traduz os valores de texto para português."""
    df = df.rename(columns=COLUMN_NAMES)

    # Valor que não estiver no dicionário vira NaN e a checagem abaixo avisa,
    # em vez de um texto em inglês passar despercebido no meio dos dados
    for coluna, traducao in VALUE_TRANSLATIONS.items():
        traduzida = df[coluna].map(traducao)
        nao_traduzidos = df.loc[traduzida.isna() & df[coluna].notna(), coluna].unique()
        if len(nao_traduzidos):
            raise ValueError(f"Valores sem tradução em {coluna}: {list(nao_traduzidos)}")
        df[coluna] = traduzida

    return df
