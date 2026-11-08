# =============================================================================
# Configurações do projeto
# -----------------------------------------------------------------------------
# Centraliza os caminhos das pastas e as variáveis do .env, para que nenhum
# outro arquivo precise "adivinhar" onde estão os dados.
# =============================================================================
import os
from pathlib import Path

from dotenv import load_dotenv

# Raiz do projeto: sobe de src/social_media_impact/config.py até social-media-impact/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Lê o arquivo .env (se existir) e joga as variáveis no ambiente
load_dotenv(PROJECT_ROOT / ".env")

# Os caminhos do .env são relativos à raiz; o segundo valor do getenv é o
# padrão usado caso a variável não exista no .env
RAW_DATA_FILE = PROJECT_ROOT / os.getenv(
    "DATA_RAW_PATH", "data/raw/Social_media_impact_on_life.csv"
)  # dados originais, nunca editados
PROCESSED_DATA_DIR = PROJECT_ROOT / os.getenv("DATA_PROCESSED_DIR", "data/processed")
FIGURES_DIR = PROJECT_ROOT / os.getenv("REPORTS_DIR", "reports/figures")

# Painel em Dash (dashboard.py). DASH_DEBUG=true só em desenvolvimento: recarrega
# o app ao salvar e mostra os erros no navegador, o que não deve ir para produção
DASH_HOST = os.getenv("DASH_HOST", "127.0.0.1")
DASH_PORT = int(os.getenv("DASH_PORT", "8050"))
DASH_DEBUG = os.getenv("DASH_DEBUG", "false").lower() == "true"
