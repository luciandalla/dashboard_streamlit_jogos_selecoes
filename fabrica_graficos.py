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

def gols_marcados_sofridos_decada(df):
    decades_summary_goals = df.groupby('decade').agg({'GP': 'sum', 'GS': 'sum'}).reset_index()

    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))


    bar_width = 0.4
    bar_positions = range(len(decades_summary_goals))
    bars1 = ax1.bar(bar_positions, decades_summary_goals['GP'], width=bar_width, label='Gols Marcados', align='center', color='#009688')
    bars2 = ax1.bar([pos + bar_width for pos in bar_positions], decades_summary_goals['GS'], width=bar_width, label='Gols Sofridos', align='center', color='#F06292')
    ax1.set_title('Quantidade de gols marcados e gols sofridos', loc='left', fontsize=13, pad=10)
    ax1.set_xlabel('Década', fontsize=11, color="#424242")
    ax1.set_ylabel('')
    ax1.xaxis.set_tick_params(labelcolor="#424242")
    ax1.yaxis.set_tick_params(labelcolor="#424242")

    if (decades_summary_goals['GP'].max() > decades_summary_goals['GS'].max()):
        y_scale = decades_summary_goals["GP"].max() + 30
    else:
        y_scale = decades_summary_goals["GS"].max() + 30    

    ax1.set_ylim(0, y_scale)
    ax1.set_xticks([pos + bar_width / 2 for pos in bar_positions])
    ax1.set_yticklabels([])
    ax1.set_xticklabels(decades_summary_goals['decade'])
    ax1.legend(fontsize=9)
    ax1.set_frame_on(False)

    for bar1, bar2 in zip(bars1, bars2):
        ax1.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(), str(bar1.get_height()), ha='center', va='bottom', fontsize=9)
        ax1.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(), str(bar2.get_height()), ha='center', va='bottom', fontsize=9)

    return fig

def media_gols(df):
    num_games_decade = df["decade"].value_counts().sort_index().reset_index()
    num_games_decade.columns = ['Década', 'Quantidade']

    decades_summary_goals = df.groupby('decade').agg({'GP': 'sum', 'GS': 'sum'}).reset_index()
    
    # Merge dos DataFrames pela coluna 'decade'
    decades_summary_goals = pd.merge(decades_summary_goals, num_games_decade, left_on='decade', right_on='Década')

    decades_summary_goals['MGP'] = decades_summary_goals['GP'] / decades_summary_goals['Quantidade']
    decades_summary_goals['MGS'] = decades_summary_goals['GS'] / decades_summary_goals['Quantidade']
    decades_summary_goals['MGP'] = decades_summary_goals['MGP'].round(2)
    decades_summary_goals['MGS'] = decades_summary_goals['MGS'].round(2)

    #Gráfico
    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))

    sns.lineplot(data=decades_summary_goals, x="decade", y="MGP", lw=2, color="#009688", ax=ax1, marker="o", label="Média de Gols Marcados")
    sns.lineplot(data=decades_summary_goals, x="decade", y="MGS", lw=2, color="#F06292", ax=ax1, marker="o", label="Média de Gols Sofridos")

    ax1.set_title('Média de Gols Marcados e Sofridos por Jogo ', loc='left', fontsize=13, pad=10)
    ax1.set_xlabel('Década', fontsize=11, color="#424242")
    ax1.set_ylabel('Média de Gols', fontsize=11, color="#424242")
    ax1.xaxis.set_tick_params(labelcolor="#424242")
    ax1.yaxis.set_tick_params(labelcolor="#424242")
    ax1.set_facecolor('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_color("#757575")
    ax1.spines['left'].set_color("#757575")
    ax1.grid(False)

    if (decades_summary_goals['MGP'].max() > decades_summary_goals['MGS'].max()):
        y_scale = decades_summary_goals["MGP"].max() + 2
    else:
        y_scale = decades_summary_goals["MGS"].max() + 20   

    ax1.set_ylim(0, y_scale)
    ax1.legend(fontsize=9)

    for index, row in decades_summary_goals.iterrows():
        ax1.text(row['decade'], row['MGP'] + 0.1, str(round(row['MGP'], 2)), color="#009688", ha='center', fontsize=10)
        ax1.text(row['decade'], row['MGS'] + 0.1, str(round(row['MGS'], 2)), color="#F06292", ha='center', fontsize=10)

    return fig


def desempenho_por_adversario(df):

    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))

    ax1.barh(df.index, df["Percentual Vitórias"], color = "#009688", height=0.7, label="Vitórias")
    ax1.barh(df.index, df["Percentual Empates"], color="#78909C", left=df["Percentual Vitórias"], height=0.7, label="Empates")
    ax1.barh(df.index, df["Percentual Derrotas"], color="#F06292", left=df["Percentual Vitórias"] + df["Percentual Empates"], height=0.7, label="Derrotas")

    ax1.set_title("Aproveitamento contra os 10 adversários com maior número de confrontos", loc='left', fontsize=13, pad=10)
    ax1.set_ylabel('')
    ax1.set_xticklabels([])
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_frame_on(False)

    for container in ax1.containers:
        labels = [f'{valor.get_width():.1f}%' if valor.get_width() != 0 else '' for valor in container]
        ax1.bar_label(container, label_type='center', labels=labels, size=10, color="white", fontweight='bold')

    return fig

def gols_por_adversario(df):
    #Dados Gráfico2
    opponent_summary_goals = df.groupby('opponent').agg({'GP': 'sum', 'GS': 'sum'}).reset_index()
    opponent_summary_goals['Número de Partidas'] = df.groupby('opponent').size().reset_index(name='Número de Partidas')['Número de Partidas']
    opponent_summary_goals = opponent_summary_goals.sort_values(by='Número de Partidas', ascending=False).head(10)
    opponent_summary_goals = opponent_summary_goals.sort_values(by='GP', ascending=False)

    #Gráfico
    sns.set_theme()
    sns.set_palette('Dark2')
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 5))

    bar_width = 0.4

    for i in range(len(opponent_summary_goals)):
        ax1.barh(i + bar_width, opponent_summary_goals['GS'].iloc[i], bar_width, label='Gols Sofridos', color="#F06292")
        ax1.barh(i + bar_width * 2, opponent_summary_goals['GP'].iloc[i], bar_width, label='Gols Marcados', color="#009688")
        ax1.text(opponent_summary_goals['GS'].iloc[i], i + bar_width, f'{opponent_summary_goals["GS"].iloc[i]}', 
                 va='center', ha='left', color='black', fontsize=7)
        ax1.text(opponent_summary_goals['GP'].iloc[i], i + bar_width * 2, f'{opponent_summary_goals["GP"].iloc[i]}', 
                 va='center', ha='left', color='black', fontsize=7)

    ax1.set_yticks([i + bar_width * 1.5 for i in range(len(opponent_summary_goals))])
    ax1.set_yticklabels(opponent_summary_goals['opponent'])
    ax1.set_xlim(0, max(opponent_summary_goals['GP'].max(), opponent_summary_goals['GS'].max()) + 20)  
    ax1.set_xlabel('')
    ax1.set_xticks([])
    ax1.set_title('Gols contra os 10 adversários com maior número de confrontos', loc='left', fontsize=13, pad=10)

    # Adicionando apenas uma vez cada rótulo para a legenda
    ax1.legend(['Gols Sofridos', 'Gols Marcados'], loc='upper right', fontsize=9)
    
    ax1.set_frame_on(False)

    return fig
    