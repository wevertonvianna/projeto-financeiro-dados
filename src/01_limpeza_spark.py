import yfinance as yf
import pandas as pd
import os

def processar_dados():
    print("⏳ Baixando cotações do Yahoo Finance...")
    tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "B3SA3.SA"]
    df_raw = yf.download(tickers, start="2024-01-01", interval="1d")['Close']
    
    # Organizar para formato longo (Data, Ativo, Preco)
    df_reset = df_raw.reset_index().melt(id_vars=['Date'], var_name='ticker', value_name='preco')
    df_reset.dropna(inplace=True)
    df_reset['ticker'] = df_reset['ticker'].str.replace('.SA', '', regex=False)
    df_reset.rename(columns={'Date': 'data'}, inplace=True)
    
    # Ordenar por ativo e data para calcular a variação
    df_reset.sort_values(by=['ticker', 'data'], inplace=True)
    
    # Calculando variação diária percentual
    df_reset['preco_anterior'] = df_reset.groupby('ticker')['preco'].shift(1)
    df_reset['retorno_diario_pct'] = ((df_reset['preco'] - df_reset['preco_anterior']) / df_reset['preco_anterior']) * 100
    df_reset.dropna(subset=['retorno_diario_pct'], inplace=True)

    # Salvar em arquivo Parquet unico
    os.makedirs("data/processed", exist_ok=True)
    caminho_parquet = "data/processed/cotacoes.parquet"
    
    df_reset.to_parquet(caminho_parquet, index=False)
    print(f"✅ Dados processados e salvos com sucesso em '{caminho_parquet}'!")

if __name__ == "__main__":
    processar_dados()