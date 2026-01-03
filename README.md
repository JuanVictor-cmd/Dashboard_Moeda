# 📊 Análise de Ações e FIIs (IBOV + IFIX)

## 📌 Visão Geral

Este projeto é uma aplicação interativa desenvolvida em **Python com Streamlit** para análise de **ações e fundos imobiliários (FIIs)** listados nos índices **IBOVESPA (IBOV)** e **IFIX**.

A aplicação permite ao usuário selecionar ativos, definir períodos de análise, visualizar gráficos de preços e calcular a performance individual e total de uma carteira de investimentos simulada.

Os dados financeiros são obtidos dinamicamente através da biblioteca **yFinance**, garantindo informações atualizadas diretamente do Yahoo Finance.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Streamlit** – Interface web interativa
* **Pandas** – Manipulação e análise de dados
* **yFinance** – Coleta de dados financeiros
* **CSV** – Base local de tickers (IBOV e IFIX)

---

## 📂 Estrutura de Arquivos

```
📁 projeto
 ├── app.py
 ├── IBOV.csv
 ├── IFIX.csv
 └── README.md
```

* **IBOV.csv**: Lista de ações do índice IBOVESPA
* **IFIX.csv**: Lista de FIIs do índice IFIX

---

## ⚙️ Funcionalidades

### 🔹 1. Carregamento de Dados

* Leitura automática dos tickers de ações e FIIs a partir de arquivos CSV
* Consolidação dos ativos em uma lista única
* Download dos preços históricos de fechamento (`Close`)
* Uso de cache (`@st.cache_data`) para melhorar performance

---

### 🔹 2. Filtros Interativos

* Seleção múltipla de ativos (ações e FIIs)
* Filtro de período por meio de slider de datas
* Validação para impedir execução sem ativos selecionados

---

### 🔹 3. Visualização Gráfica

* Gráfico de linhas exibindo a evolução do preço dos ativos selecionados
* Atualização automática conforme filtros aplicados

---

### 🔹 4. Cálculo de Performance Individual

Para cada ativo selecionado:

* Cálculo da variação percentual no período
* Simulação de investimento inicial de **R$ 1.000,00 por ativo**
* Destaque visual:

  * 🟢 Verde para performance positiva
  * 🔴 Vermelho para performance negativa

Fórmula utilizada:

```
Performance = (Preço Final / Preço Inicial) - 1
```

---

### 🔹 5. Performance Total da Carteira

* Soma do valor final de todos os ativos
* Cálculo da performance consolidada da carteira
* Exibição do resultado total com destaque visual

---

## 💡 Diferenciais do Projeto

* Integração automática entre **ações e FIIs**
* Interface simples, limpa e intuitiva
* Simulação prática de carteira de investimentos
* Código modular e fácil de manter
* Uso eficiente de cache para otimização

---

## 🚀 Possíveis Melhorias Futuras

* Inclusão de dividendos e rendimentos de FIIs
* Comparação com benchmarks (IBOV, IFIX, CDI)
* Exportação dos dados para Excel ou CSV
* Inclusão de métricas de risco (volatilidade, drawdown)
* Deploy da aplicação em nuvem (Streamlit Cloud)

---

## ▶️ Como Executar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Instale as dependências:

```bash
pip install streamlit pandas yfinance
```

3. Execute a aplicação:

```bash
streamlit run app.py
```

---

## 🧾 Conclusão

Este projeto demonstra a aplicação prática de **análise de dados financeiros**, unindo visualização interativa, manipulação de dados e consumo de APIs externas. É uma solução robusta e didática, ideal para portfólio profissional, estudos em finanças ou ciência de dados.

---

👨‍💻 Desenvolvido por **Juan Victor Almeida de Souza**
