# -*- coding: utf-8 -*-
import matplotlib
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

plt.rcParams["font.family"] = "DejaVu Sans"

W, H = 11.69, 8.27
AZUL    = "#1A56A0"
AZUL_E  = "#154A8A"
AZUL_C  = "#EBF1FA"
CINZA   = "#444444"
CINZA_L = "#888888"
FUNDO   = "#F5F5F5"
BRANCO  = "#FFFFFF"
AMARELO = "#D4900A"
AMARELO_C = "#FFF8E8"


def nova_figura():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(BRANCO)
    return fig


def cabecalho(fig, titulo, subtitulo=""):
    ax = fig.add_axes([0, 0.88, 1, 0.12])
    ax.set_facecolor(AZUL); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.04, 0.60, titulo, color=BRANCO, fontsize=17, fontweight="bold", va="center")
    if subtitulo:
        ax.text(0.04, 0.18, subtitulo, color="#AECBF0", fontsize=10, va="center")
    ax.text(0.97, 0.60, "Grupo 6", color="#AECBF0", fontsize=9, va="center", ha="right")


def rodape(fig, numero):
    ax = fig.add_axes([0, 0, 1, 0.055])
    ax.set_facecolor(FUNDO); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.04, 0.5, "Análise de Vendas Walmart  ·  Grupo 6  ·  PUC", color=CINZA_L, fontsize=8, va="center")


def separador(fig, y, x0=0.04, x1=0.96):
    ax = fig.add_axes([x0, y, x1 - x0, 0.003])
    ax.set_facecolor("#DDDDDD"); ax.axis("off")


def caixa_azul(fig, x, y, w, h, linha1="", linha2="", fs1=9, fs2=14):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(AZUL_C)
    for sp in ax.spines.values():
        sp.set_edgecolor(AZUL); sp.set_linewidth(1.2)
    ax.axis("off")
    ax.text(0.5, 0.75, linha1, ha="center", va="center", fontsize=fs1, color=AZUL, fontweight="bold")
    ax.text(0.5, 0.32, linha2, ha="center", va="center", fontsize=fs2, color=CINZA, fontweight="bold")


def bullet(fig, x, y, items, espaco=0.062, fs=10):
    for i, item in enumerate(items):
        fig.text(x, y - i * espaco, "●", color=AZUL, fontsize=6, va="top")
        fig.text(x + 0.022, y - i * espaco, item, fontsize=fs, color=CINZA, va="top")


# ── SLIDE 1 — Capa ────────────────────────────────────────────────────────────
def slide_capa(pdf):
    fig = nova_figura()
    ax_left = fig.add_axes([0, 0, 0.38, 1])
    ax_left.set_facecolor(AZUL); ax_left.axis("off")
    fig.add_axes([0.378, 0, 0.004, 1]).set_facecolor(AZUL_E)
    plt.gca().axis("off")

    fig.text(0.04, 0.83, "Projeto Final de Análise de Dados", color="#AECBF0", fontsize=10, va="top")
    fig.text(0.04, 0.76, "Dashboard\nWalmart Sales", color=BRANCO, fontsize=24,
             fontweight="bold", va="top", linespacing=1.3)
    fig.text(0.04, 0.58, "Previsão de Vendas\n2010 – 2012", color="#AECBF0", fontsize=12,
             va="top", linespacing=1.4)
    fig.text(0.04, 0.30, "Grupo 6", color=BRANCO, fontsize=11, fontweight="bold", va="top")
    fig.text(0.04, 0.24, "PUC — 2025", color="#AECBF0", fontsize=10, va="top")

    fig.text(0.44, 0.83, "Visão Geral do Projeto", color=CINZA_L, fontsize=10, va="top")
    fig.text(0.44, 0.78, "Walmart Store Sales Forecasting", color=CINZA, fontsize=14,
             fontweight="bold", va="top")

    separador(fig, 0.66, x0=0.44, x1=0.97)

    kpis = [("421.570", "registros"), ("45", "lojas"), ("81", "depart."), ("25", "variáveis")]
    for i, (v, l) in enumerate(kpis):
        caixa_azul(fig, 0.44 + i * 0.135, 0.36, 0.12, 0.24, linha1=l, linha2=v, fs1=8, fs2=17)

    fig.text(0.44, 0.28, "Período: fevereiro/2010 – outubro/2012", color=CINZA_L, fontsize=9, va="top")
    fig.text(0.44, 0.22, "Tecnologias: Python · Pandas · Plotly Dash · Matplotlib", color=CINZA_L, fontsize=9, va="top")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 2 — Base de Dados Escolhida ────────────────────────────────────────
def slide_base_dados(pdf):
    fig = nova_figura()
    cabecalho(fig, "1. Base de Dados Escolhida")
    rodape(fig, 2)

    fig.text(0.04, 0.83, "Identificação do conjunto de dados", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    bullet(fig, 0.04, 0.76, [
        "Nome: Walmart Store Sales Forecasting",
        "Fonte: Kaggle — competição pública de previsão de vendas no varejo",
        "Endereço: kaggle.com/c/walmart-recruiting-store-sales-forecasting",
        "Cobertura temporal: fevereiro de 2010 a outubro de 2012 (143 semanas)",
        "Escopo geográfico: 45 lojas localizadas nos Estados Unidos",
    ], espaco=0.065)

    separador(fig, 0.36)

    fig.text(0.04, 0.33, "Justificativa da escolha", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    razoes = [
        ("Volume e riqueza",
         "421.570 registros semanais com variáveis\n"
         "de vendas, clima, promoções e indicadores\n"
         "macroeconômicos (CPI, desemprego)."),
        ("Diversidade analítica",
         "Permite explorar sazonalidade, impacto de\n"
         "feriados, desempenho por tipo de loja e\n"
         "efetividade de promoções por departamento."),
        ("Relevância prática",
         "Dados reais de um dos maiores varejistas\n"
         "do mundo, com aplicabilidade direta em\n"
         "decisões estratégicas de negócio."),
    ]

    for i, (tit, desc) in enumerate(razoes):
        bx = 0.04 + i * 0.315
        ax = fig.add_axes([bx, 0.07, 0.29, 0.23])
        ax.set_facecolor(AZUL_C)
        for sp in ax.spines.values():
            sp.set_edgecolor(AZUL); sp.set_linewidth(1)
        ax.axis("off")
        ax.text(0.5, 0.90, tit, ha="center", va="top", fontsize=10, color=AZUL, fontweight="bold")
        ax.text(0.5, 0.68, desc, ha="center", va="top", fontsize=8.5, color=CINZA, linespacing=1.4)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 3 — Caracterização dos Dados Originais ─────────────────────────────
def slide_caracterizacao(pdf):
    fig = nova_figura()
    cabecalho(fig, "2. Caracterização dos Dados Originais")
    rodape(fig, 3)

    fig.text(0.04, 0.83, "Os dados originais são compostos por três arquivos CSV distintos:", color=CINZA,
             fontsize=11, va="top")

    headers = ["Arquivo", "Linhas", "Colunas", "Variáveis principais"]
    rows = [
        ["train.csv", "421.570", "5", "Store, Dept, Date, Weekly_Sales, IsHoliday"],
        ["features.csv", "8.190", "12", "Temperature, Fuel_Price, MarkDown1 a MarkDown5, CPI, Unemployment"],
        ["stores.csv", "45", "3", "Store, Type (A/B/C), Size (área em pés quadrados)"],
    ]
    col_x = [0.04, 0.24, 0.34, 0.44]
    col_w = [0.19, 0.09, 0.09, 0.52]

    y_h = 0.72
    for j, (h, cx, cw) in enumerate(zip(headers, col_x, col_w)):
        ax = fig.add_axes([cx, y_h, cw - 0.01, 0.075])
        ax.set_facecolor(AZUL); ax.axis("off")
        ax.text(0.5, 0.5, h, ha="center", va="center", color=BRANCO, fontsize=10, fontweight="bold")

    for i, row in enumerate(rows):
        y_r = y_h - (i + 1) * 0.095
        cor = AZUL_C if i % 2 == 0 else BRANCO
        for j, (cell, cx, cw) in enumerate(zip(row, col_x, col_w)):
            ax = fig.add_axes([cx, y_r, cw - 0.01, 0.085])
            ax.set_facecolor(cor)
            for sp in ax.spines.values():
                sp.set_edgecolor("#CCCCCC"); sp.set_linewidth(0.5)
            ax.axis("off")
            ha = "left" if j in [0, 3] else "center"
            px = 0.05 if ha == "left" else 0.5
            ax.text(px, 0.5, cell, ha=ha, va="center", fontsize=9, color=CINZA)

    separador(fig, 0.36)

    fig.text(0.04, 0.33, "Problemas identificados antes do tratamento", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    bullet(fig, 0.04, 0.27, [
        "Valores ausentes: MarkDown1 a MarkDown5 com alta proporção de NaN (semanas sem promoção)",
        "Inconsistências: valores negativos registrados nas colunas de desconto (erro de sistema)",
        "Tipo incorreto: coluna Date armazenada como texto (string), não como objeto de data",
        "Sem variáveis temporais: ausência de colunas derivadas de data (Ano, Mês, Trimestre)",
    ], espaco=0.062)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 4 — Preparação e Tratamento ────────────────────────────────────────
def slide_preparacao(pdf):
    fig = nova_figura()
    cabecalho(fig, "3. Preparação e Tratamento dos Dados")
    rodape(fig, 4)

    fig.text(0.04, 0.83, "Problemas encontrados e soluções aplicadas", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    problemas = [
        ("Valores ausentes (NaN)",
         "MarkDown1–5 preenchidos com 0.\n"
         "Ausência indica semana sem promoção."),
        ("Valores inconsistentes",
         "MarkDown negativos substituídos por 0.\n"
         "Desconto negativo é erro de registro."),
        ("Tipo de dado incorreto",
         "Coluna Date convertida para datetime\n"
         "com pd.to_datetime()."),
        ("Registros duplicados",
         "Duplicatas removidas via\n"
         "drop_duplicates()."),
    ]

    for i, (prob, sol) in enumerate(problemas):
        bx = 0.04 + (i % 2) * 0.49
        by = 0.54 if i < 2 else 0.30
        ax = fig.add_axes([bx, by, 0.45, 0.22])
        ax.set_facecolor(FUNDO)
        for sp in ax.spines.values():
            sp.set_edgecolor(AZUL); sp.set_linewidth(1.2)
        ax.axis("off")
        ax.text(0.03, 0.88, prob, va="top", fontsize=10, color=AZUL, fontweight="bold")
        ax.text(0.03, 0.55, sol, va="top", fontsize=9.5, color=CINZA, linespacing=1.4)

    separador(fig, 0.26)

    fig.text(0.04, 0.23, "Engenharia de atributos — 9 novas variáveis criadas", color=AZUL,
             fontsize=11, fontweight="bold", va="top")

    novas = [
        ("Temporais", "Ano, Mês, Trimestre (Q1–Q4)"),
        ("Sazonais", "Estação do Ano (Inverno/Primavera/Verão/Outono)"),
        ("Clima", "Faixa de Temperatura (Frio/Agradável/Quente)"),
        ("Feriados", "Nome do Feriado (Natal, Ação de Graças, Super Bowl…)"),
        ("Promoções", "Total Markdown (soma MarkDown1–5), Flag Tem Promoção"),
        ("Porte", "Porte da Loja (Pequena/Média/Grande — percentis 33/66)"),
    ]

    for i, (cat, desc) in enumerate(novas):
        col = i % 3
        row = i // 3
        ax = fig.add_axes([0.04 + col * 0.32, 0.10 - row * 0.075, 0.30, 0.062])
        ax.set_facecolor(AZUL_C)
        for sp in ax.spines.values():
            sp.set_edgecolor(AZUL); sp.set_linewidth(0.8)
        ax.axis("off")
        ax.text(0.03, 0.80, cat, va="top", fontsize=8.5, color=AZUL, fontweight="bold")
        ax.text(0.03, 0.32, desc, va="top", fontsize=8, color=CINZA)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 5 — Integração dos Dados ───────────────────────────────────────────
def slide_integracao(pdf):
    fig = nova_figura()
    cabecalho(fig, "4. Integração dos Dados")
    rodape(fig, 5)

    fig.text(0.04, 0.83, "Três arquivos combinados via left join para formar o dataset final:", color=CINZA,
             fontsize=11, va="top")

    def box_arquivo(fig, x, y, nome, dims, vars_txt):
        ax = fig.add_axes([x, y, 0.20, 0.22])
        ax.set_facecolor(AZUL_C)
        for sp in ax.spines.values():
            sp.set_edgecolor(AZUL); sp.set_linewidth(1.5)
        ax.axis("off")
        ax.text(0.5, 0.88, nome, ha="center", fontsize=11, fontweight="bold", color=AZUL)
        ax.text(0.5, 0.65, dims, ha="center", fontsize=9, color=CINZA)
        ax.text(0.5, 0.38, vars_txt, ha="center", fontsize=7.5, color=CINZA_L, linespacing=1.3)

    def box_merge(fig, x, y, titulo, chave, resultado):
        ax = fig.add_axes([x, y, 0.17, 0.22])
        ax.set_facecolor(AMARELO_C)
        for sp in ax.spines.values():
            sp.set_edgecolor(AMARELO); sp.set_linewidth(1.5)
        ax.axis("off")
        ax.text(0.5, 0.88, titulo, ha="center", fontsize=10, fontweight="bold", color=AMARELO)
        ax.text(0.5, 0.62, chave, ha="center", fontsize=8.5, color=CINZA)
        ax.text(0.5, 0.40, "left join", ha="center", fontsize=8.5, color=CINZA)
        ax.text(0.5, 0.16, resultado, ha="center", fontsize=9, color=AMARELO, fontweight="bold")

    box_arquivo(fig, 0.04, 0.57, "train.csv", "421.570 × 5",
                "Store, Dept, Date\nWeekly_Sales, IsHoliday")
    box_arquivo(fig, 0.04, 0.29, "stores.csv", "45 × 3",
                "Store, Type, Size")
    box_merge(fig, 0.29, 0.41, "MERGE 1", "on: Store", "421.570 × 7")
    box_arquivo(fig, 0.50, 0.11, "features.csv", "8.190 × 12",
                "Temperature, Fuel_Price\nMarkDown1–5, CPI, Unemployment")
    box_merge(fig, 0.53, 0.41, "MERGE 2", "on: Store+Date\n+IsHoliday", "421.570 × 16")

    # Dataset final
    ax_f = fig.add_axes([0.76, 0.34, 0.19, 0.30])
    ax_f.set_facecolor(AZUL); ax_f.axis("off")
    ax_f.text(0.5, 0.90, "Dataset Final", ha="center", fontsize=10, fontweight="bold", color=BRANCO)
    ax_f.text(0.5, 0.68, "421.570", ha="center", fontsize=18, fontweight="bold", color=BRANCO)
    ax_f.text(0.5, 0.48, "linhas", ha="center", fontsize=9, color="#AECBF0")
    ax_f.text(0.5, 0.32, "25 colunas", ha="center", fontsize=11, color="#AECBF0", fontweight="bold")
    ax_f.text(0.5, 0.14, "16 originais + 9 novas", ha="center", fontsize=8, color="#AECBF0")

    # Setas
    ov = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ov.axis("off"); ov.set_xlim(0, 1); ov.set_ylim(0, 1)
    setas = [
        (0.24, 0.70, 0.29, 0.58),
        (0.24, 0.40, 0.29, 0.48),
        (0.46, 0.52, 0.53, 0.52),
        (0.60, 0.33, 0.615, 0.41),
        (0.70, 0.52, 0.76, 0.52),
    ]
    for tx, ty, hx, hy in setas:
        ov.annotate("", xy=(hx, hy), xytext=(tx, ty),
                    arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.5))

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 6 — Construção dos Dashboards ──────────────────────────────────────
def slide_dashboards(pdf):
    fig = nova_figura()
    cabecalho(fig, "5. Construção dos Dashboards", "Dois painéis interativos — Python Dash + Plotly")
    rodape(fig, 6)

    # Dashboard 1
    fig.text(0.04, 0.83, "Dashboard 1 — Visão Geral (estático)", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    bullet(fig, 0.04, 0.76, [
        "Objetivo: panorama executivo com as principais métricas do período completo",
        "4 KPIs em destaque: total vendido, média semanal, melhor loja e semanas com feriado",
        "Callout de insight fixo com análise do impacto de feriados nas vendas",
    ], espaco=0.062)

    graficos_d1 = [
        "Evolução mensal das vendas (gráfico de área)",
        "Vendas médias por tipo de loja A, B e C (barras)",
        "Feriados vs. semanas normais + linha de média (barras)",
        "Top 10 lojas por receita acumulada (barras horizontais)",
    ]
    for i, g in enumerate(graficos_d1):
        cx = 0.04 + (i % 2) * 0.48
        cy = 0.44 if i < 2 else 0.32
        ax = fig.add_axes([cx, cy, 0.44, 0.10])
        ax.set_facecolor(AZUL_C)
        for sp in ax.spines.values():
            sp.set_edgecolor(AZUL); sp.set_linewidth(0.6)
        ax.axis("off")
        ax.text(0.02, 0.5, f"{i+1}.  {g}", va="center", fontsize=9.5, color=CINZA)

    separador(fig, 0.28)

    # Dashboard 2
    fig.text(0.04, 0.25, "Dashboard 2 — Análise Interativa (reativa)", color=AZUL, fontsize=12,
             fontweight="bold", va="top")

    filtros = ["Ano", "Tipo de Loja", "Porte", "Temperatura", "Estação do Ano"]
    fig.text(0.04, 0.18, "Painel lateral com 5 filtros reativos:", color=CINZA_L, fontsize=9.5, va="top")
    for i, f in enumerate(filtros):
        ax = fig.add_axes([0.04 + i * 0.152, 0.07, 0.135, 0.08])
        ax.set_facecolor(AZUL); ax.axis("off")
        ax.text(0.5, 0.5, f, ha="center", va="center", fontsize=9, color=BRANCO, fontweight="bold")

    fig.text(0.82, 0.18, "7 gráficos reativos", color=AZUL, fontsize=11,
             fontweight="bold", va="top", ha="center")
    fig.text(0.82, 0.12, "atualizados em\ntempo real", color=CINZA, fontsize=9,
             va="top", ha="center", linespacing=1.4)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 7 — Resultados e Insights (parte 1) ────────────────────────────────
def slide_insights_1(pdf):
    fig = nova_figura()
    cabecalho(fig, "6. Resultados e Insights", "Padrões identificados na análise exploratória — parte 1")
    rodape(fig, 7)

    insights = [
        (
            "Feriados geram aumento médio de ~7% nas vendas semanais",
            "Semanas com feriados como Natal e Ação de Graças apresentam vendas "
            "sistematicamente acima da média. O efeito é mais pronunciado no Q4 "
            "(out–dez), quando a diferença em relação a semanas normais pode ultrapassar 12%."
        ),
        (
            "Lojas do tipo A concentram ~70% da receita total",
            "As 22 lojas do tipo A (maior porte físico) dominam aproximadamente 70% de toda "
            "a receita do período analisado. Lojas B e C, mais numerosas proporcionalmente, "
            "possuem volume individual muito menor, revelando forte heterogeneidade no portfólio."
        ),
        (
            "Q4 é consistentemente o trimestre de maior volume em todos os anos",
            "Os meses de outubro, novembro e dezembro concentram o pico de vendas nos três "
            "anos analisados (2010, 2011 e 2012), refletindo o comportamento sazonal típico "
            "do varejo americano com as compras de fim de ano e Black Friday."
        ),
    ]

    for i, (tit, desc) in enumerate(insights):
        by = 0.57 - i * 0.24
        ax_b = fig.add_axes([0.04, by, 0.006, 0.19])
        ax_b.set_facecolor(AZUL); ax_b.axis("off")
        ax = fig.add_axes([0.052, by, 0.905, 0.19])
        ax.set_facecolor(FUNDO); ax.axis("off")
        ax.text(0.02, 0.88, tit, va="top", fontsize=11, fontweight="bold", color=CINZA)
        ax.text(0.02, 0.55, desc, va="top", fontsize=9.5, color=CINZA_L, linespacing=1.45, wrap=True)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 8 — Resultados e Insights (parte 2) ────────────────────────────────
def slide_insights_2(pdf):
    fig = nova_figura()
    cabecalho(fig, "6. Resultados e Insights", "Padrões identificados na análise exploratória — parte 2")
    rodape(fig, 8)

    insights = [
        (
            "Promoções (Markdowns) têm impacto relevante apenas em semanas com feriado",
            "O Total_Markdown apresenta correlação positiva com vendas principalmente em "
            "semanas de feriado. Em semanas comuns, o efeito promocional é diluído por "
            "outros fatores como sazonalidade e tipo de loja, sem impacto claro no volume."
        ),
        (
            "As 10 melhores lojas concentram cerca de 30% da receita total",
            "A distribuição de vendas entre as 45 lojas é altamente assimétrica. "
            "As 10 lojas de maior receita acumulam ~30% de todo o faturamento, "
            "indicando que decisões sobre essas lojas têm peso desproporcional nos resultados."
        ),
        (
            "Temperatura apresenta relação fraca com o volume agregado de vendas",
            "A análise por Faixa de Temperatura (Frio/Agradável/Quente) não revelou "
            "correlação forte com as vendas no nível da loja. O efeito climático parece ser "
            "mediado pela sazonalidade e varia por categoria de produto dentro de cada departamento."
        ),
    ]

    for i, (tit, desc) in enumerate(insights):
        by = 0.57 - i * 0.24
        ax_b = fig.add_axes([0.04, by, 0.006, 0.19])
        ax_b.set_facecolor(AZUL); ax_b.axis("off")
        ax = fig.add_axes([0.052, by, 0.905, 0.19])
        ax.set_facecolor(FUNDO); ax.axis("off")
        ax.text(0.02, 0.88, tit, va="top", fontsize=11, fontweight="bold", color=CINZA)
        ax.text(0.02, 0.55, desc, va="top", fontsize=9.5, color=CINZA_L, linespacing=1.45)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SLIDE 9 — Conclusão ───────────────────────────────────────────────────────
def slide_conclusao(pdf):
    fig = nova_figura()
    ax_left = fig.add_axes([0, 0, 0.38, 1])
    ax_left.set_facecolor(AZUL); ax_left.axis("off")
    fig.add_axes([0.378, 0, 0.004, 1]).set_facecolor(AZUL_E)
    plt.gca().axis("off")

    fig.text(0.04, 0.83, "Conclusões", color=BRANCO, fontsize=22, fontweight="bold", va="top")
    fig.text(0.04, 0.73, "Grupo 6  ·  PUC  ·  2025", color="#AECBF0", fontsize=10, va="top")

    fig.text(0.04, 0.57, "Entregas do projeto", color="#AECBF0", fontsize=9.5,
             fontweight="bold", va="top")
    entregas = [
        "Pipeline completo de dados (Python)",
        "Dataset tratado com 25 variáveis",
        "2 dashboards interativos (Dash)",
        "6 insights documentados",
        "Relatório técnico (PDF)",
        "Esta apresentação",
    ]
    for i, e in enumerate(entregas):
        fig.text(0.05, 0.50 - i * 0.067, f"✓  {e}", color=BRANCO, fontsize=9.5, va="top")

    fig.text(0.44, 0.83, "O que foi alcançado", color=AZUL, fontsize=13,
             fontweight="bold", va="top")

    conclusoes = [
        ("Pipeline reproduzível",
         "Aquisição, integração, limpeza e engenharia de 9 novas variáveis\n"
         "documentadas em script único e reutilizável."),
        ("Dashboards interativos",
         "Dois painéis em Python Dash com design acadêmico, filtros reativos\n"
         "e 11 visualizações cobrindo diferentes ângulos dos dados."),
        ("Insights de negócio",
         "Seis achados sobre sazonalidade, concentração de receita, impacto\n"
         "de feriados e efetividade de promoções no varejo Walmart."),
        ("Boas práticas",
         "Projeto organizado em pastas (data/, scripts/, reports/, assets/)\n"
         "com README, requirements.txt e controle de versão (Git)."),
    ]

    for i, (tit_c, desc_c) in enumerate(conclusoes):
        by = 0.68 - i * 0.155
        ax_b = fig.add_axes([0.44, by, 0.005, 0.12])
        ax_b.set_facecolor(AZUL); ax_b.axis("off")
        fig.text(0.455, by + 0.10, tit_c, va="top", fontsize=10, color=AZUL, fontweight="bold")
        fig.text(0.455, by + 0.056, desc_c, va="top", fontsize=9, color=CINZA, linespacing=1.4)

    rodape(fig, 9)
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs("reports", exist_ok=True)
    caminho = "reports/apresentacao.pdf"
    with PdfPages(caminho) as pdf:
        slide_capa(pdf)
        slide_base_dados(pdf)
        slide_caracterizacao(pdf)
        slide_preparacao(pdf)
        slide_integracao(pdf)
        slide_dashboards(pdf)
        slide_insights_1(pdf)
        slide_insights_2(pdf)
        slide_conclusao(pdf)
    print(f"Gerado: {caminho}  (9 slides)")


if __name__ == "__main__":
    main()
