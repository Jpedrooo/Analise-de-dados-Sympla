import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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



##Criando os graficos das analises

##Evolução temporal das vendas
vendas_mensais = (
    df.groupby(df['dt_venda'].dt.to_period('M'))['vr_venda']
    .sum()
    .reset_index()
)

vendas_mensais['dt_venda'] = vendas_mensais['dt_venda'].dt.to_timestamp()


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')  
ax.set_facecolor('#ebebeb')         


ax.plot(vendas_mensais['dt_venda'], vendas_mensais['vr_venda'],
        color='#6ecaf5', linewidth=3, marker='o')


for x, y in zip(vendas_mensais['dt_venda'], vendas_mensais['vr_venda']):
    ax.text(x, y + (y * 0.02), f"R$ {y/1_000_000:.2f}",
            ha='center', va='bottom', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Evolução Mensal das Vendas', fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Data da Venda', fontsize=11, color='#19325c')
ax.set_ylabel('Valor Total das Vendas (R$)', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.5)


plt.tight_layout()



#Total de vendas por estado
vendas_por_estado = (
    df.groupby('nm_localidade_estado')['vr_venda']
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')  
ax.set_facecolor('#ebebeb')         


ax.barh(vendas_por_estado['nm_localidade_estado'],
        vendas_por_estado['vr_venda'],
        color='#6ecaf5')


for index, value in enumerate(vendas_por_estado['vr_venda']):
    ax.text(value + (value * 0.01), index,
            f"R$ {value/1_000_000:.2f}",
            va='center', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Vendas Totais por Estado', fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Valor Total das Vendas (R$)', fontsize=11, color='#19325c')
ax.set_ylabel('Estado', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()



#Variação de vendas por estado com relação ao mês anterior
vendas_mensais = (
    df.groupby([df['nm_localidade_estado'], df['dt_venda'].dt.to_period('M')])['vr_venda']
    .sum()
    .reset_index()
)


vendas_mensais['pct_change'] = vendas_mensais.groupby('nm_localidade_estado')['vr_venda'].pct_change() * 100


vendas_mensais['dt_venda'] = vendas_mensais['dt_venda'].dt.to_timestamp()


ultimo_mes = vendas_mensais['dt_venda'].max()
df_mes_atual = vendas_mensais[vendas_mensais['dt_venda'] == ultimo_mes]


df_mes_atual = df_mes_atual.sort_values('pct_change', ascending=True)


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')
ax.set_facecolor('#ebebeb')


ax.barh(df_mes_atual['nm_localidade_estado'], df_mes_atual['pct_change'], color='#6ecaf5')


for index, value in enumerate(df_mes_atual['pct_change']):
    sinal = '+' if value >= 0 else ''
    ax.text(value + (1 if value >= 0 else -1), index,
            f"{sinal}{value:.2f}%",
            va='center', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Variação Percentual das Vendas por Estado (Último Mês)',
             fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Variação Percentual (%)', fontsize=11, color='#19325c')
ax.set_ylabel('Estado', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()





#Variação de vendas por categoria de negocio com relação ao mês anterior
vendas_mensais_cat = (
    df.groupby([df['nm_evento_classificacao_negocio'], df['dt_venda'].dt.to_period('M')])['vr_venda']
    .sum()
    .reset_index()
)


vendas_mensais_cat['pct_change'] = vendas_mensais_cat.groupby('nm_evento_classificacao_negocio')['vr_venda'].pct_change() * 100


vendas_mensais_cat['dt_venda'] = vendas_mensais_cat['dt_venda'].dt.to_timestamp()


ultimo_mes = vendas_mensais_cat['dt_venda'].max()
df_mes_atual_cat = vendas_mensais_cat[vendas_mensais_cat['dt_venda'] == ultimo_mes]


df_mes_atual_cat = df_mes_atual_cat.sort_values('pct_change', ascending=True)


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')
ax.set_facecolor('#ebebeb')


ax.barh(df_mes_atual_cat['nm_evento_classificacao_negocio'], df_mes_atual_cat['pct_change'], color='#6ecaf5')


for index, value in enumerate(df_mes_atual_cat['pct_change']):
    sinal = '+' if value >= 0 else ''
    ax.text(value + (1 if value >= 0 else -1), index,
            f"{sinal}{value:.2f}%",
            va='center', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Variação Percentual das Vendas por Categoria de Negócio (Último Mês)',
             fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Variação Percentual (%)', fontsize=11, color='#19325c')
ax.set_ylabel('Categoria de Negócio', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()




#Variação de vendas por categoria de negocio com relação ao ano anterior
df['ano'] = df['dt_venda'].dt.year


vendas_anuais_cat = (
    df.groupby(['nm_evento_classificacao_negocio', 'ano'])['vr_venda']
    .sum()
    .reset_index()
)


vendas_2033_2034 = vendas_anuais_cat[vendas_anuais_cat['ano'].isin([2033, 2034])]


vendas_pivot = vendas_2033_2034.pivot(index='nm_evento_classificacao_negocio', columns='ano', values='vr_venda')
vendas_pivot['pct_change'] = ((vendas_pivot[2034] - vendas_pivot[2033]) / vendas_pivot[2033]) * 100


vendas_pivot = vendas_pivot.dropna(subset=['pct_change']).sort_values('pct_change', ascending=True)


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')
ax.set_facecolor('#ebebeb')


ax.barh(vendas_pivot.index, vendas_pivot['pct_change'], color='#6ecaf5')


for index, value in enumerate(vendas_pivot['pct_change']):
    sinal = '+' if value >= 0 else ''
    ax.text(value + (1 if value >= 0 else -1), index,
            f"{sinal}{value:.2f}%",
            va='center', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Variação Percentual das Vendas por Categoria de Negócio (2034 vs 2033)',
             fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Variação Percentual (%)', fontsize=11, color='#19325c')
ax.set_ylabel('Categoria de Negócio', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()





#Variação de vendas por estado com relação ao ano anterior
vendas_anuais_estado = (
    df.groupby(['nm_localidade_estado', 'ano'])['vr_venda']
    .sum()
    .reset_index()
)


vendas_2033_2034 = vendas_anuais_estado[vendas_anuais_estado['ano'].isin([2033, 2034])]


vendas_pivot_estado = vendas_2033_2034.pivot(index='nm_localidade_estado', columns='ano', values='vr_venda')


vendas_pivot_estado['pct_change'] = ((vendas_pivot_estado[2034] - vendas_pivot_estado[2033]) / vendas_pivot_estado[2033]) * 100


vendas_pivot_estado = vendas_pivot_estado.dropna(subset=['pct_change']).sort_values('pct_change', ascending=True)


plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#ebebeb')
ax.set_facecolor('#ebebeb')


ax.barh(vendas_pivot_estado.index, vendas_pivot_estado['pct_change'], color='#6ecaf5')


for index, value in enumerate(vendas_pivot_estado['pct_change']):
    sinal = '+' if value >= 0 else ''
    ax.text(value + (1 if value >= 0 else -1), index,
            f"{sinal}{value:.2f}%",
            va='center', color='#19325c', fontsize=10, fontweight='bold')


ax.set_title('Variação Percentual das Vendas por Estado (2034 vs 2033)',
             fontsize=14, fontweight='bold', color='#19325c')
ax.set_xlabel('Variação Percentual (%)', fontsize=11, color='#19325c')
ax.set_ylabel('Estado', fontsize=11, color='#19325c')


ax.tick_params(colors='#19325c', labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

