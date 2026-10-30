import pandas as pd
import pytest

from social_media_impact.data import (
    CATEGORICAL_COLUMNS,
    COLUMNS,
    EXPECTED_COLUMNS,
    load_raw,
)


def test_load_raw_tem_todas_as_colunas():
    df = load_raw()
    assert list(df.columns) == COLUMNS
    assert len(df) == 4500


def test_load_raw_ajusta_os_tipos():
    df = load_raw()
    for coluna in CATEGORICAL_COLUMNS:
        assert isinstance(df[coluna].dtype, pd.CategoricalDtype)
    assert df["uso_madrugada"].dtype == bool


def test_load_raw_traduz_os_valores():
    df = load_raw()
    assert set(df["impacto_geral"].cat.categories) == {"Negativo", "Neutro", "Benéfico"}
    # Categorias com ordem natural já vêm ordenadas para os gráficos
    assert df["frequencia_comparacao_social"].cat.categories.tolist() == [
        "Nunca",
        "Raramente",
        "Às vezes",
        "Frequentemente",
        "Sempre",
    ]
    assert df["frequencia_comparacao_social"].cat.ordered


def test_load_raw_avisa_valor_sem_traducao(tmp_path):
    # CSV de exemplo com um impacto que não está no dicionário de tradução
    linha = {coluna: [0] for coluna in EXPECTED_COLUMNS}
    linha.update(
        Gender=["Female"],
        Academic_Level=["Undergraduate"],
        Primary_Platform=["TikTok"],
        Device_Type=["Tablet"],
        Social_Comparison_Frequency=["Never"],
        Overall_Impact=["Harmful"],
    )
    csv = tmp_path / "valor_novo.csv"
    pd.DataFrame(linha).to_csv(csv, index=False)

    with pytest.raises(ValueError, match="Harmful"):
        load_raw(csv)


def test_load_raw_avisa_coluna_ausente(tmp_path):
    # CSV de exemplo sem a coluna Overall_Impact
    csv = tmp_path / "incompleto.csv"
    pd.DataFrame(columns=EXPECTED_COLUMNS[:-1]).to_csv(csv, index=False)

    with pytest.raises(ValueError, match="Overall_Impact"):
        load_raw(csv)
