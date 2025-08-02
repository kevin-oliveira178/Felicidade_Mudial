
# 🌍 Felicidade Mundial 2019

Este projeto é uma aplicação interativa desenvolvida com **Streamlit** que realiza uma análise exploratória do _World Happiness Report 2019_. O objetivo é investigar fatores socioeconômicos que influenciam o índice de felicidade em diferentes países ao redor do mundo.

## 📊 Sobre o App

A interface permite ao usuário explorar visualmente indicadores como PIB per capita, expectativa de vida saudável, generosidade, liberdade de escolha, e muito mais. Os dados são categorizados por níveis de felicidade e riqueza, além de análises por continente e por país.

---

## 🧠 Tema

**Área:** Economia e Desenvolvimento Social  
**Fonte:** [Kaggle - World Happiness Report 2019](https://www.kaggle.com/unsdsn/world-happiness)

---

## 🔍 Funcionalidades

O app possui 12 seções acessíveis via barra lateral de navegação:

1. **Introdução**  
    Apresenta o objetivo do projeto e o contexto dos dados.

2. **Distribuição do Score**  
    Exibe estatísticas descritivas da variável principal: o Score de Felicidade.

3. **Histogramas e Boxplots**  
    Visualizações básicas da distribuição do Score.

4. **Assimetria e Curtose**  
    Métricas estatísticas para avaliar a forma da distribuição do Score.
 
5. **Score Category**  
    Classificação dos países em "Baixo", "Médio" ou "Alto" com base em tercis.

6. **Score x Riqueza**  
    Análise cruzada entre riqueza (PIB) e felicidade.

7. **GDP vs Vida Saudável**  
    Correlação entre PIB per capita e expectativa de vida saudável.

8. **Dispersão: GDP x Score**  
    Gráfico interativo para explorar a relação entre PIB e felicidade.

9. **Heatmap de Correlações**  
    Mapa de calor das correlações entre variáveis numéricas.

10. **Generosidade por Continente**  
    Comparação da generosidade média entre continentes.

11. **Liberdade x Categoria de Felicidade**  
    Boxplot mostrando a liberdade em cada nível de felicidade.

12. **Mapa Múndi de Felicidade**
    Mapa mundi interativo que apresenta uma pequena apresentação de dados estatísticos individuais de cada país.

13. **Download do Relatório**
    Download do relatório da análise exploratória dos dados apresentados.
    
---

## 🗃️ Estrutura dos Dados

O conjunto de dados contém colunas como:

- `Country or region`
- `Score`
- `GDP per capita`
- `Social support`
- `Healthy life expectancy`
- `Freedom to make life choices`
- `Generosity`
- `Perceptions of corruption`

Novas colunas criadas:

- `Score Category`: categorização em "Baixo", "Médio" e "Alto"
- `Riqueza`: classificação como "Rico" ou "Pobre"
- `continent`: continente obtido via código do país (usando pycountry)

---

## 💻 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

---

## 📦 Requisitos

- Python 3.8+
- Pandas
- NumPy
- Streamlit
- Seaborn
- Matplotlib
- Plotly
- PyCountry

> O arquivo `requirements.txt` já está incluso neste repositório.

---

## 🌐 Demonstração Online

🔗 *[https://felicidademundial-zsmd9hmvzvxlmcbvclvwxy.streamlit.app/](https://felicidademundial-zsmd9hmvzvxlmcbvclvwxy.streamlit.app/)*

---

## 🧠 Autores e Créditos

Este projeto foi desenvolvido como parte de uma análise acadêmica e conta com contribuições colaborativas.

- 💡 **Nome:** [Sara Martins de Oliveira]
- 🧪 **GitHub:** [https://github.com/error404-byshmo](https://github.com/error404-byshmo)

- 💡 **Nome:** [Kevin Evanilson de Oliveira Lima]
- 🧪 **GitHub:** [https://github.com/kevin-oliveira178](https://github.com/kevin-oliveira178)

- 💡 **Nome:** [Nayla Moraes Ferreira]
- 🧪 **GitHub:** [https://github.com/Anaylaa](https://github.com/Anaylaa)


---

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🤝 Contribuições

Contribuições são bem-vindas!  
Abra uma *Issue* ou envie um *Pull Request* com sugestões de melhoria, correções ou novas visualizações.
