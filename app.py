import pandas as pd
import streamlit as st

"""
Teste
"""

dados = pd.read_csv('laptop_prices.csv')
st.header('Tabela Original')
st.dataframe(dados)

dados_nulos_separados = dados[dados.isna().any(axis=1)]['Company'].str.split(',', expand=True)
new_column_names = ['Company','Product','TypeName','Inches','Ram','OS','Weight','Price_euros','Screen','ScreenW','ScreenH','Touchscreen','IPSpanel','RetinaDisplay','CPU_company','CPU_freq','CPU_model','PrimaryStorage','SecondaryStorage','PrimaryStorageType','SecondaryStorageType','GPU_company','GPU_model']
dados_nulos_separados.rename(columns=dict(zip(dados_nulos_separados.columns, new_column_names)), inplace=True)
dados_total = pd.concat([dados, dados_nulos_separados], axis=0, ignore_index=True).dropna(ignore_index=True)

st.header("Data Frame Informação")
st.dataframe(dados_total.info())

#Convertendo os tipos de dados
dados_total['OS'] = dados_total['OS'].astype(str)

dados_total[['Inches', 'Ram', 'Weight', 'Price_euros', 'ScreenW', 'ScreenH', 'CPU_freq', 'PrimaryStorage']] = dados_total[['Inches', 'Ram', 'Weight', 'Price_euros', 'ScreenW', 'ScreenH', 'CPU_freq', 'PrimaryStorage']].astype(float)

#Filtrando os dados
dados_completo = dados_total[['Company', 'Product', 'TypeName', 'Ram', 'OS', 'Price_euros', 'CPU_company', 'CPU_freq', 'CPU_model', 'PrimaryStorage', 'PrimaryStorageType', 'GPU_model']]

st.header('DataFrame filtrado')
st.dataframe(dados_completo)

#calcula media de preço com rellação ao SO
media_preco = dados_completo.groupby('OS')['Price_euros'].median()

st.header("Media de Preço por Sistema Operacional")
st.bar_chart(media_preco)


st.header('Pesquisa de laptop por preço')

preco_minimo, preco_maximo = st.slider(
    'Selecione o intervalo de preços',
    min_value=dados_completo['Price_euros'].min(),
    max_value=dados_completo['Price_euros'].max(),
    value=(dados_completo['Price_euros'].min(), dados_completo['Price_euros'].max())
)

# Filtrar os dados
dados_filtrados = dados_completo[(dados_completo['Price_euros'] >= preco_minimo) & (dados_completo['Price_euros'] <= preco_maximo)].sort_values(by='Price_euros', ascending=True)

# Exibir os resultados
st.dataframe(dados_filtrados)

#Contagem de laptops por sistema operacional
st.write(dados_completo['OS'].value_counts())
