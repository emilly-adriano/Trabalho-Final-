import streamlit as st
import requests
import pandas as pd
import plotly.express as px

data = {
    "produto": [
        "Açucar Native Orgânico Dourado 1kg",
        "Açucar Itaja 1KG Organico Demerara",
        "Açúcar Native Orgânico Claro 1kg",
        "Açucar Cristal Itaja 1kg Organico",
        "Bebida De Aveia Nude Organico S/ Gluten 1L",
        "Bebida De Aveia Nude Organico Baunilha 1L",
        "Bebida De Aveia Nude Organico Integral 1L",
        "Bebida De Aveia Nude Organico Cacau 1L",
        "Achocolatado Orgânico Em Pó Instantâneo Native 400G",
        "Chá Mate Poder da Terra Organico Limão 1L",
        "Chá Mate Poder da Terra Organico Pessego 1L",
        "Cereal Corn Flakes Native Organico 300g",
        "Açucar Tia Sonia 400g Organico Demerara",
        "Chá Mate Poder Da Terra Organico Tradicional 1L",
        "Açucar Native 250g Organico Sache",
        "Sorbet Orgânico Açaí Eco Fresh Pote 1,02kg",
        "Vinho Chileno Rosé Meio Seco Orgânico Reserva Adobe Valle del Rapel Garrafa 750ml",
        "Hortelã Orgânico Caisp",
        "Espinafre Orgânico Caisp 180g",
    ],
    "precos": [
        8.79, 6.48, 6.99, 5.99, 19.9, 19.9, 19.9, 19.9, 19.8,
        9.9, 9.9, 16.98, 11.98, 9.9, 9.99, 42.98, 76.8, 0.0, 0.0,
    ],
    "agrup1": [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
}

df = pd.DataFrame(data)

from sqlalchemy import create_engine 
engine = create_engine('sqlite:///banco.db', echo=True)

try:
    df.to_sql('dados', con=engine, if_exists='replace', index=False)
    print("Tabela 'dados' criada e dados inseridos com sucesso!")
except Exception as e:
    print("Erro ao criar a tabela no banco de dados:", e)

try:
    df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
    print("Dados lidos do banco com sucesso:")
    print(df_lido)
except Exception as e:
    print("Erro ao ler os dados do banco:", e)


st.write("Dados carregados do banco de dados", df_lido)

st.write("Histograma de Preços")
fig_hist = px.histogram(df_lido.precos) # type: ignore
st.plotly_chart(fig_hist)

st.write("Gráfico de pizza, preços")
fig_pie = px.pie(df_lido, "precos") # type: ignore
st.plotly_chart(fig_pie)

st.write("Barra de Preços")
fig_bar = px.bar(df_lido, 'precos') # type: ignore
st.plotly_chart(fig_bar)

st.write("Barra de Preços por Produto")
fig_bar2 = px.bar(df_lido, x='precos', y='produto', color='agrup1') # type: ignore
st.plotly_chart(fig_bar2)

st.write("Scatter de Preços por Produto")
fig_scar = px.scatter(df_lido, x='precos', y='produto', color='agrup1') # type: ignore
st.plotly_chart(fig_scar)

st.write("Histograma de Preços por Produto")
fig_hist2 = px.histogram(df_lido, x='produto', y='precos', color='agrup1') # type: ignore
st.plotly_chart(fig_hist2)

media = df_lido['precos'].mean()
mediana = df_lido['precos'].median()
desvio_padrao = df_lido['precos'].std()

st.write(f'Média dos Preços: {media:.2f}')
st.write(f'Mediana dos Preços: {mediana:.2f}')
st.write(f'Desvio Padrão dos Preços: {desvio_padrao:.2f}')
