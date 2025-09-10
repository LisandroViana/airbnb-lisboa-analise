# 🏠 Análise do Mercado de Aluguéis em Lisboa com Dados do Airbnb

Este projeto analisa dados do **Airbnb em Lisboa**, explorando preços, tipos de acomodações, disponibilidade por região e até aplicando modelos preditivos para prever valores.  
Além da análise exploratória, foram adicionados **mapas interativos** e um **dashboard dinâmico** para tornar os insights mais acessíveis.

---

## 👨‍💻 Autor
**Lisandro Almeida Viana**
 
---

## 🎯 Objetivos do Projeto
- Analisar a **distribuição de preços** dos imóveis.  
- Comparar **tipos de acomodações** e seus valores médios.  
- Identificar os **bairros mais relevantes** em termos de oferta.  
- Avaliar fatores que influenciam os preços.  
- Criar **modelos preditivos** de preço.  
- Construir **mapas interativos**.  
- Desenvolver um **dashboard exploratório**.  

---

## ❓ Perguntas que o Projeto Ajuda a Responder
- Qual o preço médio dos imóveis por tipo de acomodação?  
- Quais bairros concentram mais imóveis disponíveis?  
- Quais fatores mais influenciam o preço?  
- É possível prever o preço com base nas características do imóvel?  
- Como um novo anfitrião pode se posicionar melhor no mercado?  

---

## 📊 Ferramentas Utilizadas
- **Python**  
- **Pandas / NumPy**  
- **Matplotlib / Seaborn / Plotly**  
- **Scikit-learn**  
- **Folium**  
- **Streamlit**  
- **Jupyter Notebook**

---

## 📁 Fonte dos Dados
Dataset público disponível no [Kaggle](https://www.kaggle.com/datasets/oipila/airbnblisbon), com informações detalhadas sobre imóveis anunciados no Airbnb em Lisboa.

---

## 🔍 Principais Descobertas
- 💰 A maioria das diárias está abaixo de **€1500** (com outliers de imóveis de luxo).  
- 🏠 **Apartamentos inteiros** são significativamente mais caros que quartos privados/compartilhados.  
- 📍 Alguns bairros concentram muito mais ofertas, indicando alta procura/concorrência.  
- 🔍 **Tipo de imóvel** e **localização** são fatores cruciais para o preço.  
- 🤖 Modelos preditivos mostram que técnicas como **Random Forest** têm melhor performance que a regressão linear simples.  

---

## 🚀 Funcionalidades Extras
### 1. Modelos Preditivos Avançados
- **Decision Tree** e **Random Forest** aplicados para previsão de preços.  
- Métricas avaliadas: R², RMSE, MAE.  
- Random Forest apresentou melhor desempenho.  

### 2. Mapas Interativos
- Criados com **Folium**, permitindo explorar preços no mapa de Lisboa.  
- Inclui **mapa de calor** e **mapa de pontos coloridos**.  
👉 [Mapa interativo (HTML)](mapa_precos_lisboa.html)

### 3. Dashboard Interativo
- Desenvolvido com **Streamlit**.  
- Permite filtrar por bairro, tipo de acomodação e faixa de preço.  
- Inclui **histograma**, **boxplot** e **mapa interativo**.  
👉 [Rodar o Dashboard](app_streamlit.py)

---

## 📌 Estrutura do Projeto
```
📂 Airbnb-Lisboa
 ┣ 📜 README.md
 ┣ 📜 listings_amostra.csv      # Dataset de amostra
 ┣ 📓 analise_airbnb_lisboa_v2.ipynb   # Notebook atualizado com análises
 ┣ 📜 app_streamlit.py          # Dashboard interativo em Streamlit
 ┣ 📜 mapa_precos_lisboa.html   # Mapa interativo (Folium)
```

---

## 🔧 Como Executar Localmente
1. Clone o repositório:  
   ```bash
   git clone https://github.com/seuusuario/airbnb-lisboa.git
   cd airbnb-lisboa
   ```

2. Instale dependências:  
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o notebook no Jupyter/Colab ou rode o dashboard:  
   ```bash
   streamlit run app_streamlit.py
   ```

---

## 📌 Próximos Passos
- Testar modelos avançados como **XGBoost** e **LightGBM**.  
- Criar visualizações geográficas ainda mais ricas.  
- Publicar o dashboard em **Streamlit Cloud** ou **Hugging Face Spaces**.  

---

✍️ **Autor:** Lisandro Almeida Viana  
📌 Projeto desenvolvido para portfólio em Ciência de Dados.  
