# =============================================================================
# Carga dos dados
# -----------------------------------------------------------------------------
# Único ponto do projeto que lê o CSV. Notebook, testes e dashboard chamam
# load_raw() em vez de usar pd.read_csv direto, então os tipos e as checagens
# ficam iguais em todo lugar.
# =============================================================================
import pandas as pd

from social_media_impact.config import RAW_DATA_FILE

# Colunas que o resto do projeto espera encontrar no CSV, na ordem do arquivo
EXPECTED_COLUMNS = [
    "Student_ID",
    "Age",
    "Gender",
    "Academic_Level",
    "Primary_Platform",
    "Daily_Usage_Hours",
    "Weekend_Extra_Hours",
    "Device_Type",
    "Sleep_Duration_Hours",
    "Sleep_Quality_Score",
    "Late_Night_Usage",
    "Social_Comparison_Frequency",
    "Perceived_Stress_Score",
    "Mental_Health_Index",
    "Academic_Performance_GPA",
    "Overall_Impact",
]

# Colunas de texto com poucos valores possíveis viram "category", que ocupa
# menos memória e deixa os gráficos e o groupby mais rápidos
CATEGORICAL_COLUMNS = [
    "Gender",
    "Academic_Level",
    "Primary_Platform",
    "Device_Type",
    "Social_Comparison_Frequency",
    "Overall_Impact",
]


def load_raw(path=RAW_DATA_FILE) -> pd.DataFrame:
    """Lê o CSV original e devolve um DataFrame com os tipos certos.

    O parâmetro `path` existe para os testes poderem passar um CSV pequeno
    de exemplo; no uso normal ele vem do .env, via config.py.
    """
    df = pd.read_csv(path)

    # Falha logo se o arquivo mudou de formato, em vez de quebrar lá na frente
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(missing)}")

    # Late_Night_Usage já chega como bool (True/False no CSV), então não precisa
    # de conversão; um astype(bool) aqui transformaria valores vazios em True
    df[CATEGORICAL_COLUMNS] = df[CATEGORICAL_COLUMNS].astype("category")

    return df
