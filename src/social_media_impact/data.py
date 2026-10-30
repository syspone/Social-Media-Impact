# =============================================================================
# Carga dos dados
# -----------------------------------------------------------------------------
# Único ponto do projeto que lê o CSV. Notebook, testes e dashboard chamam
# load_raw() em vez de usar pd.read_csv direto, então os tipos e as checagens
# ficam iguais em todo lugar. A tradução para português fica em traducao.py.
# =============================================================================
import pandas as pd

from social_media_impact.config import RAW_DATA_FILE
from social_media_impact.traducao import COLUMN_NAMES, VALUE_TRANSLATIONS, translate

EXPECTED_COLUMNS = list(COLUMN_NAMES)  # nomes originais do CSV, para a checagem
COLUMNS = list(COLUMN_NAMES.values())  # nomes em português, usados no projeto

# Colunas de texto com poucos valores possíveis viram "category", que ocupa
# menos memória e deixa os gráficos e o groupby mais rápidos
CATEGORICAL_COLUMNS = [
    "genero",
    "nivel_academico",
    "plataforma_principal",
    "tipo_dispositivo",
    "frequencia_comparacao_social",
    "impacto_geral",
]

# Colunas com ordem natural viram categoria *ordenada*: os gráficos já saem
# na sequência certa (Nunca → Sempre) sem precisar de category_orders
ORDERED_COLUMNS = ["nivel_academico", "frequencia_comparacao_social", "impacto_geral"]


def load_raw(path=RAW_DATA_FILE) -> pd.DataFrame:
    """Lê o CSV original e devolve um DataFrame em português, com os tipos certos.

    O parâmetro `path` existe para os testes poderem passar um CSV pequeno
    de exemplo; no uso normal ele vem do .env, via config.py.
    """
    df = pd.read_csv(path)

    # Falha logo se o arquivo mudou de formato, em vez de quebrar lá na frente
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(missing)}")

    df = translate(df)

    # uso_madrugada já chega como bool (True/False no CSV), então não precisa
    # de conversão; um astype(bool) aqui transformaria valores vazios em True
    df[CATEGORICAL_COLUMNS] = df[CATEGORICAL_COLUMNS].astype("category")
    for coluna in ORDERED_COLUMNS:
        ordem = list(VALUE_TRANSLATIONS[coluna].values())
        df[coluna] = df[coluna].cat.set_categories(ordem, ordered=True)

    return df
