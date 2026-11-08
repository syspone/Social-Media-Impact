# =============================================================================
# Gráficos do projeto
# -----------------------------------------------------------------------------
# Único lugar onde os gráficos são montados. O notebook e o painel (dashboard.py)
# chamam estas funções, então uma mudança aqui vale para os dois.
# As funções devolvem a figura do Plotly; quem chama decide se mostra
# (fig.show() no notebook) ou coloca num dcc.Graph (no painel).
# =============================================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Nomes legíveis das colunas, para títulos e eixos dos gráficos
ROTULOS = {
    "idade": "Idade (anos)",
    "genero": "Gênero",
    "nivel_academico": "Nível acadêmico",
    "plataforma_principal": "Plataforma principal",
    "tipo_dispositivo": "Tipo de dispositivo",
    "frequencia_comparacao_social": "Frequência de comparação social",
    "impacto_geral": "Impacto geral",
    "horas_uso_diario": "Uso diário (horas)",
    "horas_extras_fim_de_semana": "Horas extras no fim de semana",
    "horas_sono": "Sono (horas)",
    "qualidade_sono": "Qualidade do sono (1 a 5)",
    "estresse_percebido": "Estresse percebido (0 a 40)",
    "indice_saude_mental": "Índice de saúde mental",
    "media_academica": "Média acadêmica (GPA)",
    "uso_madrugada": "Uso de madrugada",
}

# Nomes em português das estatísticas do df.describe()
ESTATISTICAS = {
    "count": "Qtd",
    "mean": "Média",
    "std": "Desvio padrão",
    "min": "Mínimo",
    "25%": "1º quartil (25%)",
    "50%": "Mediana (50%)",
    "75%": "3º quartil (75%)",
    "max": "Máximo",
}

SIM_NAO = {True: "Sim", False: "Não"}


def rotulo(coluna: str) -> str:
    """Nome legível da coluna; se não estiver no ROTULOS, devolve o próprio nome."""
    return ROTULOS.get(coluna, coluna)


def colunas_categoricas(df: pd.DataFrame) -> list[str]:
    """Colunas de categoria e as de sim/não (bool), na ordem do df."""
    return df.select_dtypes(include=["category", "bool"]).columns.tolist()


def colunas_numericas(df: pd.DataFrame) -> list[str]:
    """Colunas numéricas, na ordem do df."""
    return df.select_dtypes(include="number").columns.tolist()


def para_exibicao(df: pd.DataFrame) -> pd.DataFrame:
    """Cópia do df com Sim/Não no lugar de True/False, só para gráficos e tabelas.

    O df original continua com bool, que é o melhor tipo para as contas
    (ex.: df["uso_madrugada"].mean() dá a proporção de quem usa de madrugada).
    """
    return df.assign(uso_madrugada=df["uso_madrugada"].map(SIM_NAO))


def resumo_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """describe() das colunas numéricas, com linhas e estatísticas em português."""
    return df.describe().T.rename(columns=ESTATISTICAS, index=ROTULOS).round(2)


def contagem(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Quantidade e % de cada categoria da coluna, na ordem das categorias."""
    tabela = df[coluna].value_counts(sort=False).to_frame("qtd")
    tabela["pct"] = (tabela["qtd"] / len(df) * 100).round(1)
    return tabela


def grafico_barras(df: pd.DataFrame, coluna: str) -> go.Figure:
    """Barras com a quantidade de estudantes em cada categoria da coluna."""
    fig = px.histogram(
        df,
        x=coluna,
        labels=ROTULOS,
        title=f"Estudantes por {rotulo(coluna).lower()}",
        text_auto=True,  # mostra a quantidade em cima de cada barra
    )
    fig.update_layout(yaxis_title="Estudantes", bargap=0.2)
    return fig


def grafico_distribuicao(df: pd.DataFrame, coluna: str) -> go.Figure:
    """Histograma da coluna numérica com um boxplot em cima (mediana, quartis e extremos)."""
    fig = px.histogram(
        df,
        x=coluna,
        marginal="box",
        labels=ROTULOS,
        title=f"Distribuição: {rotulo(coluna)}",
    )
    fig.update_layout(yaxis_title="Estudantes", bargap=0.05)
    return fig
