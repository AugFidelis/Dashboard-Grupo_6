import pandas as pd
import os

def preparar_dados():
    # Verifica se as pastas existem, se não ele cria automaticamente
    os.makedirs('data/processed', exist_ok=True)

    # 2. Aquisição de dados (Lendo os CSVs originais)
    df_train = pd.read_csv('data/raw/train - Walmart Sales Forecast.csv')
    df_features = pd.read_csv('data/raw/features - Walmart Sales Forecast.csv')
    df_stores = pd.read_csv('data/raw/stores - Walmart Sales Forecast.csv')

    # 3. Integração de Dados (O Merge)
    # Primeiro juntamos as vendas com os detalhes das lojas usando a coluna 'Store'
    df_merged = df_train.merge(df_stores, on='Store', how='left')
    
    # Depois juntamos o resultado com os dados climáticos/econômicos (Features)
    # Usamos 'Store', 'Date' e 'IsHoliday' como chave para evitar colunas duplicadas
    df_merged = df_merged.merge(df_features, on=['Store', 'Date', 'IsHoliday'], how='left')

    # 4. Limpeza e Tratamento dos Dados
    # Os únicos valores nulos encontrados foram nas colunas MarkDown1 a MarkDown5 (Descontos).
    # Quando é nulo, significa que não houve promoção na semana, então é preenchido com 0.
    colunas_markdown = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    df_merged[colunas_markdown] = df_merged[colunas_markdown].fillna(0)

    # 4.2 Remoção de Inconsistências (Descontos Negativos)
    # Se o sistema registrou um desconto negativo (erro lógico), o valor é mudado pra 0.
    for col in colunas_markdown:
        df_merged.loc[df_merged[col] < 0, col] = 0

    # 4.3 Remoção de Inconsistências (Registros Duplicados)
    df_merged = df_merged.drop_duplicates()

    # 5. Transformação de Dados (Criando novas variáveis)
    # Convertendo a coluna Date de texto para o formato de data do python
    df_merged['Date'] = pd.to_datetime(df_merged['Date'], format='%Y-%m-%d')
    
    # Criando colunas separadas para facilitar a filtragem no dashboard depois
    df_merged['Ano'] = df_merged['Date'].dt.year
    df_merged['Mes'] = df_merged['Date'].dt.month

    # Transformando a temperatura (em fahrenheit) em categorias lógicas para facilitar filtragem também, e deixar mais fácil de mexer no dashboard ao invés de ter que colocar a temperatura manualmente
    limites_temperatura = [-100, 45, 75, 200] # Divide entre -100 a 45, 45 a 75 e 75 a 200, -100 e 200 são números extremos que jamais aconteceriam normalmente
    rotulos_temperatura = ['Frio', 'Agradável', 'Quente']
    df_merged['Faixa_Temperatura'] = pd.cut(df_merged['Temperature'], bins=limites_temperatura, labels=rotulos_temperatura)

    # Cria uma função para mapear o mês para o nome do feriado se existir um no mês
    def nomear_feriado(linha):
        if not linha['IsHoliday']:
            return 'Sem Feriado'
        elif linha['Mes'] == 2:
            return 'Super Bowl'
        elif linha['Mes'] == 9:
            return 'Dia do Trabalho'
        elif linha['Mes'] == 11:
            return 'Ação de Graças'
        elif linha['Mes'] == 12:
            return 'Natal'
        else:
            return 'Outro Feriado'

    # Aplica a função linha por linha criando a nova coluna
    df_merged['Nome_Feriado'] = df_merged.apply(nomear_feriado, axis=1)

    # 6. Exportação
    df_merged.to_csv('data/processed/walmart_limpo.csv', index=False)
    
    print(f"Total de linhas processadas: {df_merged.shape[0]}")
    print(f"Total de colunas prontas para análise: {df_merged.shape[1]}")
    
    # Faz com que o terminal não esconda colunas com '...'
    pd.set_option('display.max_columns', None)

    print(df_merged.head())


if __name__ == "__main__":
    preparar_dados()