import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

# Caminho relativo ao arquivo CSV dentro do projeto
caminho_arquivo = os.path.join("medias", "medias_mensais_geo_2020.csv")

st.title("Médias Mensais Regionais e Estaduais - 2020")

try:
    # Ler o arquivo CSV
    df_medias_geo = pd.read_csv(caminho_arquivo)

    # Lista de regiões únicas
    regioes = df_medias_geo['Regiao'].unique()
    meses = sorted(df_medias_geo['Mês'].unique())

    # Seleção interativa de variável
    variaveis = [
        'RADIACAO GLOBAL (Kj/m²)',
        'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'
    ]
    item = st.selectbox("Selecione a variável para visualizar:", variaveis)

    # --- Gráficos por Região (Média Regional) ---
    st.subheader(f"Médias Mensais Regionais de {item} - 2020")
    fig, ax = plt.subplots(figsize=(12, 6))
    for regiao in regioes:
        # Filtra o DataFrame para a região atual
        df_regiao = df_medias_geo[df_medias_geo['Regiao'] == regiao]
        # Calcula a média da variável para cada mês dentro da região
        media_regional = df_regiao.groupby('Mês')[item].mean().reindex(meses)
        ax.plot(media_regional.index, media_regional.values, marker='o', label=regiao)

    ax.set_title(f'Médias Mensais Regionais de {item} - 2020')
    ax.set_xlabel('Mês')
    ax.set_ylabel(item)
    ax.set_xticks(meses)
    ax.grid(True)
    ax.legend(title='Região')
    plt.tight_layout()
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna '{e}' não foi encontrada no arquivo CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro ao gerar os gráficos: {e}")
