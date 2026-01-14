import streamlit as st
import pandas as pd
import yfinance as yf

# Configuração da página para aproveitar melhor o espaço
st.set_page_config(layout="wide")

# 1. Carregamento de Dados
@st.cache_data
def carregar_dados(empresas):
    if not empresas:
        return pd.DataFrame()
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    # Ajustado para o ano atual (2026 conforme contexto)
    cotacoes_acao = dados_acao.history(start="2024-01-01", end="2026-01-14")
    return cotacoes_acao["Close"]

@st.cache_data
def carregar_tickers_acoes():
    try:
        base_tickers = pd.read_csv("IBOV.csv", sep=";", skiprows=2, encoding="latin1", skipfooter=2, engine="python")
        tickers = base_tickers.iloc[:, 0].dropna().astype(str).tolist()
        tickers = [item.strip() + ".SA" for item in tickers]
        return tickers
    except Exception:
        return []
    
@st.cache_data
def carregar_tickers_fiis():
    try:
        base_fiis = pd.read_csv("IFIX.csv", sep=";", skiprows=2, encoding="latin1", skipfooter=2, engine="python")
        tickers_fiis = base_fiis.iloc[:, 0].dropna().astype(str).tolist()
        tickers_fiis = [item.strip() + ".SA" for item in tickers_fiis]
        return tickers_fiis
    except Exception:
        return []

# --- Inicialização ---
tickers_ibov = carregar_tickers_acoes()
tickers_ifix = carregar_tickers_fiis()
tickers_disponiveis = sorted(list(set(tickers_ibov + tickers_ifix)))

st.title("📊 Dashboard de Performance: IBOV + IFIX")

# 2. Filtros na Lateral (Responsivos)
st.sidebar.header("Configurações da Carteira")
lista_ativos = st.sidebar.multiselect("Selecione seus ativos:", tickers_disponiveis)

# NOVO: Opção para o usuário colocar o valor da carteira
valor_investido_total = st.sidebar.number_input("Valor Total Investido (R$):", min_value=0.0, value=1000.0, step=100.0)

if not lista_ativos:
    st.warning("Selecione os ativos no menu lateral para começar.")
    st.stop()

# Carregar dados apenas dos ativos selecionados para otimizar
dados_todos = carregar_dados(lista_ativos)
dados_filtrados = dados_todos.copy()

# 3. Slider de Data
data_inicial = dados_filtrados.index.min().to_pydatetime()
data_final = dados_filtrados.index.max().to_pydatetime()

intervalo_data = st.sidebar.slider("Período de Análise", 
                                   min_value=data_inicial,
                                   max_value=data_final,
                                   value=(data_inicial, data_final),
                                   format="DD/MM/YYYY")

dados_filtrados = dados_filtrados.loc[intervalo_data[0]:intervalo_data[1]]

# 4. Gráfico Responsivo
st.subheader("Evolução das Cotações")
st.line_chart(dados_filtrados)

# 5. Cálculo de Performance
st.write("---")
st.subheader("Performance Individual e da Carteira")

# Criando colunas para métricas principais (Responsividade)
col1, col2 = st.columns(2)

carteira_rendimento_percentual = []
valor_por_ativo = valor_investido_total / len(lista_ativos)

texto_performance_ativos = ""

for ativo in lista_ativos:
    coluna_ativo = dados_filtrados[ativo].dropna()
    
    if not coluna_ativo.empty:
        # Cálculo: ((Final / Inicial) - 1)
        performance_ativo = (coluna_ativo.iloc[-1] / coluna_ativo.iloc[0]) - 1
        carteira_rendimento_percentual.append(performance_ativo)
        
        cor = "green" if performance_ativo >= 0 else "red"
        texto_performance_ativos += f"- {ativo}: :{cor}[{performance_ativo:.2%}]\n"

# 6. Exibição dos Resultados em Cards (Métricas)
if carteira_rendimento_percentual:
    # Média aritmética da performance dos ativos selecionados
    performance_media = sum(carteira_rendimento_percentual) / len(carteira_rendimento_percentual)
    valor_final_total = valor_investido_total * (1 + performance_media)
    lucro_prejuizo = valor_final_total - valor_investido_total

    with col1:
        st.metric("Performance Total", f"{performance_media:.2%}", delta=f"{performance_media:.2%}")
    
    with col2:
        st.metric("Valor Final Estimado", f"R$ {valor_final_total:,.2f}", delta=f"R$ {lucro_prejuizo:,.2f}")

    st.write("#### Detalhes por Ativo")
    st.markdown(texto_performance_ativos)

    st.info(f"O cálculo considera que o valor de **R$ {valor_investido_total:,.2f}** foi dividido igualmente entre os {len(lista_ativos)} ativos selecionados.")
