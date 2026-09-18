import streamlit as st
import duckdb
import os
import subprocess
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.title("📊 Dashboard Analítico de Ativos da B3")
st.markdown("Análise de cotações e volatilidade processadas via **DuckDB + Parquet**.")

# Garante que o arquivo Parquet existe no servidor do Streamlit
if not os.path.exists('data/processed/cotacoes.parquet'):
    subprocess.run(["python", "src/01_limpeza.py"])

# 1. Carregar dados do Parquet via DuckDB
@st.cache_data
def carregar_dados():
    con = duckdb.connect()
    df = con.query("SELECT * FROM 'data/processed/cotacoes.parquet' ORDER BY data ASC").df()
    return df

df = carregar_dados()

# 2. Filtros na barra lateral (Sidebar)
st.sidebar.header("Filtros")
tickers_disponiveis = df['ticker'].unique()
ticker_selecionado = st.sidebar.selectbox("Selecione o Ativo:", tickers_disponiveis)

# Filtrar dados pelo ativo selecionado
df_ativo = df[df['ticker'] == ticker_selecionado].copy()

# Cálculo de Média Móvel de 21 dias no Pandas
df_ativo['mma_21'] = df_ativo['preco'].rolling(window=21).mean()

# 3. Métricas Principais (Cards Topo)
col1, col2, col3, col4 = st.columns(4)
preco_atual = df_ativo['preco'].iloc[-1]
preco_max = df_ativo['preco'].max()
preco_min = df_ativo['preco'].min()
volatilidade = df_ativo['retorno_diario_pct'].std()

col1.metric("Preço Atual", f"R$ {preco_atual:.2f}")
col2.metric("Máxima do Período", f"R$ {preco_max:.2f}")
col3.metric("Mínima do Período", f"R$ {preco_min:.2f}")
col4.metric("Volatilidade Diária", f"{volatilidade:.2f}%")

st.divider()

# 4. Gráficos Interativos (Plotly)
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader(f"Histórico de Preços - {ticker_selecionado}")
    fig_preco = go.Figure()
    fig_preco.add_trace(go.Scatter(x=df_ativo['data'], y=df_ativo['preco'], mode='lines', name='Preço Fechamento'))
    fig_preco.add_trace(go.Scatter(x=df_ativo['data'], y=df_ativo['mma_21'], mode='lines', name='Média Móvel (21d)', line=dict(dash='dash', color='orange')))
    fig_preco.update_layout(xaxis_title="Data", yaxis_title="Preço (R$)", template="plotly_dark")
    st.plotly_chart(fig_preco, use_container_width=True)

with col_graf2:
    st.subheader("Distribuição dos Retornos Diários (%)")
    fig_hist = px.histogram(df_ativo, x="retorno_diario_pct", nbins=40, title=f"Frequência de Retornos - {ticker_selecionado}", color_discrete_sequence=['#00CC96'])
    fig_hist.update_layout(xaxis_title="Retorno Diário (%)", yaxis_title="Contagem", template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)