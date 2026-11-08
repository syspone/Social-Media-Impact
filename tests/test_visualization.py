import pytest

from social_media_impact.data import load_raw
from social_media_impact.visualization import (
    ROTULOS,
    colunas_categoricas,
    colunas_numericas,
    contagem,
    grafico_barras,
    grafico_distribuicao,
    para_exibicao,
    resumo_numericas,
)


@pytest.fixture(scope="module")
def df():
    # Carrega o CSV uma vez só para todos os testes deste arquivo
    return load_raw()


def test_todas_as_colunas_dos_graficos_tem_rotulo(df):
    colunas = colunas_categoricas(df) + colunas_numericas(df)
    assert set(colunas) <= set(ROTULOS)


def test_para_exibicao_troca_bool_por_sim_nao_sem_mexer_no_original(df):
    exibicao = para_exibicao(df)
    assert set(exibicao["uso_madrugada"]) == {"Sim", "Não"}
    assert df["uso_madrugada"].dtype == bool


def test_contagem_soma_100_por_cento(df):
    tabela = contagem(df, "impacto_geral")
    assert tabela["qtd"].sum() == len(df)
    assert tabela["pct"].sum() == pytest.approx(100, abs=0.2)
    # Mantém a ordem natural da categoria
    assert tabela.index.tolist() == ["Negativo", "Neutro", "Benéfico"]


def test_resumo_numericas_em_portugues(df):
    resumo = resumo_numericas(df)
    assert "Média" in resumo.columns
    assert "Uso diário (horas)" in resumo.index


def test_graficos_usam_os_rotulos(df):
    barras = grafico_barras(para_exibicao(df), "uso_madrugada")
    assert barras.layout.title.text == "Estudantes por uso de madrugada"

    distribuicao = grafico_distribuicao(df, "horas_sono")
    assert distribuicao.layout.title.text == "Distribuição: Sono (horas)"
    assert distribuicao.layout.xaxis.title.text == "Sono (horas)"
