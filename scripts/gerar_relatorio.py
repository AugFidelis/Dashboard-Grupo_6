# -*- coding: utf-8 -*-
import matplotlib
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

plt.rcParams["font.family"] = "DejaVu Sans"

W, H = 8.27, 11.69
AZUL     = "#1A56A0"
AZUL_C   = "#EBF1FA"
CINZA    = "#444444"
CINZA_L  = "#888888"
FUNDO    = "#F5F5F5"
BRANCO   = "#FFFFFF"
AMARELO  = "#D4900A"
AMARELO_C = "#FFF8E8"


def nova_pagina():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(BRANCO)
    return fig

def cab(fig, secao, titulo):
    ax = fig.add_axes([0, 0.940, 1, 0.060])
    ax.set_facecolor(AZUL); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.text(0.04, 0.52, f"{secao}  —  {titulo}", color=BRANCO, fontsize=10.5,
            fontweight="bold", va="center")
    ax.text(0.96, 0.52, "Grupo 6", color="#AECBF0", fontsize=9, va="center", ha="right")

def rod(fig, num):
    ax = fig.add_axes([0, 0, 1, 0.038])
    ax.set_facecolor(FUNDO); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.text(0.04, 0.5, "Análise de Vendas Walmart  ·  Grupo 6  ·  PUC", color=CINZA_L, fontsize=7.5, va="center")

def t1(fig, y, num, texto):
    ax = fig.add_axes([0.06, y - 0.004, 0.005, 0.028])
    ax.set_facecolor(AZUL); ax.axis("off")
    fig.text(0.072, y, f"{num}. {texto}", fontsize=13, fontweight="bold", color=CINZA, va="top")
    return y - 0.048

def t2(fig, y, texto):
    fig.text(0.06, y, texto, fontsize=10.5, fontweight="bold", color=AZUL, va="top")
    return y - 0.032

def wrap(s, n=90):
    words = s.split(); lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).lstrip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def txt(fig, y, s, fs=10, cor=CINZA, esp=0.020, indent=0.06):
    ls = wrap(s) if isinstance(s, str) else s
    for i, l in enumerate(ls):
        fig.text(indent, y - i*esp, l, fontsize=fs, color=cor, va="top")
    return y - len(ls)*esp

def sep(fig, y):
    ax = fig.add_axes([0.06, y, 0.88, 0.002])
    ax.set_facecolor("#DDDDDD"); ax.axis("off")
    return y - 0.014

def blt(fig, y, items, fs=10, esp=0.025, indent=0.06):
    for i, item in enumerate(items):
        fig.text(indent,        y - i*esp, "●", fontsize=5.5, color=AZUL, va="top")
        fig.text(indent+0.022, y - i*esp, item, fontsize=fs, color=CINZA, va="top")
    return y - len(items)*esp

def blt_exp(fig, y, items, fs=10, indent=0.06, gap=0.012):
    for label, desc in items:
        fig.text(indent,        y, "●", fontsize=5.5, color=AZUL, va="top")
        fig.text(indent+0.022, y, label, fontsize=fs, color=CINZA, fontweight="bold", va="top")
        y -= 0.022
        for l in wrap(desc, 88):
            fig.text(indent+0.022, y, l, fontsize=fs-0.5, color=CINZA_L, va="top")
            y -= 0.019
        y -= gap
    return y

def tabela(fig, y, cols, rows, cx, cw, rh=0.026):
    for j,(h,x,w) in enumerate(zip(cols,cx,cw)):
        ax = fig.add_axes([x, y, w-0.005, rh])
        ax.set_facecolor(AZUL); ax.axis("off")
        ha = "left" if j==0 else "center"; px = 0.04 if ha=="left" else 0.5
        ax.text(px, 0.5, h, ha=ha, va="center", color=BRANCO, fontsize=8.5, fontweight="bold")
    y -= rh
    for i,row in enumerate(rows):
        cor = AZUL_C if i%2==0 else BRANCO
        for j,(cell,x,w) in enumerate(zip(row,cx,cw)):
            ax = fig.add_axes([x, y, w-0.005, rh])
            ax.set_facecolor(cor)
            for sp_ in ax.spines.values(): sp_.set_edgecolor("#CCCCCC"); sp_.set_linewidth(0.5)
            ax.axis("off")
            ha = "left" if j==0 else "center"; px = 0.04 if ha=="left" else 0.5
            ax.text(px, 0.5, cell, ha=ha, va="center", fontsize=8.5, color=CINZA)
        y -= rh
    return y

def insight_box(fig, y, titulo, linhas, h=0.20):
    fig.add_axes([0.06, y-h, 0.007, h]).set_facecolor(AZUL)
    plt.gca().axis("off")
    ax = fig.add_axes([0.072, y-h, 0.868, h])
    ax.set_facecolor(FUNDO); ax.axis("off")
    ax.text(0.015, 0.93, titulo, va="top", fontsize=10.5, fontweight="bold", color=CINZA)
    esp_ax = 0.15
    for j,l in enumerate(linhas):
        ax.text(0.015, 0.67 - j*esp_ax, l, va="top", fontsize=9.5, color=CINZA_L)
    return y - h - 0.018


# ── CAPA ─────────────────────────────────────────────────────────────────────
def pagina_capa(pdf):
    fig = nova_pagina()
    ax = fig.add_axes([0, 0.60, 1, 0.40]); ax.set_facecolor(AZUL); ax.axis("off")

    fig.text(0.08, 0.95, "Relatório de Estudo", color="#AECBF0", fontsize=11, va="top")
    fig.text(0.08, 0.89, "Análise de Vendas Walmart", color=BRANCO, fontsize=22,
             fontweight="bold", va="top")
    fig.text(0.08, 0.82, "Walmart Store Sales Forecasting — Kaggle", color="#AECBF0",
             fontsize=12, va="top")
    fig.text(0.08, 0.74,
             "Pipeline de dados, dashboards interativos e insights sobre o comportamento\n"
             "de vendas em 45 lojas norte-americanas no período fev/2010 – out/2012.",
             color="#AECBF0", fontsize=10, va="top", linespacing=1.5)

    fig.text(0.08, 0.54, "Grupo 6", color=CINZA, fontsize=12, fontweight="bold", va="top")
    fig.text(0.08, 0.49, "Pontifícia Universidade Católica — PUC  ·  2025", color=CINZA_L,
             fontsize=10, va="top")

    fig.add_axes([0.06, 0.43, 0.88, 0.003]).set_facecolor(AZUL)
    plt.gca().axis("off")

    kpis = [("421.570","registros"), ("45","lojas"), ("81","departamentos"), ("25","variáveis")]
    for i,(v,l) in enumerate(kpis):
        ax_k = fig.add_axes([0.06+i*0.225, 0.24, 0.20, 0.14])
        ax_k.set_facecolor(AZUL_C)
        for sp_ in ax_k.spines.values(): sp_.set_edgecolor(AZUL); sp_.set_linewidth(1)
        ax_k.axis("off")
        ax_k.text(0.5, 0.78, l, ha="center", va="center", fontsize=8, color=AZUL, fontweight="bold")
        ax_k.text(0.5, 0.34, v, ha="center", va="center", fontsize=18, color=CINZA, fontweight="bold")

    fig.text(0.08, 0.20, "Tecnologias:", color=CINZA_L, fontsize=9, va="top")
    fig.text(0.08, 0.16, "Python  ·  Pandas  ·  Plotly Dash  ·  Matplotlib", color=CINZA,
             fontsize=10, va="top", fontweight="bold")
    fig.text(0.08, 0.10, "Período analisado:", color=CINZA_L, fontsize=9, va="top")
    fig.text(0.08, 0.06, "Fevereiro de 2010  a  Outubro de 2012  (143 semanas)", color=CINZA,
             fontsize=10, va="top")

    ax_f = fig.add_axes([0, 0, 1, 0.035]); ax_f.set_facecolor(FUNDO); ax_f.axis("off")
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 1 — BASE DE DADOS ──────────────────────────────────────────────────
def pagina_base_dados(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 1", "Base de Dados Escolhida")
    rod(fig, 2)

    y = 0.905
    y = t1(fig, y, "1", "Base de Dados Escolhida")

    y = t2(fig, y, "1.1  Identificação do Conjunto de Dados")
    y = txt(fig, y,
        "O conjunto de dados utilizado é o Walmart Store Sales Forecasting, disponibilizado "
        "publicamente na plataforma Kaggle como parte de uma competição de previsão de séries "
        "temporais. Os dados compreendem registros semanais de 45 lojas do Walmart nos Estados "
        "Unidos, cobrindo 143 semanas entre fevereiro de 2010 e outubro de 2012. A base é "
        "composta por três arquivos CSV complementares, descritos na tabela abaixo.")
    y -= 0.015

    y = tabela(fig, y,
        ["Arquivo", "Linhas", "Colunas", "Principais variáveis"],
        [
            ["train.csv",    "421.570", "5",  "Store, Dept, Date, Weekly_Sales, IsHoliday"],
            ["features.csv", "8.190",   "12", "Temperature, Fuel_Price, MarkDown1–5, CPI, Unemployment"],
            ["stores.csv",   "45",      "3",  "Store, Type (A/B/C), Size (área em ft²)"],
        ],
        [0.06, 0.25, 0.35, 0.46], [0.18, 0.09, 0.10, 0.48])
    y -= 0.022

    y = sep(fig, y)
    y = t2(fig, y, "1.2  Justificativa da Escolha")
    y = txt(fig, y,
        "A escolha da base foi motivada por três critérios principais: volume, diversidade "
        "analítica e relevância prática do contexto.")
    y -= 0.008

    y = blt_exp(fig, y, [
        ("Volume e qualidade dos dados:",
         "Com 421.570 registros semanais e cobertura de três anos consecutivos, a base oferece "
         "densidade estatística suficiente para análises de tendência, sazonalidade e impacto de "
         "eventos externos, sem necessidade de interpolação ou enriquecimento externo."),
        ("Diversidade de dimensões analíticas:",
         "A presença simultânea de variáveis de vendas, fatores climáticos (temperatura), "
         "indicadores macroeconômicos (CPI, desemprego, preço do combustível) e campanhas "
         "promocionais (MarkDown1 a MarkDown5) viabiliza análises multidimensionais e cruzamentos "
         "entre contexto econômico e comportamento de consumo."),
        ("Relevância e aplicabilidade prática:",
         "Os dados provêm de contexto competitivo real — uma das maiores redes de varejo do mundo "
         "— com potencial direto de aplicação em decisões de gestão de estoque, planejamento de "
         "campanhas e alocação de recursos por departamento e tipo de loja."),
    ], gap=0.016)
    y -= 0.010

    y = sep(fig, y)
    y = t2(fig, y, "1.3  Escopo Temporal e Geográfico")
    txt(fig, y,
        "O recorte temporal (2010–2012) captura três ciclos sazonais completos, incluindo eventos "
        "relevantes como a recuperação pós-crise de 2008, períodos inflacionários e variações no "
        "preço do combustível. As 45 lojas estão distribuídas em diferentes regiões dos EUA, "
        "com três perfis distintos (tipos A, B e C) que diferem em porte e mix de produtos.")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 2 — CARACTERIZAÇÃO ─────────────────────────────────────────────────
def pagina_caracterizacao(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 2", "Caracterização dos Dados Originais")
    rod(fig, 3)

    y = 0.905
    y = t1(fig, y, "2", "Caracterização dos Dados Originais")

    y = t2(fig, y, "2.1  Estrutura dos Arquivos")
    y = txt(fig, y,
        "Antes de qualquer transformação, o conjunto é composto por três entidades "
        "independentes. O arquivo de vendas (train.csv) é o arquivo central, contendo uma "
        "linha por combinação de loja, departamento e semana. Os outros dois fornecem "
        "atributos de contexto para enriquecimento do dataset principal.")
    y -= 0.014

    y = tabela(fig, y,
        ["Arquivo", "Granularidade", "Variável-chave", "Tipo de dado dominante"],
        [
            ["train.csv",    "Loja × Dept × Semana", "Weekly_Sales (R$)", "Numérico contínuo"],
            ["features.csv", "Loja × Semana",        "Temperature (°F)",  "Numérico + Binário"],
            ["stores.csv",   "Por loja (45 linhas)", "Type, Size",        "Categórico + Inteiro"],
        ],
        [0.06, 0.26, 0.49, 0.67], [0.19, 0.22, 0.17, 0.27])
    y -= 0.022

    y = t2(fig, y, "2.2  Variável-Alvo e Cobertura")
    y = txt(fig, y,
        "A variável-alvo é Weekly_Sales, que representa a receita semanal por departamento em "
        "cada loja, expressa em dólares americanos. Os valores variam de negativos (devoluções) "
        "a mais de US$ 700.000 por semana para os maiores departamentos das lojas tipo A. "
        "O período cobre de 05/02/2010 a 26/10/2012, com 143 semanas de observações.")
    y -= 0.018

    y = sep(fig, y)
    y = t2(fig, y, "2.3  Problemas Identificados Antes do Tratamento")
    y = txt(fig, y,
        "A inspeção inicial do dataset revelou cinco categorias de problemas que precisavam "
        "ser endereçados antes da análise exploratória:")
    y -= 0.008

    y = blt(fig, y, [
        "Valores ausentes (NaN): MarkDown1 a MarkDown5 com alta proporção de valores nulos",
        "Inconsistências numéricas: descontos negativos registrados nas colunas de MarkDown",
        "Tipo de dado incorreto: coluna Date armazenada como string, não como datetime",
        "Ausência de variáveis temporais: sem Ano, Mês, Trimestre ou Estação derivados",
        "Feriados sem identificação: IsHoliday é binária, sem nome do evento correspondente",
    ], esp=0.028)
    y -= 0.020

    y = sep(fig, y)
    y = t2(fig, y, "2.4  Distribuição das Vendas por Tipo de Loja")
    txt(fig, y,
        "As lojas do tipo A (22 unidades, maior porte) concentram aproximadamente 70% de toda "
        "a receita do período. As 17 lojas do tipo B e as 6 do tipo C, embora mais numerosas "
        "em relação ao tipo C, possuem volume individual significativamente menor. "
        "Essa assimetria é um padrão estrutural relevante para a interpretação de qualquer "
        "análise agregada: médias simples tendem a subestimar o desempenho das lojas tipo A.")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 3 — PREPARAÇÃO E TRATAMENTO ────────────────────────────────────────
def pagina_preparacao(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 3", "Preparação e Tratamento dos Dados")
    rod(fig, 4)

    y = 0.905
    y = t1(fig, y, "3", "Preparação e Tratamento dos Dados")
    y = txt(fig, y,
        "O tratamento dos dados foi implementado no script preparacao_dados.py em quatro "
        "etapas: correção de valores ausentes, eliminação de inconsistências, conversão "
        "de tipos e engenharia de novos atributos.")
    y -= 0.015

    y = t2(fig, y, "3.1  Tratamento de Valores Ausentes")
    y = txt(fig, y,
        "MarkDown1–5 tinham NaN em semanas sem promoção, preenchidos com 0 via fillna(0). "
        "Ausência de promoção equivale semanticamente a desconto zero.")
    y -= 0.015

    y = t2(fig, y, "3.2  Correção de Inconsistências Numéricas")
    y = txt(fig, y,
        "MarkDown negativos substituídos por zero via df.loc[df[col] < 0, col] = 0. "
        "Desconto negativo é erro de registro — semanticamente inválido.")
    y -= 0.015

    y = t2(fig, y, "3.3  Remoção de Duplicatas e Padronização")
    y = txt(fig, y,
        "drop_duplicates() garantiu unicidade de cada combinação loja × departamento × semana. "
        "Date convertida de string para datetime com pd.to_datetime().")
    y -= 0.015

    y = t2(fig, y, "3.4  Padronização Semântica de Feriados")
    y = txt(fig, y,
        "A coluna IsHoliday (True/False) foi enriquecida com o nome do evento pelo mês: "
        "Super Bowl (fev), Dia do Trabalho (set), Ação de Graças (nov), Natal (dez).")
    y -= 0.018

    y = sep(fig, y)
    y = t2(fig, y, "3.5  Engenharia de Atributos — 9 Novas Variáveis")
    y = txt(fig, y,
        "A engenharia de atributos criou nove variáveis para viabilizar os filtros dos "
        "dashboards e enriquecer o poder analítico do dataset processado:")
    y -= 0.010

    y = tabela(fig, y,
        ["Variável", "Tipo", "Descrição / Lógica de criação"],
        [
            ["Ano",               "Inteiro",    "Extraído de Date com .dt.year"],
            ["Mes",               "Inteiro",    "Extraído de Date com .dt.month"],
            ["Trimestre",         "Categórico", "Q1 a Q4 derivado do Mês: (Mes-1)//3 + 1"],
            ["Estacao",           "Categórico", "Inverno/Primavera/Verão/Outono por mês"],
            ["Faixa_Temperatura", "Categórico", "Frio (<45°F), Agradável (45–75°F), Quente (>75°F)"],
            ["Nome_Feriado",      "Categórico", "Super Bowl, Dia do Trabalho, Ação de Graças, Natal"],
            ["Total_Markdown",    "Numérico",   "Soma de MarkDown1 + ... + MarkDown5"],
            ["Tem_Promocao",      "Booleano",   "True se Total_Markdown > 0"],
            ["Porte_Loja",        "Categórico", "Pequena/Média/Grande por percentis 33% e 66% do Size"],
        ],
        [0.06, 0.26, 0.36], [0.19, 0.09, 0.55], rh=0.023)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 4 — INTEGRAÇÃO ─────────────────────────────────────────────────────
def pagina_integracao(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 4", "Integração dos Dados")
    rod(fig, 5)

    y = 0.905
    y = t1(fig, y, "4", "Integração dos Dados")

    y = t2(fig, y, "4.1  Estratégia de Integração")
    y = txt(fig, y,
        "Os três arquivos CSV representam entidades relacionadas por chaves comuns, "
        "de forma análoga a tabelas em um banco de dados relacional. A estratégia adotada "
        "foi o left join em duas etapas sequenciais usando o método pd.DataFrame.merge() "
        "do Pandas, garantindo que todos os 421.570 registros de vendas de train.csv "
        "fossem preservados integralmente no dataset final.")
    y -= 0.018

    y = t2(fig, y, "4.2  Etapa 1 — Junção com Dados de Lojas")
    y = txt(fig, y,
        "O arquivo train.csv foi combinado com stores.csv utilizando a coluna Store como "
        "chave de junção (left join). Como stores.csv contém apenas 45 linhas (uma por loja), "
        "o resultado é uma expansão lateral do dataset de vendas: as variáveis Type e Size "
        "são adicionadas a cada registro, resultando em 421.570 linhas × 7 colunas. "
        "Não há perda de registros nessa operação.")
    y -= 0.018

    y = t2(fig, y, "4.3  Etapa 2 — Junção com Dados de Contexto")
    y = txt(fig, y,
        "O resultado da Etapa 1 foi combinado com features.csv usando uma chave composta "
        "de três colunas: Store, Date e IsHoliday. A chave tripla foi necessária porque "
        "features.csv possui uma linha por loja por semana, enquanto train.csv possui "
        "múltiplas linhas por semana (uma por departamento). Sem a chave composta, "
        "o merge geraria duplicatas. O resultado adiciona 9 variáveis de contexto: "
        "Temperature, Fuel_Price, MarkDown1–5, CPI e Unemployment.")
    y -= 0.022

    # Diagrama de integração compacto
    fig.text(0.06, y, "Representação do processo:", color=CINZA_L, fontsize=9, va="top")
    y -= 0.010

    dy = y - 0.26   # base do diagrama
    dh = 0.22

    def bx_arquivo(x, y2, nome, dims):
        ax_ = fig.add_axes([x, y2, 0.20, 0.09])
        ax_.set_facecolor(AZUL_C)
        for sp_ in ax_.spines.values(): sp_.set_edgecolor(AZUL); sp_.set_linewidth(1.2)
        ax_.axis("off")
        ax_.text(0.5, 0.70, nome, ha="center", fontsize=10, fontweight="bold", color=AZUL)
        ax_.text(0.5, 0.28, dims, ha="center", fontsize=8.5, color=CINZA)

    def bx_merge(x, y2, titulo, chave):
        ax_ = fig.add_axes([x, y2, 0.16, 0.09])
        ax_.set_facecolor(AMARELO_C)
        for sp_ in ax_.spines.values(): sp_.set_edgecolor(AMARELO); sp_.set_linewidth(1.2)
        ax_.axis("off")
        ax_.text(0.5, 0.72, titulo, ha="center", fontsize=9.5, fontweight="bold", color=AMARELO)
        ax_.text(0.5, 0.30, chave, ha="center", fontsize=8, color=CINZA)

    bx_arquivo(0.06, dy+0.13, "train.csv", "421.570 × 5")
    bx_arquivo(0.06, dy+0.01, "stores.csv", "45 × 3")
    bx_merge(0.30, dy+0.07,  "MERGE 1", "on: Store")
    bx_arquivo(0.50, dy,      "features.csv", "8.190 × 12")
    bx_merge(0.53, dy+0.13,  "MERGE 2", "on: Store+Date+IsHoliday")

    ax_f = fig.add_axes([0.75, dy+0.06, 0.18, 0.14])
    ax_f.set_facecolor(AZUL); ax_f.axis("off")
    ax_f.text(0.5, 0.82, "Dataset Final", ha="center", fontsize=9, fontweight="bold", color=BRANCO)
    ax_f.text(0.5, 0.54, "421.570 × 25", ha="center", fontsize=12, fontweight="bold", color=BRANCO)
    ax_f.text(0.5, 0.24, "16 orig. + 9 novas", ha="center", fontsize=8, color="#AECBF0")

    ov = fig.add_axes([0, 0, 1, 1], facecolor="none"); ov.axis("off")
    ov.set_xlim(0,1); ov.set_ylim(0,1)
    setas = [
        (0.26, dy+0.175, 0.30, dy+0.155),
        (0.26, dy+0.055, 0.30, dy+0.110),
        (0.46, dy+0.115, 0.53, dy+0.175),
        (0.60, dy+0.09,  0.60, dy+0.130),
        (0.69, dy+0.175, 0.75, dy+0.150),
    ]
    for tx,ty,hx,hy in setas:
        ov.annotate("", xy=(hx,hy), xytext=(tx,ty),
                    arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.5))

    # resultado visível no diagrama acima

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 5 — DASHBOARDS ─────────────────────────────────────────────────────
def pagina_dashboards(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 5", "Construção dos Dashboards")
    rod(fig, 6)

    y = 0.905
    y = t1(fig, y, "5", "Construção dos Dashboards")
    y = txt(fig, y,
        "Os dashboards foram desenvolvidos em Python com o framework Plotly Dash, que "
        "permite criar aplicações web interativas sem JavaScript. A interface é definida "
        "inteiramente em Python, com gráficos criados via Plotly Express. Os dois painéis "
        "compartilham o mesmo arquivo app.py e são acessados por abas (dcc.Tabs).")
    y -= 0.018

    y = t2(fig, y, "5.1  Dashboard 1 — Visão Geral (Estático)")
    y = txt(fig, y,
        "O primeiro dashboard é um painel executivo sem filtros dinâmicos, projetado para "
        "comunicar rapidamente os principais indicadores do período completo. A organização "
        "segue hierarquia de informação: métricas no topo, seguidas de análises progressivamente "
        "mais detalhadas. Inclui os seguintes elementos:")
    y -= 0.008
    y = blt(fig, y, [
        "4 KPI cards: total vendido, média semanal por loja, melhor loja e semanas com feriado",
        "Callout de insight: destaque visual com análise do impacto médio de feriados nas vendas",
        "Gráfico 1: Evolução mensal das vendas (gráfico de área com marcadores trimestrais)",
        "Gráfico 2: Vendas médias por tipo de loja A, B e C (barras verticais)",
        "Gráfico 3: Comparativo feriados vs. semanas normais com linha de média geral",
        "Gráfico 4: Top 10 lojas por receita acumulada (barras horizontais ordenadas)",
    ], esp=0.027)
    y -= 0.020

    y = sep(fig, y)
    y = t2(fig, y, "5.2  Dashboard 2 — Análise Interativa (Reativa)")
    y = txt(fig, y,
        "O segundo painel permite segmentação dinâmica dos dados via sidebar fixa com cinco "
        "filtros reativos. Cada alteração de filtro aciona callbacks que atualizam todos os "
        "sete gráficos simultaneamente, sem recarregar a página. Os filtros disponíveis são:")
    y -= 0.008
    y = blt(fig, y, [
        "Ano: checklist com seleção múltipla (2010, 2011, 2012)",
        "Tipo de loja: checklist A / B / C",
        "Porte da loja: checklist Pequena / Média / Grande",
        "Faixa de temperatura: dropdown Frio / Agradável / Quente",
        "Estação do ano: dropdown Inverno / Primavera / Verão / Outono",
    ], esp=0.027)
    y -= 0.020

    y = sep(fig, y)
    y = t2(fig, y, "5.3  Decisões de Design e Organização Visual")
    txt(fig, y,
        "O sistema de design é baseado em uma paleta acadêmica com azul (#1A56A0) como "
        "cor de acento e branco como fundo. As fontes IBM Plex Sans (corpo) e IBM Plex Serif "
        "(título) conferem legibilidade e formalidade. A sidebar do Dashboard 2 usa "
        "position: sticky para permanecer visível durante a rolagem. Um template Plotly "
        "customizado (academico) foi registrado globalmente para garantir consistência "
        "visual entre todos os gráficos.")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 6 — INSIGHTS (PARTE 1) ─────────────────────────────────────────────
def pagina_insights_1(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 6", "Resultados e Insights — Parte 1")
    rod(fig, 7)

    y = 0.905
    y = t1(fig, y, "6", "Resultados e Insights")
    y = txt(fig, y,
        "A análise exploratória do dataset processado revelou seis padrões relevantes "
        "sobre o comportamento de vendas. Cada insight foi identificado por agrupamento, "
        "comparação de médias ou distribuição entre categorias.")
    y -= 0.018

    y = insight_box(fig, y,
        "Insight 1 — Feriados elevam as vendas em média 7% acima da média semanal",
        wrap("Semanas com feriados registrados (IsHoliday=True) apresentam vendas "
             "consistentemente superiores à média geral. O efeito é mais pronunciado no "
             "Q4 (out–dez), com Natal e Ação de Graças impulsionando picos que chegam a "
             "12% acima da média. O Super Bowl (fev) apresenta impacto menor mas ainda "
             "positivo, especialmente em lojas próximas a grandes centros urbanos.", 85), h=0.20)

    y = insight_box(fig, y,
        "Insight 2 — Lojas tipo A concentram aproximadamente 70% da receita total",
        wrap("As 22 lojas classificadas como tipo A (maior porte físico, acima do percentil "
             "66 de tamanho) dominam a receita do período. Lojas tipo B e C, apesar de "
             "somarem 23 unidades, contribuem com os 30% restantes. Essa concentração "
             "implica que qualquer análise de tendência agregada é fortemente influenciada "
             "pelo desempenho das lojas tipo A.", 85), h=0.20)

    y = insight_box(fig, y,
        "Insight 3 — Q4 é o trimestre de maior volume em todos os três anos",
        wrap("Os meses de outubro, novembro e dezembro concentram sistematicamente o pico "
             "de vendas nos anos 2010, 2011 e 2012, refletindo o comportamento sazonal "
             "do varejo norte-americano com Black Friday, Cyber Monday e compras natalinas. "
             "O Q1 (jan–mar) apresenta o menor volume, com queda acentuada imediatamente "
             "após o Natal.", 85), h=0.20)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── SEÇÃO 6 — INSIGHTS (PARTE 2) ─────────────────────────────────────────────
def pagina_insights_2(pdf):
    fig = nova_pagina()
    cab(fig, "Seção 6", "Resultados e Insights — Parte 2")
    rod(fig, 8)

    y = 0.905
    y = t2(fig, y, "Continuação — Insights 4, 5 e 6")
    y -= 0.010

    y = insight_box(fig, y,
        "Insight 4 — Promoções (Markdowns) têm impacto relevante apenas em semanas com feriado",
        wrap("A variável Total_Markdown apresenta correlação positiva com vendas "
             "principalmente em semanas de feriado, sugerindo que campanhas promocionais "
             "amplificam o efeito já existente do feriado, mas não geram demanda nova "
             "em semanas comuns. Em semanas normais, o volume de Markdown não se traduz "
             "em aumento proporcional de vendas no agregado.", 85), h=0.20)

    y = insight_box(fig, y,
        "Insight 5 — As 10 melhores lojas respondem por cerca de 30% da receita total",
        wrap("A distribuição de receita entre as 45 lojas é altamente assimétrica. "
             "As 10 lojas de maior faturamento acumulam aproximadamente 30% de toda a "
             "receita do período. Esse nível de concentração indica que estratégias "
             "voltadas especificamente para as lojas de maior volume têm potencial de "
             "impacto desproporcional sobre o resultado consolidado da rede.", 85), h=0.20)

    y = insight_box(fig, y,
        "Insight 6 — Temperatura apresenta relação fraca com o volume agregado de vendas",
        wrap("A análise por Faixa_Temperatura (Frio, Agradável, Quente) não revelou "
             "correlação forte com o volume de vendas no nível da loja. As medianas de "
             "vendas nas três faixas de temperatura são próximas, e as distribuições se "
             "sobrepõem amplamente. O efeito climático pode ser relevante em categorias "
             "específicas de produto (ex.: roupas de inverno, bebidas), mas se dilui "
             "quando a análise é feita no agregado de todos os departamentos.", 85), h=0.20)

    y -= 0.010
    y = sep(fig, y)
    y = t2(fig, y, "Síntese dos Achados")
    txt(fig, y,
        "Os seis insights revelam que o desempenho de vendas no Walmart é fortemente "
        "determinado por três eixos estruturais: sazonalidade (Q4 e feriados), "
        "heterogeneidade do portfólio (tipo e porte das lojas) e concentração de receita "
        "(top 10 lojas). Fatores externos como temperatura e promoções exercem influência "
        "secundária ou mediada pelos eixos primários. Esses achados sugerem que iniciativas "
        "de alta alavancagem devem priorizar as lojas tipo A no período Q4, com atenção "
        "especial ao planejamento de estoque para semanas de feriado.")

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── CONCLUSÃO ─────────────────────────────────────────────────────────────────
def pagina_conclusao(pdf):
    fig = nova_pagina()
    cab(fig, "Conclusão", "Síntese, Limitações e Referências")
    rod(fig, 9)

    y = 0.905
    y = t1(fig, y, "", "Conclusão")
    y = txt(fig, y,
        "Este projeto demonstrou a viabilidade de construir um pipeline completo de análise "
        "de dados — da aquisição à visualização interativa — com ferramentas de código aberto "
        "em Python. O conjunto de dados Walmart Store Sales Forecasting mostrou-se adequado "
        "aos objetivos do projeto: volume suficiente para análise estatística, diversidade "
        "de variáveis para análises multidimensionais e relevância prática para insights "
        "aplicáveis a contextos reais de varejo.")
    y -= 0.022

    y = t2(fig, y, "Contribuições do Projeto")
    y = blt(fig, y, [
        "Pipeline reproduzível de preparação e integração de dados em script único",
        "Dataset enriquecido com 9 novas variáveis de engenharia de atributos",
        "Dashboard 1: painel executivo com 4 KPIs e 4 visualizações estáticas",
        "Dashboard 2: painel interativo com 5 filtros reativos e 7 gráficos dinâmicos",
        "6 insights documentados sobre sazonalidade, concentração e promoções",
    ], esp=0.028)
    y -= 0.022

    y = sep(fig, y)
    y = t2(fig, y, "Limitações")
    y = txt(fig, y,
        "O dataset cobre apenas 2010–2012, limitando a generalização para padrões mais "
        "recentes do varejo. A análise é feita no nível de loja e não de produto individual, "
        "o que impede insights sobre mix de categorias. As variáveis macroeconômicas (CPI, "
        "desemprego) apresentam baixa variação semanal, reduzindo seu poder explicativo "
        "em análises de curto prazo.")
    y -= 0.022

    y = sep(fig, y)
    y = t2(fig, y, "Possibilidades de Melhoria")
    y = blt(fig, y, [
        "Aplicar modelos preditivos (ARIMA, Prophet, XGBoost) para previsão de vendas futuras",
        "Incorporar dados externos como índices de confiança do consumidor e eventos locais",
        "Análise por departamento para identificar categorias mais sensíveis a feriados",
        "Deploy do dashboard em plataforma web (Heroku, Render) para acesso remoto",
    ], esp=0.028)
    y -= 0.022

    y = sep(fig, y)
    y = t2(fig, y, "Referências")
    blt(fig, y, [
        "Kaggle. Walmart Store Sales Forecasting. kaggle.com/c/walmart-recruiting-store-sales-forecasting",
        "McKinney, W. (2022). Python for Data Analysis, 3rd ed. O'Reilly Media.",
        "Plotly Technologies. Dash Documentation. dash.plotly.com",
        "Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering.",
    ], esp=0.028)

    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs("reports", exist_ok=True)
    caminho = "reports/relatorio_estudo.pdf"
    with PdfPages(caminho) as pdf:
        pagina_capa(pdf)
        pagina_base_dados(pdf)
        pagina_caracterizacao(pdf)
        pagina_preparacao(pdf)
        pagina_integracao(pdf)
        pagina_dashboards(pdf)
        pagina_insights_1(pdf)
        pagina_insights_2(pdf)
        pagina_conclusao(pdf)
    print(f"Gerado: {caminho}  (9 páginas)")


if __name__ == "__main__":
    main()
