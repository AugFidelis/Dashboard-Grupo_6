"""
Tarefa 7 — Análise Exploratória dos Dados
Tarefa 8 — Identificação e Formulação dos Insights

Dataset: Walmart Sales Forecast (2010–2012)
"""
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)

# Este script foi usado para entender a base antes de montar o dashboard.
# Ele imprime os principais numeros que depois viraram graficos e insights.

# ── 1. Carregamento ───────────────────────────────────────────────────────────
df = pd.read_csv("data/processed/walmart_limpo.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 60)
print("DIAGNÓSTICO GERAL DO DATASET")
print("=" * 60)
print(f"Registros: {len(df):,}")
print(f"Colunas:   {df.shape[1]}")
print(f"Periodo:   {df['Date'].min().date()} a {df['Date'].max().date()}")
print(f"Lojas:     {df['Store'].nunique()} (IDs {df['Store'].min()}–{df['Store'].max()})")
print(f"Deptos:    {df['Dept'].nunique()} distintos")
print(f"\nTipos de loja:")
# Primeiro e feito um diagnostico geral para saber tamanho da base,
# periodo analisado, quantidade de lojas e perfil dos tipos de loja.
print(df.groupby("Type").agg(
    n_lojas=("Store", "nunique"),
    tamanho_medio=("Size", "mean"),
    registros=("Store", "count")
).round(0))

# ── 2. Estatísticas descritivas ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("ESTATÍSTICAS DESCRITIVAS — Weekly_Sales")
print("=" * 60)
# Estatisticas basicas ajudam a entender escala, media e dispersao das vendas.
stats = df["Weekly_Sales"].describe()
print(stats.apply(lambda x: f"$ {x:,.0f}"))

# ── 3. Análise temporal ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("VENDAS POR ANO")
print("=" * 60)
# Aqui o desempenho agregado de cada ano e comparado para ver a tendencia geral.
por_ano = df.groupby("Ano")["Weekly_Sales"].agg(
    total="sum", media="mean", mediana="median"
).round(0)
print(por_ano.map(lambda x: f"$ {x:,.0f}"))

# ── 4. Análise de feriados ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("IMPACTO DOS FERIADOS")
print("=" * 60)
# Cada feriado e comparado com a media geral para medir o impacto percentual.
media_geral = df["Weekly_Sales"].mean()
por_feriado = df.groupby("Nome_Feriado")["Weekly_Sales"].agg(
    media="mean", total="sum", n_semanas="count"
).reset_index()
por_feriado["variacao_pct"] = (
    (por_feriado["media"] - media_geral) / media_geral * 100
).round(1)
por_feriado = por_feriado.sort_values("media", ascending=False)
print(por_feriado.to_string(index=False))

# ── 5. Análise por tipo de loja ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("DESEMPENHO POR TIPO DE LOJA")
print("=" * 60)
# Esta tabela mostra se o tipo de loja influencia faturamento, media e tamanho.
por_tipo = df.groupby("Type").agg(
    total_vendas=("Weekly_Sales", "sum"),
    media_semanal=("Weekly_Sales", "mean"),
    n_lojas=("Store", "nunique"),
    tamanho_medio=("Size", "mean"),
).round(0)
por_tipo["share_pct"] = (
    por_tipo["total_vendas"] / por_tipo["total_vendas"].sum() * 100
).round(1)
print(por_tipo)

# ── 6. Top departamentos ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TOP 10 DEPARTAMENTOS POR FATURAMENTO TOTAL")
print("=" * 60)
# O ranking de departamentos mostra onde esta concentrada a maior parte das vendas.
top_depts = (
    df.groupby("Dept")["Weekly_Sales"].sum()
    .sort_values(ascending=False)
    .head(10)
)
for dept, val in top_depts.items():
    print(f"  Dept {dept:>3}: $ {val:>15,.0f}")

# ── 7. Impacto das markdowns ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("IMPACTO DAS MARKDOWNS (PROMOÇÕES)")
print("=" * 60)
# As cinco colunas MarkDown sao somadas para criar uma leitura unica de promocao.
df["Total_Markdown"] = df[["MarkDown1", "MarkDown2", "MarkDown3",
                             "MarkDown4", "MarkDown5"]].sum(axis=1)
df["Com_Markdown"] = df["Total_Markdown"] > 0
comp = df.groupby("Com_Markdown")["Weekly_Sales"].agg(
    media="mean", n="count"
).round(0)
comp.index = ["Sem promoção", "Com promoção"]
print(comp)
dif_pct = (
    (comp.loc["Com promoção", "media"] - comp.loc["Sem promoção", "media"])
    / comp.loc["Sem promoção", "media"] * 100
)
print(f"\nDiferença com promoção: {dif_pct:+.1f}%")

# ── 8. Formulação dos insights ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("INSIGHTS FORMULADOS")
print("=" * 60)
# Esta lista organiza os principais achados em frases prontas para a apresentacao.
insights = [
    ("Insight 1 [Dashboard 1]",
     "Ação de Graças eleva as vendas em +41% acima da média geral "
     "($ 24.547 vs $ 17.484). É o evento comercial de maior impacto no período."),
    ("Insight 2 [Dashboard 1]",
     "Natal registra vendas ABAIXO da média (-7.5%, $ 16.089). "
     "Isso indica que as compras natalinas ocorrem principalmente em novembro, "
     "concentradas na semana da Ação de Graças (Black Friday)."),
    ("Insight 3 [Dashboard 1]",
     "Lojas Tipo A concentram ~65% do faturamento total, apesar de representarem "
     "50% das lojas. Seu tamanho médio (194.201 m²) é quase o dobro das Tipo B."),
    ("Insight 4 [Dashboard 1]",
     "A venda média semanal caiu de $ 17.824 (2010) para $ 17.110 (2012), "
     "uma queda acumulada de ~4% — pode refletir pressão econômica do período."),
    ("Insight 5 [Dashboard 2]",
     "Promoções (MarkDowns) estão associadas a vendas ~1.9% superiores. "
     "O efeito é mais pronunciado em meses de campanha (nov/dez)."),
    ("Insight 6 [Dashboard 2]",
     "Os departamentos 92 e 95 lideram o faturamento (mais de $ 300M cada). "
     "São categorias de produtos sazonais de alto giro."),
]

for titulo, texto in insights:
    print(f"\n  [{titulo}]")
    print(f"  {texto}")

print("\n" + "=" * 60)
print("Análise concluída.")
