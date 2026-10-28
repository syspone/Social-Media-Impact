import pandas as pd
import pytest

from social_media_impact.data import CATEGORICAL_COLUMNS, EXPECTED_COLUMNS, load_raw


def test_load_raw_tem_todas_as_colunas():
    df = load_raw()
    assert list(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 4500


def test_load_raw_ajusta_os_tipos():
    df = load_raw()
    for coluna in CATEGORICAL_COLUMNS:
        assert isinstance(df[coluna].dtype, pd.CategoricalDtype)
    assert df["Late_Night_Usage"].dtype == bool


def test_load_raw_avisa_coluna_ausente(tmp_path):
    # CSV de exemplo sem a coluna Overall_Impact
    csv = tmp_path / "incompleto.csv"
    pd.DataFrame(columns=EXPECTED_COLUMNS[:-1]).to_csv(csv, index=False)

    with pytest.raises(ValueError, match="Overall_Impact"):
        load_raw(csv)
