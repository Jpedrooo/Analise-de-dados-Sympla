import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import Graficos

df = pd.read_csv("Base_de_Vendas_para_Teste_Tecnico_Dados__20250904.csv", sep=';', quotechar='"')


df.info()
##trnsformando qt_ingresso_por_evento em float64
df['qt_ingresso_por_evento'] = df['qt_ingresso_por_evento'].str.replace(',', '.').str.strip()
df['qt_ingresso_por_evento'] = pd.to_numeric(df['qt_ingresso_por_evento'], errors='coerce')
##trnsformando qt_evento_por_produtor em float64
df['qt_evento_por_produtor'] = df['qt_evento_por_produtor'].str.replace(',', '.').str.strip()
df['qt_evento_por_produtor'] = pd.to_numeric(df['qt_evento_por_produtor'], errors='coerce')
##trnsformando vr_medio_ingresso em float64
df['vr_medio_ingresso'] = df['vr_medio_ingresso'].str.replace(',', '.').str.strip()
df['vr_medio_ingresso'] = pd.to_numeric(df['vr_medio_ingresso'], errors='coerce')
##tranformando a dt_venda em datetime
df['dt_venda'] = pd.to_datetime(df['dt_venda'], errors='coerce')
##transformando o vr_venda em float64(pandas reconhece o padrão ameriacno)
df['vr_venda'] = (
    df['vr_venda']
    .str.replace('.', '', regex=False)  
    .str.replace(',', '.', regex=False) 
    .astype(float)                      
)



print(df.head())
print(df.describe())
print(df.nunique())
##verificando se exite valores duplicados, se sim, quantos são
print(df.duplicated().sum())
##verificando se existe valores nulos, se sim quantos são
print(df.isnull().sum())
##preenchendo os valores nulos com a media da coluna por estado
df['vr_medio_ingresso'] = df['vr_medio_ingresso'].fillna(
    df.groupby('nm_localidade_estado')['vr_medio_ingresso'].transform('mean')
)
df['qt_ingresso_por_evento'] = df['qt_ingresso_por_evento'].fillna(
    df.groupby('nm_localidade_estado')['qt_ingresso_por_evento'].transform('mean')
)



vendas_mensais = (
    df.groupby(df['dt_venda'].dt.to_period('M'))['vr_venda']
    .sum()
    .reset_index()
)
vendas_mensais['dt_venda'] = vendas_mensais['dt_venda'].dt.to_timestamp()


Graficos.grafico_linha(
    vendas_mensais, 
    'dt_venda', 
    'vr_venda',
    'Evolução Mensal das Vendas', 
    'Data da Venda', 
    'Valor Total das Vendas (R$)'
)




vendas_por_estado = (
    df.groupby('nm_localidade_estado')['vr_venda']
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

Graficos.grafico_barh(
    vendas_por_estado, 
    'vr_venda', 
    'nm_localidade_estado',
    'Vendas Totais por Estado', 
    'Valor Total das Vendas (R$)', 
    'Estado'
)

vendas_mensais_estado = (
    df.groupby([df['nm_localidade_estado'], df['dt_venda'].dt.to_period('M')])['vr_venda']
    .sum()
    .reset_index()
)
vendas_mensais_estado['pct_change'] = vendas_mensais_estado.groupby('nm_localidade_estado')['vr_venda'].pct_change() * 100
vendas_mensais_estado['dt_venda'] = vendas_mensais_estado['dt_venda'].dt.to_timestamp()
ultimo_mes = vendas_mensais_estado['dt_venda'].max()
df_mes_atual = vendas_mensais_estado[vendas_mensais_estado['dt_venda'] == ultimo_mes].sort_values('pct_change')

Graficos.grafico_barh(df_mes_atual, 'pct_change', 'nm_localidade_estado',
             'Variação Percentual das Vendas por Estado (Último Mês)',
             'Variação Percentual (%)', 'Estado', percentual=True)


Graficos.grafico_variacao_anual(df, 'nm_evento_classificacao_negocio', 'Categoria de Negócio')
Graficos.grafico_variacao_anual(df, 'nm_localidade_estado', 'Estado')
