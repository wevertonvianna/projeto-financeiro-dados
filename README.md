# 📊 Pipeline Analítico de Ativos da B3

Pipeline prático de Engenharia e Análise de Dados desenvolvido para extração, processamento colunar e visualização interativa de indicadores do mercado financeiro brasileiro.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem base do projeto.
- **`uv`**: Gerenciador ultrarrápido de pacotes e ambientes virtuais.
- **Yahoo Finance API (`yfinance`)**: Fonte de dados brutos de cotações históricas.
- **Pandas**: Limpeza, estruturação de dados e cálculos de variação percentual.
- **DuckDB**: Banco de dados SQL analítico embarcado (in-process) para execução de consultas de alta velocidade sobre arquivos Parquet.
- **Streamlit & Plotly**: Construção da aplicação web interativa e gráficos analíticos.

---

## 🏗️ Estrutura do Projeto

```text
projeto-financeiro-dados/
├── data/
│   ├── raw/                 # Armazenamento de dados brutos
│   └── processed/           # Camada analítica otimizada (Parquet)
├── src/
│   ├── 01_limpeza.py        # Ingestão e ETL de cotações da B3
│   ├── 02_analise_sql.py    # Agregações e métricas de risco via DuckDB SQL
│   └── 03_dashboard.py      # Aplicação web e dashboard no Streamlit
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação do repositório

```

## ⚡ Como Executar com o UV

# Clone o repositório

git clone [https://github.com/seu-usuario/projeto-financeiro-dados.git](https://github.com/seu-usuario/projeto-financeiro-dados.git)
cd projeto-financeiro-dados

# Criar o ambiente virtual com uv

uv venv

# Ativar o ambiente virtual

## No Windows (PowerShell):

.venv\Scripts\activate

## No Linux/macOS:

source .venv/bin/activate

# Instalar as dependências via uv

uv pip install -r requirements.txt

### 2. Execução do Pipeline

Execute os scripts em sequência usando o `uv run`:

#### Passo A: Ingestão e Tratamento de Dados (ETL)

Baixa as cotações, calcula os retornos diários e gera o arquivo `cotacoes.parquet`:

```bash
uv run python src/01_limpeza.py

```

#### Passo B: Análise Analítica via DuckDB (SQL)

Roda consultas SQL de volatilidade e médias de preço direto no Parquet:

```bash
uv run python src/02_analise_sql.py

```

#### Passo C: Dashboard Interativo

Sobe a aplicação web com gráficos do Plotly no seu navegador (`http://localhost:8501`):

```bash
uv run streamlit run src/03_dashboard.py

```

---

## 📈 Resultados e Métricas Geradas

O pipeline gera automaticamente:

- **Histórico de Preços**: Séries temporais ajustadas com Média Móvel (MMA 21d).
- **Métricas de Risco**: Cálculo de volatilidade diária percentual (`STDDEV`) e retorno médio.
- **Distribuição de Retornos**: Histograma estatístico de variação percentual dos ativos.

```

```
