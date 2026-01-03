import streamlit as st
import pandas as pd
import yfinance as yf

# 1. Carregamento de Dados
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    # Buscamos um período amplo para o cache e filtramos depois
    cotacoes_acao = dados_acao.history(start="2024-01-01", end="2026-01-01")
    return cotacoes_acao["Close"]

@st.cache_data
def carregar_tickers_acoes():
    try:
        base_tickers = pd.read_csv("IBOV.csv", sep=";", skiprows=2, encoding="latin1", skipfooter=2, engine="python")
        tickers = base_tickers.iloc[:, 0].dropna().astype(str).tolist()
        tickers = [item.strip() + ".SA" for item in tickers]
        return tickers
    except FileNotFoundError:
        st.error("Arquivo IBOV.csv não encontrado.")
        return []
    
@st.cache_data
def carregar_tickers_fiis():
    # Função para carregar os FIIs do arquivo IFIX.csv
    try:
        base_fiis = pd.read_csv("IFIX.csv", sep=";", skiprows=2, encoding="latin1", skipfooter=2, engine="python")
        tickers_fiis = base_fiis.iloc[:, 0].dropna().astype(str).tolist()
        tickers_fiis = [item.strip() + ".SA" for item in tickers_fiis]
        return tickers_fiis
    except FileNotFoundError:
        st.error("Arquivo IFIX.csv não encontrado.")
        return []

# --- Inicialização Combinada ---
# Carregamos ambas as listas e unimos em uma só
tickers_ibov = carregar_tickers_acoes()
tickers_ifix = carregar_tickers_fiis()
tickers_disponiveis = sorted(list(set(tickers_ibov + tickers_ifix))) # Remove duplicatas e ordena

# O download agora engloba Ações e FIIs
dados_todos = carregar_dados(tickers_disponiveis)

st.title("Análise de Ações e FIIs (IBOV + IFIX)")

# 2. Filtros na Lateral
st.sidebar.header("Filtros")
lista_ativos = st.sidebar.multiselect("Selecione os ativos (Ações ou FIIs):", dados_todos.columns)

if not lista_ativos:
    st.warning("Por favor, selecione ao menos um ativo no menu lateral.")
    st.stop()

# Filtrar dados antes de qualquer cálculo
dados_filtrados = dados_todos[lista_ativos].copy()

# 3. Slider de Data
data_inicial = dados_filtrados.index.min().to_pydatetime()
data_final = dados_filtrados.index.max().to_pydatetime()

intervalo_data = st.sidebar.slider("Selecione o período", 
                                   min_value=data_inicial,
                                   max_value=data_final,
                                   value=(data_inicial, data_final),
                                   format="DD/MM/YYYY")

# Aplicar filtro de data
dados_filtrados = dados_filtrados.loc[intervalo_data[0]:intervalo_data[1]]

# 4. Gráfico
st.line_chart(dados_filtrados)

# 5. Cálculo de Performance
st.write("### Performance dos Ativos")

texto_performance_ativos = ""
carteira_valores = []

for ativo in lista_ativos:
    coluna_ativo = dados_filtrados[ativo].dropna() # dropna evita erros com ativos novos
    
    if not coluna_ativo.empty:
        # Cálculo da performance (valor final / valor inicial - 1)
        performance_ativo = (coluna_ativo.iloc[-1] / coluna_ativo.iloc[0]) - 1
        
        # Simulação de carteira (R$ 1.000,00 iniciais por ativo)
        valor_final_ativo = 1000 * (1 + performance_ativo)
        carteira_valores.append(valor_final_ativo)
        
        # Formatação de cor
        cor = "green" if performance_ativo >= 0 else "red"
        texto_performance_ativos += f"- {ativo}: :{cor}[{performance_ativo:.2%}]\n"

# Exibir performance individual
st.markdown(texto_performance_ativos)

# 6. Performance Total da Carteira
if carteira_valores:
    total_inicial = len(lista_ativos) * 1000
    total_final = sum(carteira_valores)
    performance_total = (total_final / total_inicial) - 1

    cor_total = "green" if performance_total >= 0 else "red"

    st.write("---")
    st.markdown(f"**Performance Total da Carteira:** :{cor_total}[{performance_total:.2%}]")