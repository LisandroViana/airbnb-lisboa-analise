
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Airbnb Lisboa — Dashboard (KPIs Simples)", layout="wide")

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
        for ch in ["€", "$", "R$", ",", " "]:
            s = s.replace(ch, "")
        s = s.replace(".", "") if s.count(".") > 1 else s
        try:
            return float(s)
        except:
            s_alt = s.replace(".", "").replace(",", ".")
            try:
                return float(s_alt)
            except:
                return np.nan
    if "price" in df.columns and "price_num" not in df.columns:
        df["price_num"] = df["price"].apply(parse_price)
    return df

# 👉 Ajuste o caminho para o seu CSV, se necessário
DATA_PATH = "listings_amostra.csv"
df = load_data(DATA_PATH)

st.title("🏠 Airbnb Lisboa — Dashboard Interativo (versão para leigos)")
st.markdown("Explore preços, bairros e tipos de acomodações. Indicadores simples no topo ajudam a entender o mercado rapidamente.")

# -------------------- FILTROS --------------------
col1, col2, col3 = st.columns(3)
with col1:
    if 'neighbourhood_cleansed' in df.columns:
        bairros_base = df['neighbourhood_cleansed']
        bairro_col = 'neighbourhood_cleansed'
    elif 'neighbourhood' in df.columns:
        bairros_base = df['neighbourhood']
        bairro_col = 'neighbourhood'
    else:
        bairros_base = pd.Series(dtype=object)
        bairro_col = None
    bairros = sorted([c for c in bairros_base.dropna().unique()]) if len(bairros_base) else []
    bairro = st.selectbox("Bairro", options=["(Todos)"] + bairros)
with col2:
    tipos = sorted(df['room_type'].dropna().unique()) if 'room_type' in df.columns else []
    tipo = st.selectbox("Tipo de acomodação", options=["(Todos)"] + tipos)
with col3:
    if 'price_num' in df.columns:
        try:
            max_preco = float(np.nanpercentile(df['price_num'], 99))
        except Exception:
            max_preco = float(np.nanmax(df['price_num']))
        limite = st.slider("Preço máximo (filtrar)", min_value=0.0, max_value=max_preco, value=max_preco)
    else:
        max_preco = None
        limite = None

# -------------------- APLICA FILTROS --------------------
df_f = df.copy()
if bairro_col and bairro != "(Todos)":
    df_f = df_f[df_f[bairro_col] == bairro]
if tipo != "(Todos)" and 'room_type' in df_f.columns:
    df_f = df_f[df_f['room_type'] == tipo]
if 'price_num' in df_f.columns and max_preco is not None:
    df_f = df_f[df_f['price_num'] <= limite]

# -------------------- KPIs SIMPLES --------------------
st.subheader("📊 Indicadores principais")

def fmt_money(v):
    if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
        return "—"
    return f"€ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def safe_stat(series, fn, default=None):
    try:
        val = fn(series.dropna()) if series is not None else default
        if pd.isna(val):
            return default
        return float(val)
    except Exception:
        return default

mean_price = safe_stat(df_f.get('price_num'), np.mean)
min_price  = safe_stat(df_f.get('price_num'), np.min)
max_price  = safe_stat(df_f.get('price_num'), np.max)
total_imoveis = int(len(df_f))
num_bairros = int(df_f[bairro_col].nunique()) if bairro_col and len(df_f) else 0
tipo_comum = df_f['room_type'].mode()[0] if 'room_type' in df_f.columns and len(df_f['room_type'].dropna()) else "—"

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Preço médio da diária", fmt_money(mean_price))
with k2:
    st.metric("Preço mínimo", fmt_money(min_price))
with k3:
    st.metric("Preço máximo", fmt_money(max_price))
with k4:
    st.metric("Total de imóveis", f"{total_imoveis:,}".replace(",", "."))
with k5:
    st.metric("Bairros representados", f"{num_bairros}")

st.caption(f"🏠 Tipo de acomodação mais comum: **{tipo_comum}**")

# -------------------- GRÁFICOS SIMPLES --------------------
st.markdown("### Visualizações rápidas")
c1, c2 = st.columns([1, 1])
with c1:
    if 'price_num' in df_f.columns and len(df_f):
        fig = px.histogram(df_f, x='price_num', nbins=50, title="Distribuição de Preços (após filtros)")
        fig.update_layout(xaxis_title="Preço (€)", yaxis_title="Número de Anúncios", bargap=0.1)
        fig.update_traces(marker_color='rgb(52, 152, 219)', marker_line_color='rgb(41, 128, 185)', marker_line_width=1)
        st.plotly_chart(fig, use_container_width=True)
with c2:
    if 'room_type' in df_f.columns and 'price_num' in df_f.columns and len(df_f):
        fig2 = px.bar(
            df_f.groupby('room_type')['price_num'].mean().reset_index(),
            x='room_type',
            y='price_num',
            color='room_type',
            title="Preço Médio por Tipo de Acomodação",
            labels={'price_num': 'Preço Médio (€)', 'room_type': 'Tipo de Acomodação'}
        )
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

# -------------------- RODAPÉ --------------------
st.markdown("---")
st.caption("Dica: ajuste os filtros no topo para ver os KPIs mudarem. Indicadores foram simplificados para leitura por não especialistas.")
