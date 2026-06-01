# Dashboard Walmart — Grupo 6

Projeto final de análise de dados com Python e Dash.  
Tema: **Análise de Vendas do Walmart (2010–2012)**

## Dataset

| Arquivo | Registros | Descrição |
|---------|-----------|-----------|
| `train - Walmart Sales Forecast.csv` | 421.570 | Vendas semanais por loja e departamento |
| `features - Walmart Sales Forecast.csv` | 8.190 | Dados econômicos e climáticos por loja/semana |
| `stores - Walmart Sales Forecast.csv` | 45 | Tipo e tamanho de cada loja |

Fonte: Kaggle — Walmart Recruiting - Store Sales Forecasting

## Estrutura do Projeto

```
Dashboard-Grupo_6/
├── data/
│   ├── raw/                  # Arquivos originais (não modificados)
│   └── processed/
│       └── walmart_limpo.csv # Dataset integrado e tratado (274.153 registros)
├── scripts/
│   ├── preparacao_dados.py   # Tarefas 2, 4, 5 e 6: aquisição, integração, limpeza e transformação
│   └── analise_exploratoria.py  # Tarefa 7 e 8: EDA e insights
├── app.py                    # Dashboards 1 e 2 em Dash
├── requirements.txt
└── README.md
```

## Como executar

```bash
# 1. Criar ambiente virtual (se necessário)
python -m venv .venv

# 2. Ativar o ambiente
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. (Opcional) Reprocessar os dados
python scripts/preparacao_dados.py

# 5. Rodar a análise exploratória
python scripts/analise_exploratoria.py

# 6. Iniciar o dashboard
python app.py
# Acesse: http://127.0.0.1:8050
```

## Dashboards

### Dashboard 1 — Visão Geral (Executivo)
- 5 cards de KPIs: faturamento total, venda média, lojas, loja campeã, registros
- Evolução mensal das vendas (2010–2012)
- Comparativo de faturamento por tipo de loja
- Impacto de feriados nas vendas vs média geral
- Ranking das Top 10 lojas

### Dashboard 2 — Exploração Interativa
- **3 filtros**: Ano (checklist), Tipo de Loja (checklist), Faixa de Temperatura (dropdown)
- **5 visualizações interativas** via callbacks:
  1. Evolução temporal por tipo de loja
  2. Venda média por feriado
  3. Top 15 departamentos por faturamento
  4. Boxplot de distribuição por tipo de loja
  5. Vendas com e sem promoção por mês

## Pipeline de Ciência de Dados

```
Aquisição → Integração → Limpeza → Transformação → EDA → Insights → Dashboard
(T2)         (T4)         (T5)       (T6)            (T7)   (T8)       (T9–T12)
```

## Principais Insights

1. **Ação de Graças +41%**: maior evento comercial do período
2. **Natal abaixo da média (-8%)**: compras concentradas em novembro
3. **Lojas Tipo A = 65% do faturamento** com metade das unidades
4. **Queda de 4% na venda média** de 2010 a 2012
5. **Promoções elevam vendas em +1.9%**, efeito mais forte em nov/dez
6. **Departamentos 92 e 95** lideram com mais de R$300M cada
