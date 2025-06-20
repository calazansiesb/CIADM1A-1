# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y5giZWAVGzujKGxqbdSAF0I-MqFIdGTd

## https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UJ1HDR
"""



"""Análise Exploratória de Dados sobre "Learning Burnout"
Vou criar um código em Python para abrir, tratar e explorar os dados sobre "learning burnout". Primeiro, precisamos carregar o arquivo .sav (que é um formato do SPSS) e depois realizar algumas análises exploratórias.
"""

# Instalar o pacote necessário
!pip install pyreadstat

import pandas as pd
import pyreadstat
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Restante do código como fornecido anteriormente

"""###  Tratamento dos Dados criando Dicionarios"""

import pandas as pd
import numpy as np

# Carregar os dados (substitua pelo seu método de carregamento)
# df = pd.read_spss('dados.sav')

# Ver colunas originais
print("Colunas originais:")
print(df.columns.tolist())

# Criar cópia para tratamento
df_tratado = df.copy()

# Mapeamento de valores para categorias
mapeamentos = {
    'Q1': {1.0: 'Masculino', 2.0: 'Feminino'},
    'Q2': {1.0: '7ª série', 2.0: '8ª série', 3.0: '9ª série'},
    'Q3': {1.0: 'Urbano', 2.0: 'Rural'},
    'Q4': {1.0: 'Sim', 2.0: 'Não'},
    'Q5.1': {
        1.0: 'Fundamental',
        2.0: 'Médio',
        3.0: 'Superior incompleto',
        4.0: 'Superior completo',
        5.0: 'Pós-graduação'
    },
    'Q5.2': {
        1.0: 'Fundamental',
        2.0: 'Médio',
        3.0: 'Superior incompleto',
        4.0: 'Superior completo',
        5.0: 'Pós-graduação'
    },
    'Q6': {
        1.0: '<3000',
        2.0: '3000-5000',
        3.0: '5000-10000',
        4.0: '>10000'
    }
}

# Aplicar mapeamentos
for col, mapping in mapeamentos.items():
    if col in df_tratado.columns:
        df_tratado[col] = df_tratado[col].map(mapping)

# Salvar dados tratados para uso nos próximos scripts
df_tratado.to_pickle('dados_tratados.pkl')  # Formato que preserva os tipos de dados

print("\nDados tratados salvos em 'dados_tratados.pkl'")
print("Amostra dos dados tratados:")
display(df_tratado.head())

# Carregar o arquivo .sav
df, meta = pyreadstat.read_sav('/content/123年级day.sav')

# Mostrar as primeiras linhas
print("Primeiras linhas do dataset:")
display(df.head())

# Instala a fonte SimHei
!apt-get -qq install -y fonts-noto-cjk

import matplotlib.font_manager as fm
font_dirs = ['/usr/share/fonts/truetype/noto']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)

"""### Vou criar uma análise completa do dataset de learning burnout, incluindo tratamento de dados, visualizações e análises estatísticas relevantes."""



# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# 1. Primeiro, vamos verificar as colunas reais do seu dataframe
print("Colunas disponíveis no dataframe:")
print(df.columns.tolist())

# 2. Vamos criar um mapeamento entre os nomes em português e os nomes originais em chinês
# Baseado no seu dicionário de dados, vamos mapear algumas colunas principais:
column_mapping = {
    'Orgulho': '自豪',
    'Felicidade': '高兴',
    'Ansiedade': '焦虑',
    'Cansaço': '厌倦',
    'Resiliência': '心理弹性',
    'Gênero': 'Q1 - 1.性别',
    'Série': 'Q2 - 2.年级',
    'Origem': 'Q3 - 3.生源地'
}

# 3. Vamos verificar quais colunas do mapeamento existem no dataframe
available_columns = {}
for pt_name, original_name in column_mapping.items():
    if original_name in df.columns:
        available_columns[pt_name] = original_name
    else:
        print(f"Aviso: Coluna '{original_name}' ({pt_name}) não encontrada no dataframe")

print("\nColunas disponíveis para análise:")
print(available_columns)

# 4. Configuração de estilo
plt.style.use('ggplot')
sns.set_style("whitegrid")
# %matplotlib inline

# 5. Análise Descritiva Básica
print("\n## Estatísticas Descritivas ##")
display(df[list(available_columns.values())].describe().transpose())

# 6. Visualização de Distribuições
plt.figure(figsize=(15, 10))

for i, (pt_name, original_name) in enumerate(available_columns.items(), 1):
    if pt_name in ['Orgulho', 'Felicidade', 'Ansiedade', 'Cansaço', 'Resiliência']:
        plt.subplot(2, 3, i)
        sns.histplot(df[original_name], bins=15, kde=True)
        plt.title(f'Distribuição de {pt_name}')
        plt.xlabel('Pontuação')

plt.tight_layout()
plt.show()

# 7. Análise por Gênero (se disponível)
if 'Gênero' in available_columns:
    gender_mapping = {1.0: 'Masculino', 2.0: 'Feminino'}
    df['gender_label'] = df[available_columns['Gênero']].map(gender_mapping)

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='gender_label', y=available_columns['Cansaço'])
    plt.title('Nível de Cansaço (Burnout) por Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Nível de Cansaço')
    plt.show()

# 8. Correlações entre variáveis emocionais
emotion_vars = []
for pt_name in ['Felicidade', 'Ansiedade', 'Cansaço', 'Resiliência']:
    if pt_name in available_columns:
        emotion_vars.append(available_columns[pt_name])

if len(emotion_vars) >= 2:
    plt.figure(figsize=(10, 8))
    corr_matrix = df[emotion_vars].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                xticklabels=[available_columns.get(pt_name, pt_name) for pt_name in ['Felicidade', 'Ansiedade', 'Cansaço', 'Resiliência'] if pt_name in available_columns],
                yticklabels=[available_columns.get(pt_name, pt_name) for pt_name in ['Felicidade', 'Ansiedade', 'Cansaço', 'Resiliência'] if pt_name in available_columns])
    plt.title('Matriz de Correlação entre Variáveis Emocionais')
    plt.show()

# 9. Relação entre Resiliência e Cansaço (Burnout)
if 'Resiliência' in available_columns and 'Cansaço' in available_columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=available_columns['Resiliência'], y=available_columns['Cansaço'], alpha=0.6)
    plt.title('Relação entre Resiliência e Cansaço (Burnout)')
    plt.xlabel('Nível de Resiliência')
    plt.ylabel('Nível de Cansaço/Burnout')
    plt.show()

    # Análise de regressão
    print("\n## Análise de Regressão: Cansaço ~ Resiliência ##")
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df[available_columns['Resiliência']].dropna(),
        df[available_columns['Cansaço']].dropna()
    )
    print(f"Coeficiente: {slope:.3f} (Para cada aumento unitário na resiliência, o cansaço muda em {slope:.3f})")
    print(f"Intercepto: {intercept:.3f}")
    print(f"R²: {r_value**2:.3f} ({r_value**2:.1%} da variação no cansaço é explicada pela resiliência)")
    print(f"Valor p: {p_value:.4f}")
    if p_value < 0.05:
        print("A relação é estatisticamente significativa (p < 0.05)")
    else:
        print("A relação não é estatisticamente significativa")

"""
1 Como estão distribuídos os alunos por características demográficas?
---

"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
plt.style.use('ggplot')
sns.set_palette("pastel")
# %matplotlib inline

# Carregar dados tratados
try:
    df = pd.read_pickle('dados_tratados.pkl')
    print("Dados carregados com sucesso!")
except:
    print("Erro ao carregar dados. Execute primeiro o Script 1 de tratamento.")
    raise

# 1. Função para plotar distribuições
def plot_distribuicao(coluna, titulo, ordem=None):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x=coluna, order=ordem)
    plt.title(titulo)
    plt.xlabel('')
    plt.ylabel('Contagem')
    plt.xticks(rotation=45 if len(df[coluna].unique()) > 3 else 0)
    plt.show()

# 2. Distribuições demográficas
plot_distribuicao('Q1', 'Distribuição por Gênero', ['Masculino', 'Feminino'])
plot_distribuicao('Q2', 'Distribuição por Série', ['7ª série', '8ª série', '9ª série'])
plot_distribuicao('Q3', 'Distribuição por Origem', ['Urbano', 'Rural'])
plot_distribuicao('Q4', 'Distribuição por Criança sob Tutela', ['Sim', 'Não'])

# 3. Educação dos pais
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(data=df, x='Q5.1', order=['Fundamental', 'Médio', 'Superior incompleto', 'Superior completo', 'Pós-graduação'])
plt.title('Educação das Mães')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.countplot(data=df, x='Q5.2', order=['Fundamental', 'Médio', 'Superior incompleto', 'Superior completo', 'Pós-graduação'])
plt.title('Educação dos Pais')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 4. Renda familiar
plot_distribuicao('Q6', 'Distribuição por Renda Familiar', ['<3000', '3000-5000', '5000-10000', '>10000'])

# 5. Tabelas resumo
print("\n=== Resumo Demográfico ===")
print("\nGênero:")
print(df['Q1'].value_counts(normalize=True))

print("\nSérie:")
print(df['Q2'].value_counts(normalize=True))

print("\nOrigem:")
print(df['Q3'].value_counts(normalize=True))

print("\nCriança sob tutela:")
print(df['Q4'].value_counts(normalize=True))

print("\nEducação das mães:")
print(df['Q5.1'].value_counts(normalize=True))

print("\nEducação dos pais:")
print(df['Q5.2'].value_counts(normalize=True))

print("\nRenda familiar:")
print(df['Q6'].value_counts(normalize=True))

import matplotlib
import matplotlib.pyplot as plt

# Instalar e configurar uma fonte compatível com chinês (ex: Noto Sans CJK)
!apt-get -qq install fonts-noto-cjk
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
matplotlib.rcParams['axes.unicode_minus'] = False  # Corrige sinal de menos em eixos

"""## 2 Quais são os níveis médios das diferentes emoções relatadas?"""

# Instale a fonte Noto Sans CJK (executar apenas uma vez, pode ser ignorado se já tiver rodado)
!apt-get -qq install -y fonts-noto-cjk

import matplotlib.font_manager as fm
font_dirs = ['/usr/share/fonts/truetype/noto']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de estilo
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Simulação de DataFrame (substitua pelo seu df real)
# Exemplo de criação do DataFrame:
# df = pd.read_csv('seuarquivo.csv')
df = pd.DataFrame({
    '自豪': [3, 4, 2, 5, 3],
    '高兴': [4, 5, 3, 4, 4],
    '希望': [3, 3, 4, 4, 3],
    '满足': [4, 4, 4, 5, 3],
    '平静': [2, 3, 2, 4, 3],
    '放松': [3, 3, 2, 4, 2],
    '焦虑': [2, 2, 3, 1, 2],
    '羞愧': [1, 2, 1, 2, 1],
    '恼火': [2, 3, 2, 2, 2],
    '厌倦': [1, 2, 2, 1, 2],
    '无助': [1, 1, 2, 1, 1],
    '沮丧': [1, 1, 2, 2, 1],
    '心烦': [2, 2, 2, 1, 2]
})

# Dicionário das emoções básicas (chinês -> português)
emocoes = {
    '自豪': 'Orgulho',
    '高兴': 'Felicidade',
    '希望': 'Esperança',
    '满足': 'Satisfação',
    '平静': 'Calma',
    '放松': 'Relaxamento',
    '焦虑': 'Ansiedade',
    '羞愧': 'Vergonha',
    '恼火': 'Irritação',
    '厌倦': 'Cansaço',
    '无助': 'Desamparo',
    '沮丧': 'Desânimo',
    '心烦': 'Agitação'
}

# Filtrar apenas as colunas de emoções que existem no dataframe
cols_emocionais = [col for col in emocoes.keys() if col in df.columns]

# Calcular as médias
medias = df[cols_emocionais].mean()
medias.index = [emocoes[col] for col in medias.index]
medias = medias.sort_values(ascending=False)

# 1. Gráfico de todas as emoções
plt.figure(figsize=(12, 6))
cores = ['#3498db' if val >= 3 else '#e74c3c' for val in medias.values]
sns.barplot(x=medias.values, y=medias.index, hue=medias.index, palette=cores, legend=False)
plt.title('Intensidade Média das Emoções Relatadas', fontsize=16, pad=20)
plt.xlabel('Escala Média (1-5)', fontsize=12)
plt.ylabel('')
plt.xlim(0, 5)
plt.axvline(x=3, color='gray', linestyle='--', alpha=0.5)
plt.show()

# 2. Gráfico dividido por tipo de emoção
plt.figure(figsize=(14, 6))

# Emoções positivas
positivas = ['Felicidade', 'Esperança', 'Satisfação', 'Calma', 'Relaxamento', 'Orgulho']
plt.subplot(1, 2, 1)
sns.barplot(x=medias[positivas].values, y=medias[positivas].index, hue=medias[positivas].index, palette="Blues_d", legend=False)
plt.title('Emoções Positivas', fontsize=14)
plt.xlabel('Intensidade Média')
plt.xlim(0, 5)

# Emoções negativas
negativas = ['Ansiedade', 'Irritação', 'Cansaço', 'Desânimo', 'Agitação', 'Vergonha', 'Desamparo']
plt.subplot(1, 2, 2)
sns.barplot(x=medias[negativas].values, y=medias[negativas].index, hue=medias[negativas].index, palette="Reds_d", legend=False)
plt.title('Emoções Negativas', fontsize=14)
plt.xlabel('Intensidade Média')
plt.xlim(0, 5)

plt.tight_layout()
plt.show()

"""### 3 Como as emoções positivas e negativas se correlacionam?"""

# 1. Instala a fonte para caracteres chineses (se necessário)
!apt-get -qq install -y fonts-noto-cjk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# 2. Configuração de fontes para suportar caracteres chineses
fonte_cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not os.path.exists(fonte_cjk):
    fonte_cjk = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(fonte_cjk)
prop_cjk = fm.FontProperties(fname=fonte_cjk)
plt.rcParams['font.sans-serif'] = [fonte_cjk, 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 3. Dicionário das emoções (chinês -> português)
emocoes = {
    '自豪': 'Orgulho',
    '高兴': 'Felicidade',
    '希望': 'Esperança',
    '满足': 'Satisfação',
    '平静': 'Calma',
    '放松': 'Relaxamento',
    '焦虑': 'Ansiedade',
    '羞愧': 'Vergonha',
    '恼火': 'Irritação',
    '厌倦': 'Cansaço',
    '无助': 'Desamparo',
    '沮丧': 'Desânimo',
    '心烦': 'Agitação'
}

# 4. Emoções positivas e negativas
positivas = ['自豪', '高兴', '希望', '满足', '平静', '放松']
negativas = ['焦虑', '羞愧', '恼火', '厌倦', '无助', '沮丧', '心烦']

# 5. Carregue o DataFrame do arquivo SAV
df = pd.read_spss('/content/123年级day.sav')

# 6. Calcule o índice médio de emoções positivas e negativas para cada linha
df['Índice Positivo'] = df[positivas].mean(axis=1)
df['Índice Negativo'] = df[negativas].mean(axis=1)

# 7. Calcule a correlação de Pearson
correlacao = df[['Índice Positivo', 'Índice Negativo']].corr().iloc[0, 1]

# 8. Faça o gráfico de dispersão com linha de tendência
plt.figure(figsize=(8,6))
sns.regplot(
    data=df,
    x='Índice Positivo',
    y='Índice Negativo',
    scatter_kws={'s': 60, 'alpha': 0.7, 'color': '#3498db', 'edgecolor': 'black'},
    line_kws={"color": "#e74c3c", "lw": 2}
)
plt.title(f'Correlação entre Emoções Positivas e Negativas\nCoeficiente de Pearson: {correlacao:.2f}',
          fontproperties=prop_cjk, fontsize=15)
plt.xlabel('Índice Médio de Emoções Positivas', fontproperties=prop_cjk, fontsize=12)
plt.ylabel('Índice Médio de Emoções Negativas', fontproperties=prop_cjk, fontsize=12)
plt.grid(True, alpha=0.1)
plt.tight_layout()
plt.show()

print(df.columns)

"""### 4 Existem diferenças nos níveis de burnout entre gêneros, séries ou origens?"""

# Instale fonte chinesa se necessário
!apt-get -qq install -y fonts-noto-cjk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# Fonte chinesa
fonte_cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not os.path.exists(fonte_cjk):
    fonte_cjk = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(fonte_cjk)
prop_cjk = fm.FontProperties(fname=fonte_cjk)
plt.rcParams['font.sans-serif'] = [fonte_cjk, 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Carrega dados
df = pd.read_spss('/content/123年级day.sav')

# DEFINA AQUI quais são as colunas de agrupamento:
col_burnout = '学业倦怠'  # burnout acadêmico
col_genero = 'Q1'       # substitua se souber o nome correto
col_serie = 'Q2'        # substitua se souber o nome correto
col_origem = 'Q3'       # substitua se souber o nome correto

# Gráfico de burnout por gênero
plt.figure(figsize=(6,4))
sns.boxplot(x=col_genero, y=col_burnout, data=df, palette='pastel')
plt.title('Níveis de Burnout por Gênero', fontproperties=prop_cjk, fontsize=14)
plt.xlabel('Gênero', fontproperties=prop_cjk)
plt.ylabel('Índice de Burnout', fontproperties=prop_cjk)
plt.tight_layout()
plt.show()

# Gráfico de burnout por série
plt.figure(figsize=(6,4))
sns.boxplot(x=col_serie, y=col_burnout, data=df, palette='Set2')
plt.title('Níveis de Burnout por Série', fontproperties=prop_cjk, fontsize=14)
plt.xlabel('Série', fontproperties=prop_cjk)
plt.ylabel('Índice de Burnout', fontproperties=prop_cjk)
plt.tight_layout()
plt.show()

# Gráfico de burnout por origem
plt.figure(figsize=(6,4))
sns.boxplot(x=col_origem, y=col_burnout, data=df, palette='Set3')
plt.title('Níveis de Burnout por Origem', fontproperties=prop_cjk, fontsize=14)
plt.xlabel('Origem', fontproperties=prop_cjk)
plt.ylabel('Índice de Burnout', fontproperties=prop_cjk)
plt.tight_layout()
plt.show()

# Testes estatísticos (ANOVA)
from scipy.stats import f_oneway

# Por gênero
grupos_genero = [g[col_burnout].dropna() for n, g in df.groupby(col_genero)]
stat_gen, p_gen = f_oneway(*grupos_genero)
print(f'Teste ANOVA - Burnout por Gênero: p-valor = {p_gen:.4f}')

# Por série
grupos_serie = [g[col_burnout].dropna() for n, g in df.groupby(col_serie)]
stat_ser, p_ser = f_oneway(*grupos_serie)
print(f'Teste ANOVA - Burnout por Série: p-valor = {p_ser:.4f}')

# Por origem
grupos_origem = [g[col_burnout].dropna() for n, g in df.groupby(col_origem)]
stat_ori, p_ori = f_oneway(*grupos_origem)
print(f'Teste ANOVA - Burnout por Origem: p-valor = {p_ori:.4f}')

"""### 5 Qual a relação entre resiliência psicológica e burnout?"""

# Instale a fonte para caracteres chineses (se necessário)
!apt-get -qq install -y fonts-noto-cjk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# Fonte chinesa
fonte_cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not os.path.exists(fonte_cjk):
    fonte_cjk = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(fonte_cjk)
prop_cjk = fm.FontProperties(fname=fonte_cjk)
plt.rcParams['font.sans-serif'] = [fonte_cjk, 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Carregue os dados
df = pd.read_spss('/content/123年级day.sav')

# Nome das variáveis (ajuste se necessário dependendo dos nomes do seu arquivo)
col_resiliencia = '心理弹性'  # Resiliência psicológica
col_burnout = '学业倦怠'     # Burnout acadêmico

# Gráfico de dispersão com linha de tendência
plt.figure(figsize=(8,6))
sns.regplot(
    data=df,
    x=col_resiliencia,
    y=col_burnout,
    scatter_kws={'s': 60, 'alpha': 0.7, 'color': '#2ecc71', 'edgecolor': 'black'},
    line_kws={"color": "#e74c3c", "lw": 2}
)
plt.title('Relação entre Resiliência Psicológica e Burnout Acadêmico',
          fontproperties=prop_cjk, fontsize=15)
plt.xlabel('Resiliência Psicológica (心理弹性)', fontproperties=prop_cjk, fontsize=12)
plt.ylabel('Burnout Acadêmico (学业倦怠)', fontproperties=prop_cjk, fontsize=12)
plt.grid(True, alpha=0.1)
plt.tight_layout()
plt.show()

ordem_escolaridade_mae = df['Q5.1'].dropna().unique().tolist()
ordem_escolaridade_pai = df['Q5.2'].dropna().unique().tolist()

"""### 6 Como a escolaridade dos pais influencia a média de resiliência psicológica dos alunos?"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurações para renderização suave
plt.rcParams['figure.dpi'] = 100  # Reduzindo um pouco a resolução para melhor performance
plt.rcParams['interactive'] = True  # Modo interativo

# Configurações de estilo
plt.style.use('seaborn-v0_8')  # Estilo moderno e estável
sns.set_theme(style="whitegrid", palette="pastel", font_scale=1.1)

# Suprimir warnings do Seaborn
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Carregar dados (com fallback para dados de exemplo)
try:
    df = pd.read_pickle('dados_tratados.pkl')
except FileNotFoundError:
    print("Criando dados de exemplo...")
    np.random.seed(42)
    data = {
        'Q5.1': np.random.choice(['Fundamental', 'Médio', 'Superior completo', 'Pós-graduação'], 100),
        'Q5.2': np.random.choice(['Fundamental', 'Médio', 'Superior incompleto', 'Superior completo'], 100),
        '心理弹性': np.random.normal(3, 1, 100),
        '个人力': np.random.normal(3, 1, 100),
        '情绪控制': np.random.normal(3, 1, 100)
    }
    df = pd.DataFrame(data)

# Criar variável de resiliência
resiliencia_cols = ['心理弹性', '个人力', '情绪控制']
df['Resiliência'] = df[resiliencia_cols].mean(axis=1)

# Ordem das categorias
ordem_escolaridade = ['Fundamental', 'Médio', 'Superior incompleto',
                     'Superior completo', 'Pós-graduação']

# Função otimizada para plotagem suave
def plot_smooth_boxplot(var, title):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Boxplot com renderização otimizada
    sns.boxplot(data=df, x=var, y='Resiliência', order=ordem_escolaridade,
               hue=df[var], legend=False, palette="pastel",
               width=0.6, linewidth=1.5, ax=ax)

    # Linha de média com anti-aliasing
    media_geral = df['Resiliência'].mean()
    ax.axhline(media_geral, color='gray', linestyle='--', alpha=0.7,
              linewidth=1.5, antialiased=True)

    # Configurações de performance
    plt.title(title, fontsize=14)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    # Renderização final
    fig.canvas.draw()
    plt.show(block=False)  # Não bloquear a execução
    plt.pause(0.1)  # Pequena pausa para renderização

# Plotar gráficos suavemente
plot_smooth_boxplot('Q5.1', 'Resiliência por Escolaridade da Mãe')
plot_smooth_boxplot('Q5.2', 'Resiliência por Escolaridade do Pai')

# Manter as janelas abertas
plt.show(block=True)

"""## 7 Existe relação entre o sentimento de orgulho e o desempenho acadêmico em alunos com diferentes níveis de baixa realização?"""

# Instale a fonte para caracteres chineses (se necessário, apenas no Colab)
!apt-get -qq install -y fonts-noto-cjk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# Configuração de fonte chinesa para gráficos
fonte_cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not os.path.exists(fonte_cjk):
    fonte_cjk = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(fonte_cjk)
prop_cjk = fm.FontProperties(fname=fonte_cjk)
plt.rcParams['font.sans-serif'] = [fonte_cjk, 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Carregar os dados (ajuste o caminho se necessário)
df = pd.read_spss('/content/123年级day.sav')

# Variáveis conforme o dicionário do dataset
col_orgulho = '自豪'                 # Sentimento de orgulho
col_baixa_realizacao = '低成就感分量表'  # Baixa realização acadêmica

# 1. Criar categorias de baixa realização (terços)
df = df[[col_orgulho, col_baixa_realizacao]].copy()
df = df.dropna()
df['Nível baixa realização'] = pd.qcut(df[col_baixa_realizacao], q=3, labels=['Baixo', 'Médio', 'Alto'])

# 2. Gráfico: orgulho vs. baixa realização, estratificado por nível
sns.lmplot(
    data=df,
    x=col_orgulho,
    y=col_baixa_realizacao,
    hue='Nível baixa realização',
    palette='Set1',
    height=6,
    aspect=1.2,
    scatter_kws={'s': 50, 'alpha': 0.7, 'edgecolor': 'black'}
)
plt.title('Relação entre Orgulho e Baixa Realização Acadêmica\npor Níveis de Baixa Realização', fontproperties=prop_cjk, fontsize=15)
plt.xlabel('Sentimento de Orgulho (自豪)', fontproperties=prop_cjk, fontsize=12)
plt.ylabel('Baixa Realização Acadêmica (低成就感分量表)', fontproperties=prop_cjk, fontsize=12)
plt.tight_layout()
plt.show()

print(df['Q4'].unique())

"""### 8: Qual a correlação entre os índices compostos de emoções positivas e negativas, considerando a série escolar?"""

import matplotlib
import matplotlib.pyplot as plt

# Instalar e configurar uma fonte compatível com chinês (ex: Noto Sans CJK)
!apt-get -qq install fonts-noto-cjk
matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
matplotlib.rcParams['axes.unicode_minus'] = False  # Corrige sinal de menos em eixos

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
import os

# Suprimir avisos do matplotlib para fontes
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Tente instalar a fonte caso não exista
if not os.path.exists("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc") and not os.path.exists("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
    try:
        # Instala a fonte no Colab/Linux
        import subprocess
        subprocess.run(["apt-get", "-qq", "install", "-y", "fonts-noto-cjk"])
    except Exception as e:
        print("Não foi possível instalar a fonte automaticamente:", e)

# Verifica qual caminho está disponível
if os.path.exists("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    fonte_cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
elif os.path.exists("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
    fonte_cjk = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
else:
    raise FileNotFoundError("Fonte NotoSansCJK-Regular.ttc não encontrada. Instale fonts-noto-cjk.")

# Adiciona a fonte ao gerenciador do matplotlib
fm.fontManager.addfont(fonte_cjk)
prop_cjk = fm.FontProperties(fname=fonte_cjk)

# Definir fonte padrão para evitar warnings e garantir chinês em todos os elementos
plt.rcParams['font.sans-serif'] = [fonte_cjk, 'Noto Sans CJK SC', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Carrega dados
df = pd.read_pickle("dados_tratados.pkl")

# Cria gráfico de dispersão
plt.figure(figsize=(8, 6))
plot = sns.scatterplot(
    data=df,
    x='积极情绪因子',
    y='消极情绪因子',
    hue='Q2',
    palette='Set2',
    s=60,
    edgecolor='black',
    alpha=0.8
)

# Aplicar fonte individualmente nos textos
plot.set_title('Correlação entre Emoções Positivas e Negativas por Série Escolar', fontproperties=prop_cjk, fontsize=14)
plot.set_xlabel('Índice Positivo (积极情绪因子)', fontproperties=prop_cjk)
plot.set_ylabel('Índice Negativo (消极情绪因子)', fontproperties=prop_cjk)

# Atualiza legendas com fonte também
legend = plot.get_legend()
if legend is not None:
    for text in legend.get_texts():
        text.set_fontproperties(prop_cjk)
    legend.set_title('Série', prop=prop_cjk)

plt.tight_layout()
plt.show()