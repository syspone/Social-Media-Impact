# =============================================================================
# Painel em Dash
# -----------------------------------------------------------------------------
# Como rodar (na raiz do projeto, com a .venv ativa):
#     python -m social_media_impact.dashboard
# e abrir no navegador o endereço que aparece no terminal (padrão:
# http://127.0.0.1:8050). Para parar: Ctrl+C no terminal.
#
# Um app Dash tem 3 partes, na ordem deste arquivo:
#   1. Dados      -> o df carregado uma vez, quando o app sobe
#   2. Layout     -> o "esqueleto" da página: títulos, filtros e gráficos
#   3. Callbacks  -> funções que redesenham os gráficos quando um filtro muda
# Os gráficos em si vêm de visualization.py, os mesmos do notebook.
# =============================================================================
import pandas as pd
from dash import Dash, Input, Output, callback, dcc, html

from social_media_impact.config import DASH_DEBUG, DASH_HOST, DASH_PORT
from social_media_impact.data import load_raw
from social_media_impact.visualization import (
    colunas_categoricas,
    colunas_numericas,
    grafico_barras,
    grafico_distribuicao,
    para_exibicao,
    rotulo,
)

# -----------------------------------------------------------------------------
# 1. Dados
# -----------------------------------------------------------------------------
df = para_exibicao(load_raw())
PLATAFORMAS = sorted(df["plataforma_principal"].cat.categories)

# -----------------------------------------------------------------------------
# 2. Layout
# -----------------------------------------------------------------------------
# html.* são as partes da página (Div = caixa, H1 = título, P = parágrafo).
# dcc.* são os componentes interativos (Dropdown = lista, Graph = gráfico).
# Cada componente usado num callback precisa de um id único.


def opcoes(colunas: list[str]) -> list[dict]:
    """Transforma nomes de colunas em opções de Dropdown com o nome legível."""
    return [{"label": rotulo(coluna), "value": coluna} for coluna in colunas]


def bloco_grafico(titulo: str, id_dropdown: str, colunas: list[str], inicial: str, id_grafico: str):
    """Caixa com título, lista para escolher a coluna e o gráfico."""
    return html.Div(
        style={"flex": "1", "minWidth": "400px"},
        children=[
            html.H3(titulo),
            dcc.Dropdown(id=id_dropdown, options=opcoes(colunas), value=inicial, clearable=False),
            dcc.Graph(id=id_grafico),
        ],
    )


app = Dash(__name__, title="Social Media Impact")

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "fontFamily": "sans-serif"},
    children=[
        html.H1("Impacto das redes sociais nos estudantes"),
        html.P("Visão geral dos estudantes: escolha a coluna de cada gráfico."),
        # Filtro geral: vale para os dois gráficos
        html.Label("Plataforma principal", htmlFor="filtro-plataforma"),
        dcc.Dropdown(
            id="filtro-plataforma",
            options=PLATAFORMAS,
            multi=True,  # permite escolher várias; vazio = todas
            placeholder="Todas as plataformas",
        ),
        html.P(id="total-estudantes", style={"fontWeight": "bold"}),
        html.Div(
            style={"display": "flex", "gap": "24px", "flexWrap": "wrap"},
            children=[
                bloco_grafico(
                    "Colunas categóricas",
                    "coluna-categorica",
                    colunas_categoricas(df),
                    "impacto_geral",
                    "grafico-barras",
                ),
                bloco_grafico(
                    "Distribuição das numéricas",
                    "coluna-numerica",
                    colunas_numericas(df),
                    "horas_uso_diario",
                    "grafico-distribuicao",
                ),
            ],
        ),
    ],
)

# -----------------------------------------------------------------------------
# 3. Callbacks
# -----------------------------------------------------------------------------
# @callback liga entradas (Input) a saídas (Output) pelo id + propriedade.
# Quando um Input muda, o Dash chama a função e coloca o retorno no Output.
# Os parâmetros da função vêm na mesma ordem dos Inputs.


def filtrar(plataformas: list[str] | None) -> pd.DataFrame:
    """Só as linhas das plataformas escolhidas; lista vazia ou None = todas."""
    if not plataformas:
        return df
    return df[df["plataforma_principal"].isin(plataformas)]


@callback(Output("total-estudantes", "children"), Input("filtro-plataforma", "value"))
def atualizar_total(plataformas):
    total = len(filtrar(plataformas))
    return f"{total:,} estudantes no filtro".replace(",", ".")


@callback(
    Output("grafico-barras", "figure"),
    Input("coluna-categorica", "value"),
    Input("filtro-plataforma", "value"),
)
def atualizar_barras(coluna, plataformas):
    return grafico_barras(filtrar(plataformas), coluna)


@callback(
    Output("grafico-distribuicao", "figure"),
    Input("coluna-numerica", "value"),
    Input("filtro-plataforma", "value"),
)
def atualizar_distribuicao(coluna, plataformas):
    return grafico_distribuicao(filtrar(plataformas), coluna)


if __name__ == "__main__":
    app.run(host=DASH_HOST, port=DASH_PORT, debug=DASH_DEBUG)
