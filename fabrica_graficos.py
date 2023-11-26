import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Gráfico - Número de jogos por década
def graf_jogos_decada(df):
    num_games_decade = df["decade"].value_counts().sort_index().reset_index()
    num_games_decade.columns = ['Década', 'Quantidade']

    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))

    sns.lineplot(data=num_games_decade, x='Década', y='Quantidade', lw=2, color="#009688", ax=ax1, marker="o", label="Quantidade de Jogos")
    ax1.set_title('Quantidade de Jogos Realizados', loc='left', fontsize=13, pad=10)
    ax1.set_xlabel('Década', fontsize=11, color="#424242")
    ax1.set_ylabel('Quantidade de Jogos', fontsize=11, color="#424242")
    ax1.xaxis.set_tick_params(labelcolor="#424242")
    ax1.yaxis.set_tick_params(labelcolor="#424242")
    ax1.set_facecolor('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_color("#757575")
    ax1.spines['left'].set_color("#757575")
    ax1.grid(False)
    ax1.legend(fontsize=9)
    ax1.set_ylim(0, num_games_decade['Quantidade'].max() + 20)

    for index, row in num_games_decade.iterrows():
        ax1.text(row['Década'], row['Quantidade'] + 1, f'{row["Quantidade"]}', ha='center', va='bottom', fontsize=10, color="#009688")

    return fig

def graf_aproveitamento_decada(df):
    decade_results = pd.DataFrame()
    decade_results['Vitória'] = (df['result'] == 'Vitória').groupby(df['decade']).sum()
    decade_results['Derrota'] = (df['result'] == 'Derrota').groupby(df['decade']).sum()
    decade_results['Empate'] = (df['result'] == 'Empate').groupby(df['decade']).sum()
    decade_results['Número de Jogos'] = df.groupby('decade')['result'].count()
    decade_results = decade_results.fillna(0)
    decade_results['Percentual Vitórias'] = (decade_results['Vitória'] / decade_results['Número de Jogos']) * 100
    decade_results['Percentual Derrotas'] = (decade_results['Derrota'] / decade_results['Número de Jogos']) * 100
    decade_results['Percentual Empates'] = (decade_results['Empate'] / decade_results['Número de Jogos']) * 100
    decade_results['Percentual Vitórias'] = decade_results['Percentual Vitórias'].round(2)
    decade_results['Percentual Derrotas'] = decade_results['Percentual Derrotas'].round(2)
    decade_results['Percentual Empates'] = decade_results['Percentual Empates'].round(2)

    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))

    ax1.barh(decade_results.index, decade_results["Percentual Vitórias"], color = "#009688", height=8.5, label="Vitórias")
    ax1.barh(decade_results.index, decade_results["Percentual Empates"], color="#78909C", left=decade_results["Percentual Vitórias"], height=8.5, label="Empates")
    ax1.barh(decade_results.index, decade_results["Percentual Derrotas"], color="#F06292", left=decade_results["Percentual Vitórias"] + decade_results["Percentual Empates"], height=8.5, label="Derrotas")

    ax1.set_title("Percentual de Vitórias, Empates e Derrotas", loc='left', fontsize=13, pad=10)
    ax1.set_ylabel('')
    ax1.set_yticks(decade_results.index)
    ax1.set_yticklabels(decade_results.index, fontsize=9)
    ax1.set_xticklabels([])
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_frame_on(False)

    for container in ax1.containers:
        labels = [f'{valor.get_width():.1f}%' if valor.get_width() != 0 else '' for valor in container]
        ax1.bar_label(container, label_type='center', labels=labels, size=10, color="white", fontweight='bold')

    return fig