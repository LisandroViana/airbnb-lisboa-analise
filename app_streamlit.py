import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Airbnb Lisboa — Dashboard", layout="wide")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Função para limpar e converter preço
    def parse_price(s):
        if pd.isna(s):
            return np.nan
        if isinstance(s, (int, float)):
            return float(s)
        s = str(s)
        for ch in ['€', '$', 'R$', ',', ' ']:
            s = s.replace(ch, '')
        s = s.replace('.', '') if s.count('.') > 1 else s
        try:
            return float(s)
        except:
            s_alt = s.replace('.', '').replace(',', '.')
            try:
                return float(s_alt)
            except:
                return np.nan
    if 'price' in df.columns and 'price_num' not in df.columns:
        df['price_num'] = df['price'].apply(parse_price)
    return df

# 👉 Ajuste o caminho para o seu CSV
DATA_PATH = "listings_amostra.csv"
df = load_data(DATA_PATH)

st.title("🏠 Airbnb Lisboa — Dashboard Interativo")
st.markdown("Explore preços, bairros e tipos de acomodações (dataset de amostra).")

# -------------------- FILTROS --------------------
col1, col2, col3 = st.columns(3)
with col1:
    bairros = sorted([c for c in df.get('neighbourhood_cleansed', df.get('neighbourhood', pd.Series())).dropna().unique()]) if ('neighbourhood_cleansed' in df.columns or 'neighbourhood' in df.columns) else []
    bairro = st.selectbox("Bairro", options=["(Todos)"] + bairros)
with col2:
    tipos = sorted(df['room_type'].dropna().unique()) if 'room_type' in df.columns else []
    tipo = st.selectbox("Tipo de acomodação", options=["(Todos)"] + tipos)
with col3:
    max_preco = float(np.nanpercentile(df['price_num'], 99)) if 'price_num' in df.columns else None
    if max_preco:
        limite = st.slider("Preço máximo (filtrar)", min_value=0.0, max_value=max_preco, value=max_preco)

df_f = df.copy()
if bairro != "(Todos)":
    col_bairro = 'neighbourhood_cleansed' if 'neighbourhood_cleansed' in df_f.columns else 'neighbourhood'
    df_f = df_f[df_f[col_bairro] == bairro]
if tipo != "(Todos)" and 'room_type' in df_f.columns:
    df_f = df_f[df_f['room_type'] == tipo]
if 'price_num' in df_f.columns and max_preco:
    df_f = df_f[df_f['price_num'] <= limite]

# -------------------- GRÁFICOS --------------------
c1, c2 = st.columns([1, 1])
with c1:
    if 'price_num' in df_f.columns:
        fig = px.histogram(df_f, x='price_num', nbins=50, title="Distribuição de Preços (filtrada)")
        st.plotly_chart(fig, use_container_width=True)
with c2:
    if 'room_type' in df_f.columns and 'price_num' in df_f.columns:
        fig2 = px.box(df_f, x='room_type', y='price_num', title="Preço por Tipo de Acomodação")
        st.plotly_chart(fig2, use_container_width=True)

# -------------------- MAPA --------------------
st.subheader("Mapa Interativo")
if {'latitude', 'longitude'}.issubset(df_f.columns):
    df_map = df_f[['latitude', 'longitude', 'price_num']].dropna()
    center = [38.7223, -9.1393]  # Centro de Lisboa
    m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")
    if len(df_map) > 0:
        HeatMap(df_map[['latitude', 'longitude', 'price_num']].values.tolist(), radius=12, blur=18, max_zoom=13).add_to(m)
    st_folium(m, width=None, height=520)
else:
    st.info("Dataset sem colunas de latitude/longitude para o mapa.")
