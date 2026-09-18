import duckdb

def analisar_risco_retorno():
    # Consulta SQL direta no arquivo Parquet
    query = """
    SELECT 
        ticker,
        ROUND(AVG(preco), 2) AS preco_medio,
        ROUND(MAX(preco), 2) AS preco_maximo,
        ROUND(MIN(preco), 2) AS preco_minimo,
        ROUND(STDDEV(retorno_diario_pct), 2) AS volatilidade_pct,
        ROUND(AVG(retorno_diario_pct), 3) AS retorno_medio_diario_pct
    FROM 'data/processed/cotacoes.parquet'
    GROUP BY ticker
    ORDER BY volatilidade_pct DESC;
    """

    resultado = duckdb.query(query).df()
    
    print("\n=======================================================")
    print("📊 RELATÓRIO FINANCEIRO (Pandas + DuckDB SQL)")
    print("=======================================================")
    print(resultado)

if __name__ == "__main__":
    analisar_risco_retorno()