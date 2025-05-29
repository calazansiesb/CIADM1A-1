import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

# Caminho relativo ao arquivo CSV dentro do projeto
caminho_arquivo_unificado = os.path.join("medias", "medias_mensais_geo_temp_media_completo.csv")

st.title("Médias Mensais por Estado (2020-2025) diego")

try:
    # Ler o arquivo unificado
    df_unificado = pd.read_csv(caminho_arquivo_unificado)

    # Lista de estados únicos disponíveis
    estados_disponiveis = sorted(df_unificado['Estado'].unique())

    # Seleção interativa do estado
    estado_selecionado = st.selectbox("Selecione o Estado:", estados_disponiveis)

    # Filtrar dados para o estado selecionado
    df_estado = df_unificado[df_unificado['Estado'] == estado_selecionado]

    # Lista de anos únicas no estado selecionado
    anos_estado = sorted(df_estado['Ano'].unique())
    meses = sorted(df_estado['Mês'].unique())

    # Variáveis a serem plotadas
    variaveis = {
        'Temperatura Média (°C)': 'Temp_Media',
        'Precipitação Total (mm)': 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
        'Radiação Global (Kj/m²)': 'RADIACAO GLOBAL (Kj/m²)'
    }

    # Seleção interativa da variável
    nome_var = st.selectbox("Selecione a variável para visualizar:", list(variaveis.keys()))
    coluna_var = variaveis[nome_var]

    # Cores para os anos
    from matplotlib.cm import get_cmap
    cmap = get_cmap('viridis')
    cores_anos = {ano: cmap(i / len(anos_estado)) for i, ano in enumerate(anos_estado)}

    # Gerar o gráfico para a variável escolhida e estado selecionado
    titulo_grafico_dinamico = f"Média Mensal de {nome_var} em {estado_selecionado} (2020-2025)"
    st.subheader(titulo_grafico_dinamico)
    fig, ax = plt.subplots(figsize=(10, 6))
    for ano in anos_estado:
        df_ano_estado = df_estado[df_estado['Ano'] == ano].groupby('Mês')[coluna_var].mean().reindex(meses)
        if not df_ano_estado.empty:
            ax.plot(meses, df_ano_estado.values, marker='o', linestyle='-', color=cores_anos[ano], label=str(ano))

    ax.set_title(f'') # Deixamos o título vazio aqui pois st.subheader já faz o título principal
    ax.set_xlabel('Mês')
    ax.set_ylabel(nome_var)
    ax.set_xticks(meses)
    ax.grid(True)
    ax.legend(title='Ano')
    plt.tight_layout()
    st.pyplot(fig)

    # --- INÍCIO DA SEÇÃO DE EXPLICAÇÃO DO GRÁFICO ---
    st.markdown("---") # Linha divisória para separar o gráfico da explicação
    st.header("Entendendo o Gráfico: Análise de Dados Climáticos por Estado")

    st.write(
        """
        Olá a todos! Apresento aqui um gráfico interativo desenvolvido no Streamlit que nos permite analisar dados climáticos de forma muito dinâmica, focando em um estado específico e diferentes variáveis ao longo dos anos.
        """
    )

    st.subheader("1. Título do Gráfico:")
    st.markdown(
        f"""
        * **"{titulo_grafico_dinamico}"**: O título nos informa exatamente o que o gráfico representa: a **média mensal da {nome_var}**, específica para o **Estado de {estado_selecionado}**, abrangendo os **anos de 2020 a 2025**.
        """
    )

    st.subheader("2. Eixos do Gráfico:")
    st.markdown(
        """
        * **Eixo X (Horizontal - Mês):** Representa os meses do ano, de 1 (janeiro) a 12 (dezembro). Isso nos permite ver a evolução da variável selecionada ao longo de um ano.
        * **Eixo Y (Vertical - Valor da Variável):** Indica o valor da variável selecionada (neste caso, por exemplo, Temperatura Média em °C, Precipitação Total em mm, ou Radiação Global em Kj/m²). A escala se adapta automaticamente aos dados.
        """
    )

    st.subheader("3. Linhas Coloridas e Legenda (Anos):")
    st.markdown(
        """
        * Cada **linha colorida** no gráfico representa um **ano diferente** (de 2020 a 2025).
        * A **legenda à direita** indica qual cor corresponde a cada ano.
        * Isso nos permite comparar o comportamento da variável selecionada (ex: temperatura, precipitação) para o mesmo mês em anos distintos, ajudando a identificar variações anuais e tendências.
        """
    )

    st.subheader("4. Interatividade do Streamlit (Controles Acima do Gráfico):")
    st.markdown(
        """
        A beleza deste aplicativo Streamlit está na sua interatividade, proporcionada pelos seletores acima do gráfico:

        * **"Selecione o Estado:"**: Permite que você escolha qualquer um dos estados brasileiros disponíveis na base de dados. Ao selecionar um estado, todos os gráficos e dados abaixo se ajustarão para refletir as informações desse estado.
        * **"Selecione a variável para visualizar:"**: Neste momento, você pode escolher entre `Temperatura Média (°C)`, `Precipitação Total (mm)` e `Radiação Global (Kj/m²)`. Ao mudar a variável, o gráfico se reorganiza para mostrar as médias mensais da nova variável para o estado e anos selecionados.

        Esses seletores tornam a ferramenta extremamente versátil para diferentes análises e investigações climáticas ou de dados.
        """
    )

    st.subheader("O que podemos aprender com este gráfico?")
    st.markdown(
        """
        * Podemos identificar **padrões sazonais** da variável selecionada para o estado escolhido. Por exemplo, em um estado, a temperatura pode ter um pico em meses específicos e ser mais baixa em outros.
        * É possível **comparar o comportamento da variável** em diferentes anos. Isso é crucial para observar se há variações significativas ano a ano ou se padrões se mantêm constantes.
        * Ao trocar o estado e a variável, você pode explorar a diversidade climática e de dados em diferentes regiões do Brasil.

        Em resumo, este gráfico é uma ferramenta poderosa e fácil de usar, que permite explorar e compreender as médias mensais de diversas variáveis climáticas por estado e ao longo dos anos, tudo isso graças à simplicidade e interatividade do Streamlit.
        """
    )
    # --- FIM DA SEÇÃO DE EXPLICAÇÃO DO GRÁFICO ---


except FileNotFoundError:
    st.error(f"Erro: O arquivo '{caminho_arquivo_unificado}' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna '{e}' não foi encontrada no arquivo CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro ao gerar os gráficos: {e}")
