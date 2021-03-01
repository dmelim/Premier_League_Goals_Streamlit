import streamlit as st
import pandas as pd
import base64

st.title('Explora os melhores marcadores da Premier League')

st.markdown("""
Esta app faz um webscraping de estatísticas dos melhores marcadores da Premier League!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [statbunker.com/](https://www.statbunker.com/competitions/TopGoalScorers?comp_id=667).
""")

ids = { 
    "PL2120" : "667"
    ,"PL2019" : "639","PL1918" : "614", "PL1817" : "586","PL1716" : "556"}
x = list(ids.keys())
st.sidebar.header('Interface de Input do Utilizador')
selected_year = st.sidebar.selectbox ('Anos', x)

@st.cache
def load_data(a):
    url = "https://www.statbunker.com/competitions/TopGoalScorers?comp_id=" + str(a)
    html = pd.read_html(url, header = 0)
    df = html[0]
    playerstats = df
    return playerstats
playerstats = load_data(ids.get(selected_year))

sorted_unique_team = sorted(playerstats.Clubs.unique())
selected_team = st.sidebar.multiselect('Club', sorted_unique_team, sorted_unique_team)

df_selected_team = playerstats[(playerstats.Clubs.isin(selected_team))]

st.header('Estatísticas das equipas selecionadas')
st.write('Dimensão: ' + str(df_selected_team.shape[0]) + ' filas e ' + str(df_selected_team.shape[1]) + ' colunas.')
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

clubesgolos = {
}

clubes = playerstats.Clubs.unique()

for clube in clubes:
    clubesgolos.update({clube : 0})

for index, row in playerstats.iterrows():
    clubesgolos.update({row['Clubs'] : clubesgolos.get(row['Clubs']) + row['Goals']})

if st.button('Gráfico de Barras'):
    st.header('Gráfico de Barras (Golos por equipa)')
    chart_data = pd.DataFrame(
    clubesgolos.values(),
    clubesgolos.keys(),
    columns = ["Golos"])  
    st.bar_chart(chart_data, 400, 800,True)