# =============================================================================
# Configuração compartilhada dos testes (pytest lê este arquivo sozinho)
# -----------------------------------------------------------------------------
# O CSV original fica fora do git. Testes marcados com @pytest.mark.requer_dados
# são pulados quando o arquivo não existe (ex.: na CI do GitHub), em vez de falhar.
# =============================================================================
import pytest

from social_media_impact.config import RAW_DATA_FILE


def pytest_collection_modifyitems(config, items):
    if RAW_DATA_FILE.exists():
        return
    pular = pytest.mark.skip(reason=f"CSV não encontrado em {RAW_DATA_FILE}")
    for item in items:
        if "requer_dados" in item.keywords:
            item.add_marker(pular)
