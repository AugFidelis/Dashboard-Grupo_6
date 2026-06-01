import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# Aqui eu carrego a base ja tratada no script de preparacao.
# Essa base e a que alimenta todos os graficos do dashboard.

# ── Dados ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/processed/walmart_limpo.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ── Paleta ────────────────────────────────────────────────────────────────────
# Separei as cores em variaveis para manter o dashboard padronizado
# e facilitar qualquer ajuste visual antes da apresentacao.
AZUL    = "#1A56A0"
CINZA_E = "#444444"
CINZA_M = "#777777"
CINZA_L = "#AAAAAA"
BORDA   = "#DDDDDD"
FUNDO   = "#F5F5F5"
BRANCO  = "#FFFFFF"
TEXTO   = "#111111"

CORES_TIPO   = {"A": AZUL, "B": CINZA_E}
ESCALA_AZUL  = [[0, "#C8D9EF"], [1, AZUL]]
ESCALA_CINZA = [[0, "#E0E0E0"], [1, CINZA_E]]

# ── Template Plotly — estilo acadêmico ───────────────────────────────────────
# O template do Plotly evita repetir configuracoes de fonte, fundo,
# legenda e eixos em cada grafico que foi criado.
pio.templates["academico"] = go.layout.Template(
    layout=dict(
        font=dict(family="'IBM Plex Sans', sans-serif", color=TEXTO, size=12),
        paper_bgcolor=BRANCO,
        plot_bgcolor=BRANCO,
        colorway=[AZUL, CINZA_E, "#5B8DB8", "#888888", "#2C4A6B", "#A0A0A0"],
        title=dict(
            font=dict(family="'IBM Plex Sans', sans-serif", size=13,
                      color=TEXTO, weight=500),
            x=0, xanchor="left", pad=dict(l=0, t=0),
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            linecolor=BORDA, linewidth=1, showline=True,
            tickcolor=BORDA, tickfont=dict(size=11, color=CINZA_M),
            title_font=dict(size=11, color=CINZA_M),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#EEEEEE", gridwidth=1,
            zeroline=False, linecolor="rgba(0,0,0,0)",
            tickcolor="rgba(0,0,0,0)",
            tickfont=dict(size=11, color=CINZA_M),
            title_font=dict(size=11, color=CINZA_M),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            font=dict(size=11, color=CINZA_M),
            orientation="h", yanchor="bottom", y=1.02,
        ),
        margin=dict(l=4, r=4, t=40, b=4),
        hoverlabel=dict(
            bgcolor=TEXTO, font_color=BRANCO,
            font_size=12, bordercolor=TEXTO,
        ),
        hovermode="x unified",
    )
)
pio.templates.default = "academico"

# ── KPIs ──────────────────────────────────────────────────────────────────────
# Estes indicadores sao calculados uma vez no inicio porque aparecem
# nos cards principais da visao geral.
total_vendas    = df["Weekly_Sales"].sum()
media_semanal   = df["Weekly_Sales"].mean()
total_lojas     = df["Store"].nunique()
loja_top        = df.groupby("Store")["Weekly_Sales"].sum().idxmax()
total_registros = len(df)
media_geral     = df["Weekly_Sales"].mean()

def fmt(v):
    # Formata valores grandes para os cards ficarem mais faceis de ler.
    if v >= 1e9: return f"${v/1e9:.2f}B"
    if v >= 1e6: return f"${v/1e6:.1f}M"
    return f"${v:,.0f}"

# ── App ───────────────────────────────────────────────────────────────────────
# Inicio da aplicacao Dash. O suppress_callback_exceptions permite
# callbacks de componentes que so aparecem quando a aba e aberta.
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Análise de Vendas Walmart — Grupo 6"

WRAP = {"maxWidth": "1280px", "margin": "0 auto", "padding": "0 32px"}

ESTILO_CARTA = {
    "background": BRANCO,
    "border": f"1px solid {BORDA}",
    "borderRadius": "3px",
    "padding": "20px",
}

# ── Header ────────────────────────────────────────────────────────────────────
# Cabecalho fixo com o titulo do trabalho e as abas de navegacao.
# As abas separam a visao resumida da parte interativa.
header = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Span("Análise de Vendas Walmart", style={
                    "fontFamily": "'IBM Plex Serif', serif",
                    "fontSize": "18px", "fontWeight": "500",
                    "color": TEXTO, "letterSpacing": "-0.2px",
                }),
                html.Span(" · 2010–2012", style={
                    "fontSize": "14px", "color": CINZA_M,
                    "fontFamily": "'IBM Plex Sans', sans-serif",
                    "fontWeight": "300", "marginLeft": "4px",
                }),
            ]),
            html.Div("Grupo 6", style={
                "fontSize": "12px", "color": CINZA_M,
                "fontFamily": "'IBM Plex Sans', sans-serif",
            }),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "baseline", "paddingBottom": "14px",
        }),
        dcc.Tabs(id="tabs-principal", value="tab-1", children=[
            dcc.Tab(label="Visão Geral", value="tab-1"),
            dcc.Tab(label="Exploração Interativa", value="tab-2"),
        ]),
    ], style=WRAP),
], style={
    "background": BRANCO,
    "borderBottom": f"1px solid {BORDA}",
    "paddingTop": "20px",
    "position": "sticky", "top": "0", "zIndex": "100",
})

# Layout base da pagina: primeiro entra o header e depois um conteiner
# vazio que sera preenchido conforme a aba selecionada.
app.layout = html.Div([
    header,
    html.Div(
        html.Div(id="conteudo-tab", style={"paddingTop": "28px", "paddingBottom": "48px"}),
        style=WRAP,
    ),
], style={
    "fontFamily": "'IBM Plex Sans', sans-serif",
    "background": FUNDO, "minHeight": "100vh",
})


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════

def rotulo_secao(texto):
    # Cria o titulo pequeno que separa os blocos do dashboard.
    return html.Div([
        html.Span(texto, style={
            "fontSize": "11px", "fontWeight": "500",
            "textTransform": "uppercase", "letterSpacing": "0.06em",
            "color": CINZA_M,
        }),
        html.Hr(style={
            "border": "none", "borderTop": f"1px solid {BORDA}",
            "margin": "6px 0 16px",
        }),
    ])

def layout_dashboard1():
    # Esta primeira aba mostra a leitura executiva do trabalho:
    # indicadores, graficos principais e os insights ja selecionados.
    # ── KPIs ─────────────────────────────────────────────────────────────────
    kpis_data = [
        ("Faturamento Total", fmt(total_vendas)),
        ("Venda Média Semanal", fmt(media_semanal)),
        ("Total de Lojas", str(total_lojas)),
        ("Loja com Maior Volume", f"Loja {loja_top}"),
        ("Registros Analisados", f"{total_registros:,}"),
    ]
    kpis = html.Div([
        html.Div([
            html.Div(valor, style={
                "fontSize": "24px", "fontWeight": "600",
                "color": AZUL if i == 0 else TEXTO,
                "letterSpacing": "-0.5px", "lineHeight": "1",
            }),
            html.Div(label, style={
                "fontSize": "11px", "color": CINZA_M,
                "marginTop": "5px", "fontWeight": "400",
            }),
        ], style={
            "padding": "18px 22px",
            "background": BRANCO,
            "border": f"1px solid {BORDA}",
            "borderLeft": f"3px solid {AZUL if i == 0 else BORDA}",
            "borderRadius": "3px",
            "flex": "1", "minWidth": "130px",
        })
        for i, (label, valor) in enumerate(kpis_data)
    ], style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginBottom": "28px"})

    # ── Gráfico 1: Evolução mensal ────────────────────────────────────────────
    # Agrupo por ano e mes para transformar os dados semanais em serie mensal.
    df_mensal = df.groupby(["Ano", "Mes"])["Weekly_Sales"].sum().reset_index()
    df_mensal["Periodo"] = pd.to_datetime(
        df_mensal["Ano"].astype(str) + "-" + df_mensal["Mes"].astype(str), format="%Y-%m"
    )
    df_mensal = df_mensal.sort_values("Periodo")
    df_mensal["Vendas_M"] = df_mensal["Weekly_Sales"] / 1_000_000

    fig_tendencia = px.line(
        df_mensal, x="Periodo", y="Vendas_M",
        title="Figura 1. Evolução Mensal das Vendas (2010–2012)",
        labels={"Vendas_M": "Faturamento ($ M)", "Periodo": ""},
        color_discrete_sequence=[AZUL],
    )
    fig_tendencia.update_traces(
        line_width=1.8, mode="lines+markers",
        marker_size=3, marker_color=AZUL,
        hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:.1f}M<extra></extra>",
    )
    fig_tendencia.update_layout(showlegend=False)

    # ── Gráfico 2: Tipo de loja ───────────────────────────────────────────────
    # Aqui comparo os tipos de loja para mostrar qual grupo puxa mais faturamento.
    df_tipo = df.groupby("Type")["Weekly_Sales"].agg(["sum", "mean"]).reset_index()
    df_tipo.columns = ["Tipo", "Total", "Media"]
    df_tipo["Total_B"] = df_tipo["Total"] / 1_000_000_000
    df_tipo["Share"] = (df_tipo["Total"] / df_tipo["Total"].sum() * 100).round(1)

    fig_tipo = px.bar(
        df_tipo, x="Tipo", y="Total_B",
        title="Figura 2. Faturamento por Tipo de Loja",
        labels={"Total_B": "Faturamento ($ B)", "Tipo": ""},
        color="Tipo", color_discrete_map=CORES_TIPO,
        text=df_tipo["Share"].apply(lambda x: f"{x}% do total"),
    )
    fig_tipo.update_traces(
        textposition="outside", textfont_size=11,
        marker_line_width=0, width=0.4,
    )
    fig_tipo.update_layout(showlegend=False)

    # ── Gráfico 3: Feriados ───────────────────────────────────────────────────
    # Calculo a media por feriado para ver quais datas mudam mais o resultado.
    df_feriado = df.groupby("Nome_Feriado")["Weekly_Sales"].mean().reset_index()
    df_feriado.columns = ["Feriado", "Media_Vendas"]
    df_feriado = df_feriado.sort_values("Media_Vendas", ascending=False)
    df_feriado["Variacao"] = ((df_feriado["Media_Vendas"] - media_geral) / media_geral * 100).round(1)
    df_feriado["Cor"] = df_feriado["Media_Vendas"].apply(
        lambda x: AZUL if x >= media_geral else CINZA_L
    )

    fig_feriados = go.Figure(go.Bar(
        x=df_feriado["Feriado"],
        y=df_feriado["Media_Vendas"],
        marker_color=df_feriado["Cor"],
        marker_line_width=0,
        text=[f"{v:+.1f}%" for v in df_feriado["Variacao"]],
        textposition="outside",
        textfont=dict(size=11, color=CINZA_M),
        hovertemplate="<b>%{x}</b><br>Média: $%{y:,.0f}<extra></extra>",
    ))
    fig_feriados.add_hline(
        y=media_geral, line_dash="dot", line_color=CINZA_L, line_width=1,
        annotation_text="Média geral", annotation_font_size=10,
        annotation_font_color=CINZA_M, annotation_position="top right",
    )
    fig_feriados.update_layout(
        title="Figura 3. Venda Média Semanal por Período",
        yaxis_title="Venda Média ($)", xaxis_title="",
    )

    # ── Gráfico 4: Top 10 lojas ───────────────────────────────────────────────
    # Seleciono as 10 lojas com maior faturamento acumulado no periodo.
    df_lojas = df.groupby("Store")["Weekly_Sales"].sum().reset_index()
    df_lojas.columns = ["Loja", "Total"]
    df_lojas = df_lojas.nlargest(10, "Total")
    df_lojas["Total_M"] = df_lojas["Total"] / 1_000_000
    df_lojas["Loja"] = df_lojas["Loja"].apply(lambda x: f"Loja {x:02d}")
    df_lojas = df_lojas.sort_values("Total_M", ascending=True)

    fig_top_lojas = px.bar(
        df_lojas, x="Total_M", y="Loja", orientation="h",
        title="Figura 4. Top 10 Lojas por Faturamento Total",
        labels={"Total_M": "Faturamento ($ M)", "Loja": ""},
        color="Total_M", color_continuous_scale=ESCALA_AZUL,
        text="Total_M",
    )
    fig_top_lojas.update_traces(
        texttemplate="$%{x:.0f}M", textposition="outside",
        textfont=dict(size=10), marker_line_width=0,
    )
    fig_top_lojas.update_layout(coloraxis_showscale=False)

    # ── Callout de insights ───────────────────────────────────────────────────
    # Os insights resumem as conclusoes que eu quero defender na apresentacao.
    insights = html.Div([
        html.Div(style={
            "width": "3px", "background": AZUL,
            "marginRight": "18px", "flexShrink": "0",
        }),
        html.Div([
            html.Div("Principais achados", style={
                "fontSize": "11px", "fontWeight": "500",
                "color": AZUL, "marginBottom": "8px",
                "textTransform": "uppercase", "letterSpacing": "0.05em",
            }),
            html.Ul([
                html.Li("Ação de Graças eleva a venda média em +41%, configurando-se como o principal evento comercial do período analisado."),
                html.Li("Natal apresenta venda 8% abaixo da média geral, indicando que as compras natalinas concentram-se em novembro."),
                html.Li("Lojas Tipo A representam 50% das unidades, mas respondem por 65% do faturamento total, em razão de seu maior porte médio."),
                html.Li("A venda média semanal recuou de $17.824 (2010) para $17.110 (2012), redução de aproximadamente 4% no período."),
            ], style={
                "margin": "0", "paddingLeft": "16px",
                "lineHeight": "1.8", "color": TEXTO,
                "fontSize": "13px",
            }),
        ]),
    ], style={
        "display": "flex",
        "background": BRANCO,
        "border": f"1px solid {BORDA}",
        "borderLeft": f"3px solid {AZUL}",
        "borderRadius": "3px",
        "padding": "18px 22px",
        "marginBottom": "24px",
    })

    def carta(fig, span=1):
        # Pequena funcao auxiliar para nao repetir a estrutura visual dos graficos.
        return html.Div(
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
            style={**ESTILO_CARTA, "gridColumn": f"span {span}"},
        )

    grid = html.Div([
        carta(fig_tendencia, 2),
        carta(fig_tipo, 1),
        carta(fig_feriados, 2),
        carta(fig_top_lojas, 1),
    ], style={
        "display": "grid",
        "gridTemplateColumns": "repeat(3, 1fr)",
        "gap": "16px", "marginBottom": "24px",
    })

    return html.Div([
        rotulo_secao("Indicadores gerais"),
        kpis,
        insights,
        rotulo_secao("Visualizações"),
        grid,
    ])


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 2 — EXPLORAÇÃO INTERATIVA
# ══════════════════════════════════════════════════════════════════════════════

def layout_dashboard2():
    # A segunda aba e a parte interativa: o usuario filtra os dados
    # e todos os graficos abaixo sao atualizados pelos callbacks.
    anos_disp   = sorted(df["Ano"].unique())
    tipos_disp  = sorted(df["Type"].unique())
    portes_disp = ["Pequena", "Média", "Grande"]
    estacoes    = ["Verão", "Outono", "Inverno", "Primavera"]

    def check(id_, opts, vals):
        # Cria listas de selecao reutilizaveis para ano, tipo e porte de loja.
        return dcc.Checklist(
            id=id_,
            options=[{"label": html.Span(str(o), style={"fontSize": "13px", "marginLeft": "6px"}), "value": o} for o in opts],
            value=vals,
            style={"display": "flex", "flexDirection": "column", "gap": "7px"},
            inputStyle={"accentColor": AZUL, "width": "13px", "height": "13px", "cursor": "pointer"},
        )

    def rotulo_filtro(texto):
        # Padroniza os titulos pequenos usados acima de cada filtro.
        return html.Div(texto, style={
            "fontSize": "10.5px", "fontWeight": "500",
            "textTransform": "uppercase", "letterSpacing": "0.06em",
            "color": CINZA_M, "marginBottom": "8px", "marginTop": "16px",
        })

    # Barra lateral com todos os filtros que controlam os graficos da aba 2.
    sidebar = html.Div([
        html.Div("Filtros", style={
            "fontSize": "13px", "fontWeight": "500",
            "color": TEXTO, "paddingBottom": "12px",
            "borderBottom": f"1px solid {BORDA}",
            "marginBottom": "4px",
        }),

        rotulo_filtro("Ano"),
        check("filtro-ano", anos_disp, anos_disp),

        rotulo_filtro("Tipo de Loja"),
        check("filtro-tipo", tipos_disp, tipos_disp),

        rotulo_filtro("Porte da Loja"),
        check("filtro-porte", portes_disp, portes_disp),

        rotulo_filtro("Temperatura"),
        dcc.Dropdown(
            id="filtro-temperatura",
            options=[{"label": t, "value": t} for t in ["Todas", "Frio", "Agradável", "Quente"]],
            value="Todas", clearable=False,
            style={"fontSize": "13px"},
        ),

        rotulo_filtro("Estação"),
        dcc.Dropdown(
            id="filtro-estacao",
            options=[{"label": e, "value": e} for e in ["Todas"] + estacoes],
            value="Todas", clearable=False,
            style={"fontSize": "13px"},
        ),
    ], style={
        "width": "210px", "flexShrink": "0",
        "background": BRANCO,
        "border": f"1px solid {BORDA}",
        "borderRadius": "3px",
        "padding": "18px 16px",
        "position": "sticky", "top": "76px",
        "height": "fit-content",
    })

    def graf_box(id_graf):
        # Cria o card do grafico deixando o codigo do layout mais limpo.
        return html.Div(
            dcc.Graph(id=id_graf, config={"displayModeBar": False}),
            style=ESTILO_CARTA,
        )

    # Area principal onde ficam os graficos que respondem aos filtros.
    charts_area = html.Div([
        html.Div([
            graf_box("graf-vendas-tempo"),
            graf_box("graf-feriados"),
        ], style={"display": "grid", "gridTemplateColumns": "2fr 1fr",
                  "gap": "14px", "marginBottom": "14px"}),
        html.Div([
            graf_box("graf-departamentos"),
            graf_box("graf-boxplot-tipo"),
            graf_box("graf-markdown"),
        ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr",
                  "gap": "14px", "marginBottom": "14px"}),
        html.Div([
            graf_box("graf-trimestre"),
            graf_box("graf-porte"),
        ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                  "gap": "14px"}),
    ], style={"flex": "1", "minWidth": "0"})

    return html.Div([sidebar, charts_area], style={
        "display": "flex", "gap": "20px", "alignItems": "flex-start",
    })


# ── Callback: troca de tab ────────────────────────────────────────────────────
@callback(Output("conteudo-tab", "children"), Input("tabs-principal", "value"))
def renderizar_tab(tab):
    # Quando a pessoa troca a aba, este callback escolhe qual layout mostrar.
    if tab == "tab-1":
        return layout_dashboard1()
    return layout_dashboard2()


# ── Filtro compartilhado ──────────────────────────────────────────────────────
def filtrar(anos, tipos, porte, temperatura, estacao):
    # Filtro centralizado: todos os graficos interativos usam a mesma regra
    # para garantir que os resultados estejam falando da mesma selecao.
    mask = df["Ano"].isin(anos) & df["Type"].isin(tipos) & df["Porte_Loja"].isin(porte)
    if temperatura != "Todas":
        mask &= df["Faixa_Temperatura"] == temperatura
    if estacao != "Todas":
        mask &= df["Estacao"] == estacao
    return df[mask]

INPUTS_FILTRO = [
    # Lista comum de entradas dos filtros. Assim eu nao preciso repetir
    # os mesmos Inputs manualmente em cada callback.
    Input("filtro-ano", "value"),
    Input("filtro-tipo", "value"),
    Input("filtro-porte", "value"),
    Input("filtro-temperatura", "value"),
    Input("filtro-estacao", "value"),
]


# ── Callbacks ─────────────────────────────────────────────────────────────────
@callback(Output("graf-vendas-tempo", "figure"), *INPUTS_FILTRO)
def update_vendas_tempo(anos, tipos, porte, temperatura, estacao):
    # Grafico de linha: mostra como as vendas evoluem no tempo
    # depois que os filtros da aba interativa sao aplicados.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    # Agrupo por mes e tipo de loja para comparar tendencias entre A e B.
    df_mes = dff.groupby(["Ano", "Mes", "Type"])["Weekly_Sales"].sum().reset_index()
    df_mes["Periodo"] = pd.to_datetime(
        df_mes["Ano"].astype(str) + "-" + df_mes["Mes"].astype(str), format="%Y-%m"
    )
    df_mes["Vendas_M"] = df_mes["Weekly_Sales"] / 1_000_000
    fig = px.line(
        df_mes.sort_values("Periodo"), x="Periodo", y="Vendas_M", color="Type",
        title="Evolução das Vendas por Tipo de Loja",
        labels={"Vendas_M": "Vendas ($ M)", "Periodo": "", "Type": "Tipo"},
        color_discrete_map=CORES_TIPO, markers=True,
    )
    fig.update_traces(marker_size=3, line_width=1.8)
    return fig


@callback(Output("graf-feriados", "figure"), *INPUTS_FILTRO)
def update_feriados(anos, tipos, porte, temperatura, estacao):
    # Mostra a venda media de cada feriado dentro do recorte escolhido.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    df_f = dff.groupby("Nome_Feriado")["Weekly_Sales"].mean().reset_index()
    df_f.columns = ["Feriado", "Media"]
    df_f = df_f.sort_values("Media", ascending=True)
    fig = px.bar(
        df_f, x="Media", y="Feriado", orientation="h",
        title="Venda Média por Feriado",
        labels={"Media": "Venda Média ($)", "Feriado": ""},
        color="Media", color_continuous_scale=ESCALA_AZUL,
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    return fig


@callback(Output("graf-departamentos", "figure"), *INPUTS_FILTRO)
def update_departamentos(anos, tipos, porte, temperatura, estacao):
    # Identifica quais departamentos mais faturaram no recorte filtrado.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    df_d = dff.groupby("Dept")["Weekly_Sales"].sum().reset_index().nlargest(15, "Weekly_Sales")
    df_d["Vendas_M"] = df_d["Weekly_Sales"] / 1_000_000
    df_d["Dept"] = df_d["Dept"].apply(lambda x: f"Dept {x:02d}")
    df_d = df_d.sort_values("Vendas_M", ascending=True)
    fig = px.bar(
        df_d, x="Vendas_M", y="Dept", orientation="h",
        title="Top 15 Departamentos por Faturamento",
        labels={"Vendas_M": "Faturamento ($ M)", "Dept": ""},
        color="Vendas_M", color_continuous_scale=ESCALA_CINZA,
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False)
    return fig


@callback(Output("graf-boxplot-tipo", "figure"), *INPUTS_FILTRO)
def update_boxplot(anos, tipos, porte, temperatura, estacao):
    # Boxplot usado para comparar a distribuicao das vendas entre tipos de loja.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    fig = px.box(
        dff[dff["Weekly_Sales"] > 0],
        x="Type", y="Weekly_Sales",
        title="Distribuição por Tipo de Loja",
        labels={"Type": "", "Weekly_Sales": "Venda Semanal ($)"},
        color="Type", color_discrete_map=CORES_TIPO, points=False,
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(showlegend=False)
    return fig


@callback(Output("graf-markdown", "figure"), *INPUTS_FILTRO)
def update_markdown(anos, tipos, porte, temperatura, estacao):
    # Compara semanas com promocao e sem promocao para observar o efeito das markdowns.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    # Uso copy para criar colunas auxiliares sem modificar o dataframe original.
    dff = dff.copy()
    dff["Promocao"] = dff["Tem_Promocao"].map({True: "Com promoção", False: "Sem promoção"})
    df_md = dff.groupby(["Mes", "Promocao"])["Weekly_Sales"].mean().reset_index()
    df_md["Mes_Nome"] = df_md["Mes"].apply(
        lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun",
                   "Jul","Ago","Set","Out","Nov","Dez"][m - 1]
    )
    fig = px.bar(
        df_md, x="Mes_Nome", y="Weekly_Sales", color="Promocao",
        barmode="group",
        title="Promoções vs Vendas por Mês",
        labels={"Weekly_Sales": "Venda Média ($)", "Mes_Nome": "", "Promocao": ""},
        color_discrete_map={"Com promoção": AZUL, "Sem promoção": CINZA_L},
    )
    fig.update_traces(marker_line_width=0)
    return fig


@callback(Output("graf-trimestre", "figure"), *INPUTS_FILTRO)
def update_trimestre(anos, tipos, porte, temperatura, estacao):
    # Resume as vendas por trimestre para facilitar comparacoes sazonais.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    df_t = dff.groupby(["Trimestre", "Type"])["Weekly_Sales"].mean().reset_index()
    fig = px.bar(
        df_t.sort_values("Trimestre"), x="Trimestre", y="Weekly_Sales", color="Type",
        barmode="group",
        title="Venda Média por Trimestre",
        labels={"Weekly_Sales": "Venda Média ($)", "Trimestre": "", "Type": "Tipo"},
        color_discrete_map=CORES_TIPO,
        category_orders={"Trimestre": ["Q1", "Q2", "Q3", "Q4"]},
    )
    fig.update_traces(marker_line_width=0)
    return fig


@callback(Output("graf-porte", "figure"), *INPUTS_FILTRO)
def update_porte(anos, tipos, porte, temperatura, estacao):
    # Cruza porte da loja com estacao do ano para analisar diferencas de comportamento.
    dff = filtrar(anos, tipos, porte, temperatura, estacao)
    if dff.empty:
        return go.Figure()
    df_p = dff.groupby(["Porte_Loja", "Estacao"])["Weekly_Sales"].mean().reset_index()
    fig = px.bar(
        df_p, x="Porte_Loja", y="Weekly_Sales", color="Estacao",
        barmode="group",
        title="Venda por Porte de Loja e Estação",
        labels={"Weekly_Sales": "Venda Média ($)", "Porte_Loja": "", "Estacao": "Estação"},
        category_orders={
            "Porte_Loja": ["Pequena", "Média", "Grande"],
            "Estacao": ["Verão", "Outono", "Inverno", "Primavera"],
        },
        color_discrete_sequence=[AZUL, CINZA_E, "#5B8DB8", CINZA_L],
    )
    fig.update_traces(marker_line_width=0)
    return fig


if __name__ == "__main__":
    # Executa o servidor local do Dash quando rodamos: python app.py
    app.run(debug=True)
