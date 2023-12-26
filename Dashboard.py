import streamlit as st
import requests
import pandas as pd 
import plotly.express as px
import formatacao_dataframe as fmt_df
import fabrica_graficos as graf

df = pd.read_csv('results.csv')
df = fmt_df.traduz_paises(df)
teams = df['home_team'].unique()
teams.sort()
teams = teams.tolist()



#Streamlit
st.set_page_config(layout="wide")
st.title('Análise histórica dos confrontos entre seleções')

st.write("Explore um tesouro de informações sobre os confrontos históricos entre seleções em um único lugar! \
        Nosso dataframe abrange uma extensa coleção de resultados de todos os jogos já disputados entre times nacionais, \
        oferecendo uma visão ampla e detalhada sobre as batalhas futebolísticas ao longo do tempo. Convido você a mergulhar \
        nesse universo de dados, descobrindo padrões, estatísticas e curiosidades fascinantes sobre as partidas entre as seleções. \
        Venha explorar e desvendar os segredos contidos nessas informações!")

with st.sidebar:
    st.title("Filtros")
    default_index = teams.index('Brasil')
    option_team = st.selectbox('Selecione uma seleção:',(teams), index=default_index)
    df_country, df_home, df_away = fmt_df.formata_df(df, option_team)
    competicoes = df_country['tournament'].unique()
    competicoes = ['Todas Competições'] + list(competicoes)
    option = st.selectbox('Selecione uma competição:',(competicoes))

if option == 'Todas Competições':
    df_tournament = df_country
    df_tournament_home = df_home
    df_tournament_away = df_away
else:
    df_tournament = df_country[df_country['tournament'] == option]
    df_tournament_home = df_home[df_home['tournament'] == option]
    df_tournament_away = df_away[df_away['tournament'] == option]

df_opponent = fmt_df.resultado_por_oponente(df_tournament)
df_opponent_home = fmt_df.resultado_por_oponente(df_tournament_home)
df_opponent_away = fmt_df.resultado_por_oponente(df_tournament_away)

# DESEMPENHO GERAL 
st.write("")
st.write("")
st.write("")
st.subheader(f"{option_team} - Desempenho Geral em {option}")
geral, casa, visitante = st.tabs(['Geral', 'Casa', 'Fora'])
with geral:
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Jogos', df_tournament.shape[0])
    with col2:
        st.metric('Vitórias', df_tournament[df_tournament["result"] == 'Vitória'].shape[0])
    with col3:
        st.metric('Empates', df_tournament[df_tournament["result"] == 'Empate'].shape[0])
    with col4:
        st.metric('Derrotas', df_tournament[df_tournament["result"] == 'Derrota'].shape[0])

with casa:
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Jogos', df_tournament_home.shape[0])
    with col2:
        st.metric('Vitórias', df_tournament_home[df_tournament_home["result"] == 'Vitória'].shape[0])
    with col3:
        st.metric('Empates', df_tournament_home[df_tournament_home["result"] == 'Empate'].shape[0])
    with col4:
        st.metric('Derrotas', df_tournament_home[df_tournament_home["result"] == 'Derrota'].shape[0])

with visitante:
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Jogos', df_tournament_away.shape[0])
    with col2:
        st.metric('Vitórias', df_tournament_away[df_tournament_away["result"] == 'Vitória'].shape[0])
    with col3:
        st.metric('Empates', df_tournament_away[df_tournament_away["result"] == 'Empate'].shape[0])
    with col4:
        st.metric('Derrotas', df_tournament_away[df_tournament_away["result"] == 'Derrota'].shape[0])

#Desempenho por Década
st.write("")
st.write("")
st.write("")
st.subheader(f"{option_team} - Desempenho por Década em {option}")
geral, casa, visitante = st.tabs(['Geral', 'Casa', 'Fora'])
with geral:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.graf_jogos_decada(df_tournament))
        st.pyplot(graf.gols_marcados_sofridos_decada(df_tournament))
    with col2:
        st.pyplot(graf.graf_aproveitamento_decada(df_tournament))
        st.write("")
        st.write("")
        st.pyplot(graf.media_gols(df_tournament))

with casa:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.graf_jogos_decada(df_tournament_home))
        st.pyplot(graf.gols_marcados_sofridos_decada(df_tournament_home))
    with col2:
        st.pyplot(graf.graf_aproveitamento_decada(df_tournament_home))
        st.write("")
        st.write("")
        st.pyplot(graf.media_gols(df_tournament_home))
        

with visitante:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.graf_jogos_decada(df_tournament_away))
        st.pyplot(graf.gols_marcados_sofridos_decada(df_tournament_away))
    with col2:
        st.pyplot(graf.graf_aproveitamento_decada(df_tournament_away))
        st.write("")
        st.write("")
        st.pyplot(graf.media_gols(df_tournament_away))

st.subheader(f"{option_team} - Desempenho Geral por Adversário em {option}")
geral, casa, visitante = st.tabs(['Geral', 'Casa', 'Fora'])

with geral:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.desempenho_por_adversario(df_opponent))
    with col2:
        st.pyplot(graf.gols_por_adversario(df_tournament))

with casa:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.desempenho_por_adversario(df_opponent_home))
    with col2:
        st.pyplot(graf.gols_por_adversario(df_tournament_home))

with visitante:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(graf.desempenho_por_adversario(df_opponent_away))
    with col2:
        st.pyplot(graf.gols_por_adversario(df_tournament_away))

