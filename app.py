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

###### funções internas ####

def calcular_quartil(df, k):
    N = df['Frequência'].sum()
    pos = k * N / 4  # posição do quartil (k=1 → Q1, k=2 → Q2...)
    
    for i, freq_acum in enumerate(df['Frequência Acumulada']):
        if freq_acum >= pos:
            break
    
    classe = df.iloc[i]
    L = classe['Classe'].left
    F_antes = 0 if i == 0 else df.iloc[i - 1]['Frequência Acumulada']
    f = classe['Frequência']
    h = classe['Classe'].right - classe['Classe'].left
    
    Q = L + ((pos - F_antes) / f) * h
    return Q







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
    "3. tabela de frequência do score",
    "4. Assimetria",
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
#criação da tabela de frequência agrupada para a variável score
score.info()
score = score
n = len(score)
s = np.std(score, ddof=1)  # desvio padrão amostral (ddof=1)
amplitude = score.max() - score.min()

# Calculando largura da classe utilizando método de scott, acredito que por ter acesso aos dados brutos
# vou encontrar uma presentatovodade melhor nele (bin width)

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
    
    st.write(""" O score de felicidade foi uma medida obtida em 2015
             ao se perguntar às pessoas como elas classificariam sua felicidade de 0 a 10.""" )
    st.write("E esse vai ser a nossa variável pricipal para avaliação")
    st.write("""Dito isso, o primeiro passo é vermos as estatísticas descritivas sobre 
             essa variável. Seguem abaixo.
          """)
    
    
    st.header("1️⃣ Distribuição do Score de Felicidade")
    st.write(df['Score'].describe())
    st.markdown("""
    Olhando para a tabela acima e tomando como referência o valor da média e do desvio padrão, 
    vemos que, no intervalo entre média - 1 desvio padrão e média + 1 desvio padrão, os primeiro 
    e terceiro quartis estão incluídos. Isso significa que pelo menos 50% dos dados estão dentro 
    desse intervalo, o que reforça a hipótese de que a distribuição segue a regra empírica 
    dos 68, 95, 99,7 — podendo, portanto, estar muito próxima de uma distribuição normal.
    """)
    st.write("""Por outro lado, se olharmos os valores de média e mediana, temos a mediana ligeiramente menor que a média, com uma diferença bem mínima. Podemos supor, então, que a distribuição é fracamente assimétrica à direita.
Mas calma — ainda não dá pra concluir nada com certeza! """)
    st.write("Passe para a próxima e vamos explorar mais um pouco, analisando os gráficos! ")


### terçeira seção: gráficos que mostram a a distribuição da variável score ##


elif choice == "2. Histogramas e Boxplots":
    st.header("2️⃣ Histogramas e Boxplots do Score")
     
    
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(x=df['Score'], ax=ax, color='#ff7f0e')
    ax.set_title("Boxplot do Score")
    plt.tight_layout()
    
    
    #exibição dos gráficos e comentario embaixo
    
    st.write("""Nesse momento vamos buscar evidenciar nossa tese sobre a assimetria da distribuição dos 
             dados 
             para isso podemos calcular o coeficiente de assimetria para a variável score seguindo o 
             método de Skewness""")
    #calculo feito com método de skewnes. a função existente no pandas
    skewness = skew(df['Score'])
    
    st.write(f"**Assimetria:** {skewness:.4f}")
    st.write(f"""Como podemos ver, o valor do coeficiente de assimetria confirma nossa suposição. 
             O valor de {skewness:.4f} indica uma assimetria fraca e positiva.
            """)
    st.write("Podemos, então, representar isso graficamente com um boxplot.")
    
    st.pyplot(fig)
    st.write("Perceba que, mesmo com o gráfico, a diferença na distribuição é pouco perceptível. Parece até que os dados estão perfeitamente e igualmente distribuídos.")
    st.write("O que faremos na sequência é representar melhor essa distribuição, de modo que possamos enxergar de fato o que está acontecendo.")
    st.write("Vá para a próxima seção.")
    
    #quarta parte: agrupamento dos dados.


elif choice == "3. tabela de frequência do score":
    st.header("3️⃣ Tabela de frequência do Score")
    
    st.write("""Como estamos tratando de dados quantitativos contínuos, é muito conveniente agrupar esses dados,
 criando uma tabela de frequência de classes.""")

    
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
    
    st.write(f"""Utilizaremos o método de Scott por se aplicar bem a uma quantidade média de dados, para calcular o número 
    de classes k ({k}). Daí calculamos a amplitude h de cada classe ({h}) e
    tomaremos como valor ínfimo o piso do menor valor da série; criamos as classes e 
    distribuímos as ocorrências.""")

    st.write("Construindo a tabela, temos:")

    st.write(frq_tab_score)

    st.write("""Olhando a tabela de frequências, podemos observar uma concentração dos dados nas classes de intervalos de 4-5 e 5-6.""")

    st.write("Para uma melhor leitura, vamos construir um histograma a partir da tabela.")

    
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
    plt.xticks(rotation=360)
    plt.tight_layout()
    
    ####apresentação
    st.pyplot(fig)
    st.write("Agora temos uma melhor visualização da distribuição. Podemos calcular para esses dados agrupados as medidas descritivas.")
    st.write("Podemos perceber, neste ponto, que há uma concentração de observações nos valores de 4 a 6 e que a maior parte dos dados está concentrada mais à direita.")
    st.write("A partir dos dados agrupados, podemos também refazer os cálculos das medidas descritivas e reconstruir o boxplot feito anteriormente.")

       ### #média ####
    # 1. Calcular os pontos médios dos intervalos
    classes = list(range(2,9,1))
    midpoints = [(i+i+1)/2 for i in classes]

    # 2. Frequências
    frequencias = frq_tab_score.values

    # 3. Produto frequência * ponto médio
    produto_fx = [f * x for f, x in zip(frequencias, midpoints)]

    # 4. Média
    AGmedia = sum(produto_fx) / sum(frequencias)

    ###########quartis 
    #formatar um data frame com as medidas necessárias 
    classes = pd.IntervalIndex.from_tuples([(2, 3), (3, 4), (4, 5), (5, 6),(6,7),(7,8)])
    frequencias = frq_tab_score.values
    df2 = pd.DataFrame({'Classe': classes, 'Frequência': frequencias})
    df2['Frequência Acumulada'] = df2['Frequência'].cumsum() 

    qa1 = calcular_quartil(df2, 1)  #qa1 são as medidas de posição feitas a partir dos dados agrupados 
    qa2 = calcular_quartil(df2, 2)  # Mediana
    qa3 = calcular_quartil(df2, 3)

    minimo = df2['Classe'].apply(lambda x: x.left).min()
    maximo = df2['Classe'].apply(lambda x: x.right).max()
    st.write(f"Média:\n{AGmedia:.4f}\nQ1:\n{qa1:.4f}\nQ2 (Mediana):\n{qa2:.4f}\nQ3:\n{qa3:.4f}")

    st.write(f"""Note que o valor da média permanece e a mediana mantém sua leve diferença em comparação com os dados
    não agrupados.\nMédia: {AGmedia:.4f} > Mediana: {qa2:.4f}""")

    st.write("Tendo em mãos esses valores, podemos recriar o boxplot.")

    #a mediana se mantém minimamente menor que a média. logo não perdemos essa informação dos dados iniciais

    boxplot_data = {
        'med': qa2,
        'q1': qa1,
        'q3': qa3,
        'whislo': minimo,
        'whishi': maximo,
        'fliers': []  # sem outliers, pois não temos dados individuais
    }

    bxp, ax = plt.subplots(figsize=(6, 5))
    ax.axvline(qa2, color='green', linestyle='--', label=f'Mediana = {qa1}')
    ax.bxp([boxplot_data], showfliers=False, vert=False)  # aqui está a mudança
    ax.set_title('Boxplot para dados agrupados')
    ax.set_xlabel('Valores')  # trocar ylabel por xlabel, já que o gráfico fica horizontal
    ax.grid(True)
    
    
    st.write("Veja abaixo como fica o boxplot para esse agrupamento.")
    st.pyplot(bxp)
    st.write("""Perceba o 'bigode' da esquerda com comprimento maior em relação ao da direita. Isso demonstra que os dados estão mais afastados dos valores mais baixos,
            logo concentrados nos valores mais à direita.""")

    st.write("Na próxima seção, vejamos as variações da variável.")




elif choice == "4. Assimetria":
    
    st.write("Agora que temos os dados organizados de uma maneira agradável, vamos ver como ocorre a variação desses dados.")
    st.write("Tomar mão de medidas como:")

    
    #calculo das medidas de variação 
    #a diferença ainda é minima entre média ou seja fracamente assimétrica. mas nessa forma de apresentação já podemos ver que os dados estão concentrados mais a direita 

    classes = [(2, 3), (3, 4), (4, 5), (5, 6),(6,7),(7,8)]
    frequencias = frq_tab_score.values
    pontos_medios = [(a + b) / 2 for a, b in classes]

    # Total de elementos
    n = sum(frequencias)

    # Média
    media = sum(f * x for f, x in zip(frequencias, pontos_medios)) / n

    # Desvios centralizados
    desvios = [x - media for x in pontos_medios]

    # Variância
    variancia = sum(f * (d ** 2) for f, d in zip(frequencias, desvios)) / n

    # Desvio padrão
    desvio_padrao = np.sqrt(variancia)

    # Coeficiente de assimetria de fisher para dados agrupados 
    assimetria = sum(f * (d ** 3) for f, d in zip(frequencias, desvios)) / (n * desvio_padrao ** 3)

    # Curtose
    curtose = sum(f * (d ** 4) for f, d in zip(frequencias, desvios)) / (n * desvio_padrao ** 4)

    # Curtose-excesso (opcional)
    curtose_excesso = curtose - 3

    tabela = pd.DataFrame({
    'Medida': ['Média', 'variância', 'desvio padrão', 'coef assimetria','coeficiente de curtose'],
    'Valor': [media,variancia, desvio_padrao, assimetria,curtose_excesso]
    })
    st.write(tabela)
    st.write("""A média dos dados é 5,45 e a variância é 1,36, com desvio padrão de 1,16 — indicando uma dispersão
    moderada em torno da média. O coeficiente de assimetria é praticamente zero (0,0267), o que mostra
    que a distribuição é fracamente assimétrica. Já a curtose é -0,72, o que indica uma distribuição
    platicúrtica, ou seja, mais achatada que a normal.
    """)

    st.write("É possível visualizar ainda melhor isso no gráfico de curva de densidade.")

    
    
    #criação da tabela de frequência agrupada para a variável score
    score.info()
    score = score
    n = len(score)
    s = np.std(score, ddof=1)  # desvio padrão amostral (ddof=1)
    amplitude = score.max() - score.min()

    # Calculando largura da classe utilizando método de scott, acredito que por ter acesso aos dados brutos
    # vou encontrar uma presentatovodade melhor nele (bin width)

    h = (3.5 * s) / (n ** (1/3))

    # Calculando número de classes (bins) e minimos
    k = int(np.ceil(amplitude / h))
    h = int(np.ceil(h))
    min = int(np.floor(score.min()))
    max = int(np.ceil(score.max()))

    #definindo intervalos

    bins = list(range(min, max+1,h))
    
    
    fig2, ax = plt.subplots(figsize=(8, 5))
    # Histograma com densidade
    sns.histplot(score, bins=bins, kde=True, stat="density", edgecolor="black", color="lightblue")

    # Personalização
    plt.title("Histograma com Curva de Frequência (KDE)")
    plt.xlabel("Score")
    plt.ylabel("Densidade")
    plt.grid(True)
    plt.tight_layout()
    
    st.pyplot(fig2)
    st.write("""Onde podemos ver o achatamento sendo criado pela concentração dos dados nas duas classes centrais.""")

    st.write('''Note que, apesar do coeficiente de assimetria nos mostrar uma assimetria positiva, temos a impressão
        que é o oposto. Uma solução para esta distorção seria eliminar a primeira classe, pois há apenas 1 país nela,
        que cria essa impressão. Mas como nosso intuito é observar todos os países, vamos deixar essa coluna aí.''')

#parte da sara e nayla 


elif choice == "5. Score x Riqueza":
    st.header("5️⃣ Felicidade x Riqueza do País")
    st.markdown("""
                > O gráfico de barras empilhadas nos mostra visualmente o padrão descrito na tabela, na barra dos países pobres maior predominância da cor azul que representa baixa felicidade, já a barra dos países ricos é predominantemente azul claro, mostrando alta felicidade. A categoria média de felicidade se mostra mais equilibrada em ambos os grupos e menos expressiva em termos de quantidade. 
    """)
    crosstab = pd.crosstab(df['Riqueza'], df['Score Category'])
    st.write(crosstab)
    st.bar_chart(crosstab)
    st.markdown("""
                ## Conclusão:
                > Países ricos tendem a ser mais felizes, enquanto países pobres tendem a ser menos felizes. Isso indica que a correlação entre riqueza e felicidade é positiva, apesar de não ser uma relação determinística, a tendência é muito evidente.
    """)
    
elif choice == "6. GDP vs Vida Saudável":
    st.header("6️⃣ Correlação entre PIB per capita e Expectativa de Vida Saudável")
    st.markdown("""
                > O gráfico apresenta uma correlação forte positiva entre o GDP e Healthy life expectancy, por isso à medida que o GDP aumenta, também aumenta a expectativa de vida saudável. A distribuição dos pontos na tabela sugere uma tendência crescente, mostrando que países com maior renda proporcionam condições de vida melhores e mais saudáveis.
                > O coeficiente de correlação (corr = 0.84) mostra que há uma relação densa e considerável, pois quanto maior a renda média por pessoa de um país, maior a expectativa de vida com saúde de seus habitantes. De forma geral, o gráfico nos mostra uma ideia clara de que a riqueza contribui para o bem estar da população, provavelmente por meio do melhor acesso à saúde, educação, segurança, infraestrutura e lazer.
    """)
    corr = df[['GDP per capita', 'Healthy life expectancy']].corr().iloc[0, 1]
    st.write(f"Correlação de Pearson: {corr:.2f}")
    fig = px.scatter(df, x='GDP per capita', y='Healthy life expectancy',
                     color='Score Category', title='GDP vs Vida Saudável')
    st.plotly_chart(fig)

elif choice == "7. Dispersão: GDP x Score":
    st.header("7️⃣ Diagrama de Dispersão: GDP per capita x Score de Felicidade")
    st.markdown("""
                > O gráfico nos mostra uma tendência ascendente clara entre o GDP e o Score de Felicidade, pois conforme o GDP aumenta, o score de felicidade também tende a aumentar. Os pontos azuis (felicidade alta) se concentram no canto superior direito, o que indica que os países ricos, em sua maioria, têm maiores índices de felicidade. Os pontos rosa (baixa felicidade) se concentram no canto inferior esquerdo, representando países com desenvolvimento e felicidade média/baixa. Os dados apresentam uma relação positiva entre renda e felicidade. 
    """)
    fig = px.scatter(df, x='GDP per capita', y='Score',
                     color='Score Category', hover_name='Country or region')
    st.plotly_chart(fig)

elif choice == "8. Heatmap de Correlações":
    st.header("8️⃣ Mapa de Calor das Correlações")
    st.markdown("""
                ## 1. Índice de Felicidade: Como as Dimensões Socioeconômicas Importam:
                O índice de felicidade correlaciona-se positiva e fortemente com três variáveis principais, sendo elas:
                - **GDP per capita**: r = 0.79  
                > Isso significa que a riqueza média nacional está entre os fatores mais associados à felicidade. Quanto mais desenvolvida a economia de um país, melhor é a condição de vida dos habitantes.
                - **Social support (Apoio social)**: r = 0.78  
                > A presença de apoio social (amigos e familiares), tem contribuição igual ao fator econômico no nível de bem estar das pessoas.
                - **Expectativa de vida saudável**: r = 0.78  
                > A capacidade de viver uma vida longa e saudável está fortemente relacionada a percepção de felicidade.
                Isso significa que os fatores estruturais e básicos de bem estar são os principais determinantes do índice de felicidade.
                
                ## 2. O Overall Rank é um reflexo inverso do Score:
                >Como o papel do overall rank é ser inverso a todas as outras variáveis, todas estão correlacionadas negativamente com ele. As mais fortes são:
                 - **Score** r = -0.99
                >Como a correlação negativa é praticamente perfeita, isso valida a coluna score como base para a criação do ranking
                - **GDP per capita** (r = -0.80) e **Healthy life expectancy** (r = -0.79):
                >Mostra que países ricos e saudáveis ​​tendem a ocupar altas posições no ranking.
                
                ## 3. Liberdade e corrupção possui um papel moderado na felicidade:

                - **Liberdade para fazer escolhas de vida**: r = 0.57  
                > Isto é, ter liberdade para fazer escolhas importantes na vida contribui significativamente para o bem-estar percebido

                - **Percepções de corrupção**: r = 0.39  
                > Embora tenha uma correlação positiva, seu efeito é mais limitado. Isso significa que a corrupção percebida não afetou diretamente a felicidade da população em nível próximo.

                ## 4. Generosity: A Shockingly Weak Factor

                - **A generosidade**: r = 0.08  
                > Tem correlação de quase zero com o Score geral. Esta variável parece apontar o fato de que, embora seja crítico ao nível individual, o nível de generosidade de um país não afeta de forma significativa a felicidade dos habitantes.

                ## 5. Relações entre as variáveis explicativas:

                - **GDP per capita vs. Healthy life expectancy**: r = 0.84  
                > Países mais ricos têm maior qualidade de vida e longevidade.

                - **Social support vs. Freedom to make life choices**: r = 0.45  
                > As redes de apoio social fortalecem a autonomia.

                - **Perceptions of corruption vs. Freedom to make life choices**: r = 0.44  
                > A corrupção reduz a sensação de liberdade.

                ## Conclusão:

                > A matriz de correlação mostra que fatores estruturais básicos para a vida do ser humano têm maior correlação com a felicidade percebida no país.  
                > Características mais subjetivas (como generosidade e percepção de corrupção), embora tenham influência, possuem menor relevância na análise.
           


        """)
    
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
    st.markdown("""
                 ## Principais análises por continente:
                 - **Europe**:
                 > É perceptível uma grande dispersão dos dados por causa dos bigodes mais extensos e da caixa mais larga, tem uma mediana próxima de 0.15 mostrando uma generosidade moderada.
              
                 - **Oceania**:
                 > Possui apenas um valor visível (0.33), provavelmente mostrando que seus dois países (Nova Zelândia e Austrália) têm níveis de felicidade iguais ou muito próximos, além de ser um valor alto e sem dispersão, indica uma uniformidade nos dados, apesar de ser uma amostra pequena. 
              
                 - **North America**:
                 > A generosidade é moderada, também com a mediana em 0.15, mas possui outliers altos (acima de 0.4) indicando que alguns países são muito mais generosos que a média da região.
              
                 - **Asia**:
                 > A generosidade possui sua mediana pouco acima de 0.2, com uma grande variabilidade e maior presença de outliers, indicando que, apesar da região ter uma generosidade moderada, possui países muito generosos e isso gera uma grande diversidade no continente.
              
                 - **South America**:
                 > Possui a mediana mais baixa, comparado com os outros continentes, de aproximadamente 0.12 e com pouca variação, indicando que os países possuem os níveis de generosidade muito próximos, porém baixos. 
              
                 - **Africa**:
                 > Possui a mediana semelhante a Ásia, mais próxima de 0.18, tendo uma distribuição mais concentrada com uma leve presença de outliers altos, mostrando uma generosidade moderada com menor taxa de dispersão. 

                 ## Conclusão:
                 > Apesar da Oceania ter a maior taxa de generosidade, não pode ser tomada como uma informação relevante por possuir uma amostra muito limitada. A América do Sul possui a taxa de generosidade mais baixa e com a menor dispersão de dados. A América do Norte, Ásia e Europa têm as maiores variações internas, indicando maior taxa de desigualdade entre países da mesma região. 


     """)
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
    st.markdown("""
                - **Alta felicidade**:
                > É a categoria que possui a maior média (0.487), isso indica que pessoas que vivem em países mais felizes sentem que têm maior liberdade para tomar decisões de vida. Possui uma distribuição, com desvio padrão de 0.092, mais concentrada, o que apresenta maior consistência interna. Sua mediana (0.495) é bem próxima da média, sugerindo uma certa simetria. O intervalo interquartil é de 0.121, representando uma dispersão moderada.
                
                - **Média felicidade**:
                > A média da categoria é 0.375, o que nos mostra uma liberdade moderada. Tem uma dispersão de dados maior que da categoria anterior, mas menor que da categoria posterior. A mediana (de 0.389) também é próxima da média, que apresenta-nos uma distribuição também simétrica. O intervalo interquartil é de 0.187, mais alto que o da categoria anterior, sugere que há maior diversidade entre os países. 
                
                - **Baixa felicidade**:
                > É a categoria que apresenta a menor média (0.314) e a menor mediana (0.322), indicando que as pessoas nesses países sentem que têm menor liberdade para fazer escolhas de vida. Além disso, é a categoria que tem a maior dispersão (desvio padrão de 0.153), ou seja, existem muitos países em situações críticas, possui alguns países com níveis aceitáveis (máximo da categoria 0.609, maior que a média dos outros), mas também tem países onde a percepção de liberdade é praticamente nula (mínimo da categoria 0.000). Essa categoria é a que apresenta a distribuição mais assimétrica e mais desigual.

    """)
    group_stats = df.groupby('Score Category')['Freedom to make life choices'].describe()
    st.write(group_stats)
    
    st.markdown("""
                ## Conclusão:
                > Percebe-se que a percepção de liberdade está fortemente associada à felicidade. Países mais felizes têm níveis médios de liberdade mais altos e distribuições mais simétricas. Já os países menos felizes têm níveis médios de liberdade menor e maior assimetria nas distribuições. O que faz-se entender que liberdade e igualdade são fatores indispensáveis para o bem estar de uma sociedade e de seu desenvolvimento social.

    """)
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Score Category', y='Freedom to make life choices', palette='pastel')
    ax.set_title("Liberdade x Categoria de Felicidade")
    st.pyplot(fig)

elif choice == "11. Mapa Múndi de Felicidade":
    st.header("🌍 Mapa Múndi de Felicidade")
    st.markdown("""
                > Este mapa utiliza a escala de cores pra representar o nível de felicidade em cada país. Os tons de amarelo indicam países com maior felicidade, enquanto os tons de roxo mostram onde a menor nível de felicidade.
              * O mapa é interativo, ao passar o mouse sobre um país, exibe um pequeno texto com seus dados específicos.**

    """)
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
