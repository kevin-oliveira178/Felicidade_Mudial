import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import skew, kurtosis
import plotly.express as px
import pycountry as pc

st.set_page_config(page_title="Felicidade Mundial 2019", layout="wide")

# Dicionário para mapear nomes de países para códigos de duas letras
country_to_alpha2 = {country.name: country.alpha_2 for country in pc.countries}

# Dicionário para mapear códigos de países para continentes
continent_mapping = {
    'AF': 'Africa',
    'NA': 'North America',
    'OC': 'Oceania',
    'AN': 'Antarctica',
    'AS': 'Asia',
    'EU': 'Europe',
    'SA': 'South America'
}

# Dicionário para mapear códigos de países para continentes
country_to_continent = {
    'AF': 'Africa',
    'AL': 'Europe',
    'DZ': 'Africa',
    'AS': 'Asia',
    'AD': 'Europe',
    'AO': 'Africa',
    'AG': 'North America',
    'AR': 'South America',
    'AM': 'Asia',
    'AU': 'Oceania',
    'AT': 'Europe',
    'AZ': 'Asia',
    'BS': 'North America',
    'BH': 'Asia',
    'BD': 'Asia',
    'BB': 'North America',
    'BY': 'Europe',
    'BE': 'Europe',
    'BZ': 'North America',
    'BJ': 'Africa',
    'BT': 'Asia',
    'BO': 'South America',
    'BA': 'Europe',
    'BW': 'Africa',
    'BR': 'South America',
    'BN': 'Asia',
    'BG': 'Europe',
    'BF': 'Africa',
    'BI': 'Africa',
    'KH': 'Asia',
    'CM': 'Africa',
    'CA': 'North America',
    'CV': 'Africa',
    'CF': 'Africa',
    'TD': 'Africa',
    'CL': 'South America',
    'CN': 'Asia',
    'CO': 'South America',
    'KM': 'Africa',
    'CD': 'Africa',
    'CG': 'Africa',
    'CR': 'North America',
    'HR': 'Europe',
    'CU': 'North America',
    'CY': 'Asia',
    'CZ': 'Europe',
    'DK': 'Europe',
    'DJ': 'Africa',
    'DM': 'North America',
    'DO': 'North America',
    'EC': 'South America',
    'EG': 'Africa',
    'SV': 'North America',
    'GQ': 'Africa',
    'ER': 'Africa',
    'EE': 'Europe',
    'SZ': 'Africa',
    'ET': 'Africa',
    'FJ': 'Oceania',
    'FI': 'Europe',
    'FR': 'Europe',
    'GA': 'Africa',
    'GM': 'Africa',
    'GE': 'Asia',
    'DE': 'Europe',
    'GH': 'Africa',
    'GR': 'Europe',
    'GT': 'North America',
    'GN': 'Africa',
    'GW': 'Africa',
    'GY': 'South America',
    'HT': 'North America',
    'HN': 'North America',
    'HU': 'Europe',
    'IS': 'Europe',
    'IN': 'Asia',
    'ID': 'Asia',
    'IR': 'Asia',
    'IQ': 'Asia',
    'IE': 'Europe',
    'IL': 'Asia',
    'IT': 'Europe',
    'JM': 'North America',
    'JP': 'Asia',
    'KE': 'Africa',
    'KI': 'Oceania',
    'KR': 'Asia',
    'KW': 'Asia',
    'KG': 'Asia',
    'LA': 'Asia',
    'LV': 'Europe',
    'LB': 'Asia',
    'LS': 'Africa',
    'LR': 'Africa',
    'LY': 'Africa',
    'LT': 'Europe',
    'LU': 'Europe',
    'MG': 'Africa',
    'MW': 'Africa',
    'MY': 'Asia',
    'MV': 'Asia',
    'ML': 'Africa',
    'MT': 'Europe',
    'MH': 'Oceania',
    'MR': 'Africa',
    'MU': 'Africa',
    'MX': 'North America',
    'FM': 'Oceania',
    'MD': 'Europe',
    'MC': 'Europe',
    'MN': 'Asia',
    'ME': 'Europe',
    'MA': 'Africa',
    'MZ': 'Africa',
    'MM': 'Asia',
    'NA': 'Africa',
    'NR': 'Oceania',
    'NP': 'Asia',
    'NL': 'Europe',
    'NZ': 'Oceania',
    'NI': 'North America',
    'NE': 'Africa',
    'NG': 'Africa',
    'NO': 'Europe',
    'OM': 'Asia',
    'PK': 'Asia',
    'PW': 'Oceania',
    'PA': 'North America',
    'PG': 'Oceania',
    'PY': 'South America',
    'PE': 'South America',
    'PH': 'Asia',
    'PL': 'Europe',
    'PT': 'Europe',
    'QA': 'Asia',
    'RE': 'Africa',
    'RO': 'Europe',
    'RU': 'Europe',
    'RW': 'Africa',
    'WS': 'Oceania',
    'SM': 'Europe',
    'ST': 'Africa',
    'SA': 'Asia',
    'SN': 'Africa',
    'RS': 'Europe',
    'SC': 'Africa',
    'SL': 'Africa',
    'SG': 'Asia',
    'SK': 'Europe',
    'SI': 'Europe',
    'SB': 'Oceania',
    'SO': 'Africa',
    'ZA': 'Africa',
    'ES': 'Europe',
    'LK': 'Asia',
    'SD': 'Africa',
    'SR': 'South America',
    'SZ': 'Africa',
    'SE': 'Europe',
    'CH': 'Europe',
    'SY': 'Asia',
    'TJ': 'Asia',
    'TZ': 'Africa',
    'TH': 'Asia',
    'TG': 'Africa',
    'TO': 'Oceania',
    'TT': 'North America',
    'TN': 'Africa',
    'TR': 'Asia',
    'TM': 'Asia',
    'TV': 'Oceania',
    'UG': 'Africa',
    'UA': 'Europe',
    'AE': 'Asia',
    'GB': 'Europe',
    'US': 'North America',
    'UY': 'South America',
    'UZ': 'Asia',
    'VU': 'Oceania',
    'VE': 'South America',
    'VN': 'Asia',
    'YE': 'Asia',
    'ZM': 'Africa',
    'ZW': 'Africa'
}




def add_continent_column(df, country_col):
    def get_continent(country):
        try:
            # Obter o código do país a partir do dicionário
            country_code = country_to_alpha2.get(country, None)
            if country_code:
                continent = country_to_continent.get(country_code, 'Unknown')
                return continent
            else:
                return 'Unknown'
        except Exception as e:
            st.write(f"Erro ao processar o país: {country}. Erro: {e}")
            return 'Unknown'

    df['continent'] = df[country_col].apply(get_continent)

@st.cache_data
def load_and_prepare_data():
    # Carrega o dataset
    df = pd.read_csv("2019.csv")

    # Criar Score Category com base nos tercis do Score
    tercis = df['Score'].quantile([0.33, 0.66])

    def categorize(score):
        if score <= tercis[0.33]:
            return "Baixo"
        elif score <= tercis[0.66]:
            return "Médio"
        else:
            return "Alto"

    df['Score Category'] = df['Score'].apply(categorize)

    # Criar variável Riqueza baseado no GDP per capita (mediana)
    median_gdp = df['GDP per capita'].median()
    df['Riqueza'] = df['GDP per capita'].apply(lambda x: "Rico" if x >= median_gdp else "Pobre")

    # Adicionar coluna de continente
    add_continent_column(df, 'Country or region')
    
    return df

# Chame a função para carregar e preparar os dados
df = load_and_prepare_data()


# Definindo cores
background_color = "#ffffff"
text_color = "#000000"
accent_color = "#2c6e74"

# Barra lateral para navegação
st.sidebar.title("🔎 Navegação")
pages = [
    "Introdução",
    "1. Distribuição do Score",
    "2. Histogramas e Boxplots",
    "3. Assimetria e Curtose",
    "4. Score Category",
    "5. Score x Riqueza",
    "6. GDP vs Vida Saudável",
    "7. Dispersão: GDP x Score",
    "8. Heatmap de Correlações",
    "9. Generosidade por Continente",
    "10. Liberdade x Categoria de Felicidade",
    "11. Mapa Múndi de Felicidade"
]




###definição de  variáveis globais do app
score = df["Score"]



#bloco de introdução do app 


choice = st.sidebar.radio("Escolha uma seção:", pages)

if choice == "Introdução":
    st.title("🌍 O Analista Socioeconômico Global")
    st.markdown("""
    Este relatório explora os fatores socioeconômicos associados à **felicidade mundial** com base no _World Happiness Report 2019_.
    Utilizando análise exploratória de dados, buscamos responder questões relacionadas à distribuição da felicidade, desigualdade entre países, fatores econômicos, sociais e culturais.
    **Tema:** Economia e Desenvolvimento Social  
    **Fonte:** [Kaggle - World Happiness Report 2019](https://www.kaggle.com/unsdsn/world-happiness)
    """)

## segunda seção: distribuição da variável score



elif choice == "1. Distribuição do Score":
    
    st.write("O score de felicidade foi uma medida obtida em 2015 ao se perguntar as pessoas como elas classificariam sua felicidadede de 0 a 10"
             )
    st.write("E esse vai ser a nossa variável pricipal para avaliação")
    st.write("dito isso o primeiro passo é vermos as estatisticas descritivas sobre essa variável. Seguem elas abaixo")
    
    
    st.header("1️⃣ Distribuição do Score de Felicidade")
    st.write(df['Score'].describe())
    st.markdown("""
    olhando para a tabela acima e tomando o valor do desvio padrão e da média vemos que no primeiro intervalo 
    de media - menos desvio padrão a media + 1 vez o desvvio padrão vemos que os primeiro e terceiro quartis estão dentro dessa faixa. o que significa que 
    ao menos 50% dos dados estão nesse intervalo. O o que deixa a hipótese de que essa distribuição obedece a regra empirica 
    68, 95, 99,7. pode estar muito perto de um adistribuição normal.
    """)
    st.write("""por outro lado se olhar os valores de média e mediana. tmeos Mediana menor que a média, com uma diferença bem mínima. podemos supor então que 
            distribuição é fracamente assimetrica a direita. Mas calma, não conclua nada ainda """)
    st.write("passe para a próxima e vamos explorar mais um puco sobre, analisando os gráficos!! ")


### terçeira seção: gráficos que mostram a a distribuição da variável score ##


elif choice == "2. Histogramas e Boxplots":
    st.header("2️⃣ Histogramas e Boxplots do Score")
    
    #criação dos gráficos fig e histograma e boxplot fig2
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df['Score'], kde=True, ax=axs[0], color='#1f77b4')  # Azul
    axs[0].set_title("Histograma do Score")
    
    fig2, axs = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(y=df['Score'], ax=axs[1], color='#ff7f0e', horient = "h")  # Laranja
    axs[1].set_title("Boxplot do Score")
    
    #exibição dos gráficos e comentario embaixo
    st.pyplot(fig)
    st.wirite("escrever comentário aqui")
    st.write("""Nesse momento vamos buscar evidenciar nossa tese sobre a assimetria da distribuição dos dados 
             para isso podemos calcular o coeficiente de assimetria para a variável score seguindo o método de Skewness""")
    #calculo feito com método de skewnes. a função existente no pandas
    skewness = skew(df['Score'])
    
    st.write(f"**Assimetria:** {skewness:.4f}")
    st.write(f"""como podemos ver o valor do coeficiente de assimetria nos confima nossa suposição. o valor de {skewness:.4f} 
             mostra uma assimetria fraca e positiva""")
    st.write("podemos então representar isso graficamente com um box-plot")
    
    st.pyplot(fig2)
    st.write("perceba que mesmo com o gráfico. A essa diferença na distribuição é pouco perceptivel. parece até que os daos estão perfeita e igualmente distribuidos. ")
    st.write("o que faremos na sequência é melhor representar essa distribuição")
    
    
    
    #quarta parte: calculo da assimetria e curtose.


elif choice == "3. tabela de frequência do score":
    st.header("3️⃣ Tabela de frequência do Score")
    
    st.write(""" como estamos tratando de dados quantitativos contínuos é muito conveniente agrupar esses dados 
             , criando uma tabela de frequência de classes""")
    
    #criando a tabela de frequência
        
    n = len(score)
    s = np.std(score, ddof=1)  # desvio padrão amostral (ddof=1)
    amplitude = score.max() - score.min()
    

    # Calculando largura da classe utilizando método de scott, acredito que por ter acesso aos dados brutos
    # vou encontrar uma presentatividade melhor nele (bin width)

    h = (3.5 * s) / (n ** (1/3))

    # Calculando número de classes (bins) e minimos
    k = int(np.ceil(amplitude / h))
    h = int(np.ceil(h))
    min = int(np.floor(score.min()))
    max = int(np.ceil(score.max()))

    #definindo intervalos
    bins = list(range(min, max+1,h))
    labels = ['2 |-- 3','3 |-- 4','4 |-- 5','5 |-- 6','6 |-- 7', '7 |--|8']
    frq_tab_score = pd.cut(score, bins=bins, right=False, labels=labels).value_counts().sort_index()
    
    st.write(f""" Utilizaremos o método de Scott por se aplicar bem a uma quantidade media de dados, para calcular o numero 
             de classes k ({k}). Daí calculamos a amplitude h de cada classe ({h}). e
             tomaremos como valor valor ínfimo o piso do menor valor da série; criamos as classes e 
             distribuimos as ocorrencias.""")
    st.write("contruindo a tabelo temos:")
    st.write(frq_tab_score)
    st.write("""olhando a tabela de frequencias podemos observar uma concentração dos dados nas classes de intervalos de 4-5 e 5 a 6""")
    st.write("para uma melhor leitura vamos contruir um histograma a partir da tabela.")
    
    #construção do gráfico do histograma######
    labels = [str(interval) for interval in frq_tab_score.index]
    frequencias = frq_tab_score.values

    # Criar gráfico tipo histograma (manual)
    fig, ax = plt.subplots(figsize=(10, 6))

    plt.bar(labels, frequencias, edgecolor='black')
    bars = plt.bar(
        labels, 
        frequencias, 
        color='#1f77b4', 
        width=1.0,
        edgecolor='black'
        # Ajuste a largura aqui (padrão é 0.8)
    )
    plt.xlabel('Intervalos de Score')
    plt.ylabel('Frequência')
    plt.title('Histograma por Classes (Score)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    ####apresentação
    st.write(fig)
    st.write("agora temos uma boa visualização da distribuição. podemos calcular para esses dados agrupados as medidasa descritivas")
    
    
    ##kurt = kurtosis(df['Score'])
    #st.write(f"**Curtose:** {kurt:.2f}")
    #st.markdown("""
    #- Assimetria próxima de 0 indica uma distribuição quase simétrica.
    #- Curtose próxima de 0 indica distribuição mesocúrtica (sem caudas pesadas).
    #""")

elif choice == "4. Score Category":
    st.header("4️⃣ Classificação por Categoria de Felicidade")
    freq = df['Score Category'].value_counts()
    st.write(freq)
    st.bar_chart(freq)

elif choice == "5. Score x Riqueza":
    st.header("5️⃣ Felicidade x Riqueza do País")
    crosstab = pd.crosstab(df['Riqueza'], df['Score Category'])
    st.write(crosstab)
    st.bar_chart(crosstab)

elif choice == "6. GDP vs Vida Saudável":
    st.header("6️⃣ Correlação entre PIB per capita e Expectativa de Vida Saudável")
    corr = df[['GDP per capita', 'Healthy life expectancy']].corr().iloc[0, 1]
    st.write(f"Correlação de Pearson: {corr:.2f}")
    fig = px.scatter(df, x='GDP per capita', y='Healthy life expectancy',
                     color='Score Category', title='GDP vs Vida Saudável')
    st.plotly_chart(fig)

elif choice == "7. Dispersão: GDP x Score":
    st.header("7️⃣ Diagrama de Dispersão: GDP per capita x Score de Felicidade")
    fig = px.scatter(df, x='GDP per capita', y='Score',
                     color='Score Category', hover_name='Country or region')
    st.plotly_chart(fig)

elif choice == "8. Heatmap de Correlações":
    st.header("8️⃣ Mapa de Calor das Correlações")

    colors = ["#fd9091", "#feb369", "#76e1e9", "#62d8ba", "#b497e5"]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    numeric_cols = df.select_dtypes(include=np.number)
    corr_matrix = numeric_cols.corr(method='pearson')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.set_style("white")
    heatmap = sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap=custom_cmap,
        linewidths=0.5,
        linecolor=background_color,
        cbar_kws={"shrink": 0.8},
        annot_kws={"color": text_color}
    )

    plt.title("Matriz de Correlação", fontsize=16, color=accent_color)
    plt.xticks(rotation=45, ha="right", color=text_color)
    plt.yticks(rotation=0, color=text_color)
    plt.gcf().patch.set_facecolor(background_color)
    plt.tight_layout()
    st.pyplot(fig)
    
elif choice == "9. Generosidade por Continente":
    st.subheader("📦 Distribuição da Generosidade por Continente")
    df_valid = df[df['continent'] != 'Unknown']

    if not df_valid.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_valid, x='continent', y='Generosity', palette='Set2')
        plt.title('Distribuição da Generosidade por Continente')
        plt.xlabel('Continente')
        plt.ylabel('Generosidade')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Não há dados suficientes para exibir o gráfico de generosidade por continente.")
        

elif choice == "10. Liberdade x Categoria de Felicidade":
    st.header("🔟 Liberdade para cada Categoria de Felicidade")
    group_stats = df.groupby('Score Category')['Freedom to make life choices'].describe()
    st.write(group_stats)
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Score Category', y='Freedom to make life choices', palette='pastel')
    ax.set_title("Liberdade x Categoria de Felicidade")
    st.pyplot(fig)

elif choice == "11. Mapa Múndi de Felicidade":
    st.header("🌍 Mapa Múndi de Felicidade")
    
    # Criar um DataFrame para o mapa
    map_df = df[['Country or region', 'Score', 'GDP per capita', 'Healthy life expectancy', 'Generosity', 'Freedom to make life choices']]
    
    # Criar o mapa com uma paleta de cores personalizada em verde e roxo
    fig = px.choropleth(
        map_df,
        locations='Country or region',  # Nome do país
        locationmode='country names',  # Usar nomes de países
        color='Score',  # Cor baseada no Score
        hover_name='Country or region',  # Nome do país ao passar o mouse
        hover_data={
            'GDP per capita': True,
            'Healthy life expectancy': True,
            'Generosity': True,
            'Freedom to make life choices': True,
            'Score': True
        },
        color_continuous_scale=px.colors.sequential.Viridis,  # Paleta de cores verde e roxo
        title='Mapa Múndi de Felicidade 2019',
        labels={'Score': 'Score de Felicidade'},
        width=1000,  # Aumentar a largura do mapa
        height=600   # Aumentar a altura do mapa
    )
    
    st.plotly_chart(fig)
