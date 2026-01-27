import streamlit as st
import pandas as pd
import yfinance as yf

# Configuração da página
st.set_page_config(layout="wide", page_title="Análise de Carteira")

# 1. Funções de Carregamento (Mantidas com cache)
@st.cache_data
def carregar_dados(empresas):
    if not empresas: return pd.DataFrame()
    texto_tickers = " ".join(empresas)
    dados = yf.Tickers(texto_tickers)
    # Período ajustado conforme contexto
    cotacoes = dados.history(start="2024-01-01", end="2026-01-14")
    return cotacoes["Close"]

@st.cache_data
def carregar_tickers_totais():
    # Unindo carregamento de IBOV e IFIX
    lista = []
    for arq in ["IBOV.csv", "IFIX.csv"]:
        try:
            df = pd.read_csv(arq, sep=";", skiprows=2, encoding="latin1", skipfooter=2, engine="python")
            tickers = df.iloc[:, 0].dropna().astype(str).tolist()
            lista.extend([item.strip() + ".SA" for item in tickers])
        except: continue
    return sorted(list(set(lista)))

# --- Interface ---
tickers_disponiveis = carregar_tickers_totais()

st.title("📊 Carteira Personalizada")

# 2. Sidebar - Configuração de Ativos e Pesos
st.sidebar.header("1. Configuração da Carteira")
lista_ativos = st.sidebar.multiselect("Escolha os ativos:", tickers_disponiveis)

valor_investido_total = st.sidebar.number_input("Capital Total (R$):", min_value=0.0, value=1000.0, step=100.0)

# Dicionário para armazenar os pesos
pesos = {}
if lista_ativos:
    st.sidebar.write("---")
    st.sidebar.subheader("2. Definir Pesos (%)")
    
    peso_automatico = round(100 / len(lista_ativos), 2)
    
    for ativo in lista_ativos:
        pesos[ativo] = st.sidebar.number_input(f"Peso % em {ativo}", 
                                              min_value=0.0, 
                                              max_value=100.0, 
                                              value=peso_automatico)
    
    soma_pesos = sum(pesos.values())
    st.sidebar.write(f"**Soma Total: {soma_pesos:.2f}%**")
    
    if abs(soma_pesos - 100) > 0.1:
        st.sidebar.warning("⚠️ A soma dos pesos deve ser 100%")
        st.stop()

if not lista_ativos:
    st.info("Selecione os ativos na barra lateral para começar.")
    st.stop()

# 3. Processamento de Dados
dados_todos = carregar_dados(lista_ativos)

# Remove o fuso horário (timezone) para evitar o KeyError no slider
dados_todos.index = dados_todos.index.tz_localize(None)

data_inicial, data_final = dados_todos.index.min(), dados_todos.index.max()

# Agora o slider funcionará corretamente
intervalo_data = st.sidebar.slider(
    "Período", 
    min_value=data_inicial.to_pydatetime(), 
    max_value=data_final.to_pydatetime(), 
    value=(data_inicial.to_pydatetime(), data_final.to_pydatetime()),
    format="DD/MM/YYYY"
)

# Filtragem robusta usando as datas selecionadas
dados_filtrados = dados_todos.loc[intervalo_data[0]:intervalo_data[1]].copy()

# 4. Cálculos de Performance
st.subheader("Evolução da Carteira")
st.line_chart(dados_filtrados)

valor_final_carteira = 0
detalhes_performance = []

for ativo in lista_ativos:
    coluna = dados_filtrados[ativo].dropna()
    if not coluna.empty:
        perf_ativa = (coluna.iloc[-1] / coluna.iloc[0]) - 1
        
        # Cálculo baseado no peso definido pelo usuário
        valor_alocado = valor_investido_total * (pesos[ativo] / 100)
        valor_final_ativo = valor_alocado * (1 + perf_ativa)
        valor_final_carteira += valor_final_ativo
        
        detalhes_performance.append({
            "Ativo": ativo,
            "Peso": f"{pesos[ativo]}%",
            "Performance": perf_ativa,
            "Valor Final": valor_final_ativo
        })

# 5. Dashboard de Resultados
perf_total_global = (valor_final_carteira / valor_investido_total) - 1
lucro_prejuizo_total = valor_final_carteira - valor_investido_total

m1, m2, m3 = st.columns(3)
m1.metric("Investimento Inicial", f"R$ {valor_investido_total:,.2f}")
m2.metric("Valor Final da Carteira", f"R$ {valor_final_carteira:,.2f}", f"{perf_total_global:.2%}")
m3.metric("Lucro/Prejuízo", f"R$ {lucro_prejuizo_total:,.2f}", f"{perf_total_global:.2%}")

# Tabela Detalhada (Responsiva)
st.write("### Detalhamento por Ativo")
df_resumo = pd.DataFrame(detalhes_performance)
df_resumo["Performance"] = df_resumo["Performance"].map("{:.2%}".format)
df_resumo["Valor Final"] = df_resumo["Valor Final"].map("R$ {:,.2f}".format)
st.table(df_resumo)
