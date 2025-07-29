import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import f_oneway

# === Estilo ===
colors = ["#ff6b6b", "#feca57", "#48dbfb", "#1dd1a1", "#5f27cd", "#00d2d3"]
accent_color = "#10ac84"

# Configuração da página
st.set_page_config(page_title="Análise Felicidade", layout="wide")

# === Navegação ===
secoes = [
    "Introdução",
    "Estatísticas Descritivas",
    "Histograma e Tendências",
    "Correlação",
    "Generosidade por Continente",
    "Liberdade por Categoria",
    "Exportar Dados"
]
selecionado = st.sidebar.radio("Escolha uma seção", secoes)

# === Leitura dos dados ===
df = pd.read_csv("2019.csv")

# Categorias
tercis = df["Score"].quantile([0.3333, 0.6667])
df["Score_Category"] = pd.cut(df["Score"],
                              bins=[-np.inf, tercis[0.3333], tercis[0.6667], np.inf],
                              labels=["Baixo", "Médio", "Alto"])

# Continente
try:
    import pycountry_convert as pc
    def get_continent(country):
        try:
            code = pc.country_name_to_country_alpha2(country)
            cont = pc.country_alpha2_to_continent_code(code)
            return {
                'AF': 'Africa', 'NA': 'North America', 'OC': 'Oceania',
                'AN': 'Antarctica', 'AS': 'Asia', 'EU': 'Europe', 'SA': 'South America'
            }.get(cont, 'Unknown')
        except:
            return 'Unknown'
    df['continent'] = df['Country or region'].apply(get_continent)
except:
    st.warning("Módulo `pycountry_convert` não instalado. Continente não atribuído.")
    df["continent"] = "Unknown"

# === Conteúdo de cada aba ===

if selecionado == "Introdução":
    st.title("Análise de Felicidade Mundial 2019")
    st.markdown("""
    Este painel interativo apresenta uma análise descritiva dos dados da felicidade global em 2019, considerando fatores como:
    - Score de felicidade
    - Continente
    - Generosidade
    - Liberdade de escolha
    - Correlação entre variáveis
    """)

elif selecionado == "Estatísticas Descritivas":
    st.subheader("Estatísticas Descritivas")
    st.dataframe(df.describe())

elif selecionado == "Histograma e Tendências":
    st.subheader("Score de Felicidade")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["Score"], bins=15, edgecolor="black")
    plt.title("Distribuição do Score")
    st.pyplot(fig)

elif selecionado == "Correlação":
    st.subheader("Matriz de Correlação")
    cmap = LinearSegmentedColormap.from_list("custom", colors)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.select_dtypes(include=np.number).corr(), cmap=cmap, annot=True)
    st.pyplot(fig)

elif selecionado == "Generosidade por Continente":
    st.subheader("Generosidade por Continente")
    df_valid = df[df["continent"] != "Unknown"]
    media_gen = df_valid.groupby("continent")["Generosity"].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=media_gen.index, y=media_gen.values, palette=colors[:len(media_gen)])
    plt.title("Média de Generosidade")
    st.pyplot(fig)

    # Teste ANOVA
    grupos = [g["Generosity"].values for _, g in df_valid.groupby("continent")]
    f_stat, p_val = f_oneway(*grupos)
    st.markdown(f"**Estatística F:** {f_stat:.2f}  \n**p-valor:** {p_val:.4f}")
    if p_val < 0.05:
        st.success("→ Diferença significativa entre continentes.")
    else:
        st.info("→ Não há diferença significativa.")

elif selecionado == "Liberdade por Categoria":
    st.subheader("Liberdade por Score")
    st.dataframe(df.groupby("Score_Category")["Freedom to make life choices"].describe())

elif selecionado == "Exportar Dados":
    st.subheader("Exportar Dados")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", data=csv, file_name="felicidade_2019.csv", mime="text/csv")
