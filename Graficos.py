import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



sns.set_theme(style="whitegrid")


df = pd.read_csv("Base_de_Vendas_para_Teste_Tecnico_Dados__20250904.csv", sep=';', quotechar='"')




def grafico_linha(df, x, y, titulo, xlabel, ylabel):
    """Gera gráfico de linha formatado"""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#ebebeb')
    ax.set_facecolor('#ebebeb')

    ax.plot(df[x], df[y], color='#6ecaf5', linewidth=3, marker='o')

    for xi, yi in zip(df[x], df[y]):
        ax.text(xi, yi + (yi * 0.02), f"R$ {yi/1_000_000:.2f}",
                ha='center', va='bottom', color='#19325c', fontsize=10, fontweight='bold')

    ax.set_title(titulo, fontsize=14, fontweight='bold', color='#19325c')
    ax.set_xlabel(xlabel, fontsize=11, color='#19325c')
    ax.set_ylabel(ylabel, fontsize=11, color='#19325c')
    ax.tick_params(colors='#19325c', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def grafico_barh(df, x, y, titulo, xlabel, ylabel, percentual=False):
    """Gera gráfico horizontal formatado (pode mostrar % ou R$)"""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#ebebeb')
    ax.set_facecolor('#ebebeb')

    ax.barh(df[y], df[x], color='#6ecaf5')

    for index, value in enumerate(df[x]):
        if percentual:
            texto = f"{'+' if value >= 0 else ''}{value:.2f}%"
        else:
            texto = f"R$ {value/1_000_000:.2f}"
        ax.text(value + (1 if percentual else value * 0.01), index,
                texto, va='center', color='#19325c', fontsize=10, fontweight='bold')

    ax.set_title(titulo, fontsize=14, fontweight='bold', color='#19325c')
    ax.set_xlabel(xlabel, fontsize=11, color='#19325c')
    ax.set_ylabel(ylabel, fontsize=11, color='#19325c')
    ax.tick_params(colors='#19325c', labelsize=10)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



# Análises anuais
def grafico_variacao_anual(df, coluna_grupo, titulo_dimensao):
   
    df['ano'] = df['dt_venda'].dt.year

    
    vendas_anuais = (
        df.groupby([coluna_grupo, 'ano'])['vr_venda']
        .sum()
        .reset_index()
    )

    
    anos = sorted(vendas_anuais['ano'].unique())[-2:]

    
    vendas_pivot = vendas_anuais[vendas_anuais['ano'].isin(anos)].pivot(
        index=coluna_grupo, columns='ano', values='vr_venda'
    )

    
    vendas_pivot['pct_change'] = ((vendas_pivot[anos[1]] - vendas_pivot[anos[0]]) / vendas_pivot[anos[0]]) * 100

    
    vendas_pivot = vendas_pivot.dropna(subset=['pct_change']).sort_values('pct_change', ascending=True)
    
    grafico_barh(
        vendas_pivot.reset_index(),
        'pct_change',
        coluna_grupo,
        f'Variação Percentual das Vendas por {titulo_dimensao} ({anos[1]} vs {anos[0]})',
        'Variação Percentual (%)',
        titulo_dimensao,
        percentual=True
    )
    

    

