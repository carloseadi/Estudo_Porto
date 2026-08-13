# 🚗 Análise Estratégica de Precificação e Posicionamento - Porto Seguro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este projeto apresenta um diagnóstico executivo e preditivo de precificação para novos negócios da **Porto Seguro** frente a congêneres e mercado geral, visando atingir a meta corporativa de **15% de conversão de vendas**.

---

## 📌 Principais Destaques do Estudo

1. **Dominância de Cotações:** A Porto domina o topo de funil com **72,4% de share no Produto 1** e **67,6% no Produto 2**.
2. **Diagnóstico Tarifário:**
   - **Produto 1 (Entrada):** Opera em média **+8,51% acima do mercado**, limitando o fechamento a 12,54% (gap de -2,46 p.p.).
   - **Produto 2 (Perfil Alto):** Histórico comprovou atingimento da meta em Julho (**15,31% de conversão**) ao se posicionar **-1,8% vs mercado**.
3. **Modelagem Matemática e Preditiva:**
   - **Regressão Linear (OLS):** Mapeamento da curva de elasticidade-preço da demanda.
   - **Clusterização K-Means:** Agrupamento de competidores por Preço Médio e Volume.
   - **Projeção de Séries Temporais:** Estimativa de prêmios de mercado futuros para Setembro.

---

## 🛠️ Como Executar Localmente

### 1. Clonar o repositório
`ash
git clone https://github.com/carloseadi/Estudo_Porto.git
cd Estudo_Porto
`

### 2. Instalar as dependências
`ash
pip install -r requirements.txt
`

### 3. Rodar o Dashboard
`ash
streamlit run app_1.py
`

---

## 🚀 Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io/).
2. Conecte sua conta do GitHub.
3. Selecione o repositório carloseadi/Estudo_Porto.
4. Defina o **Main file path** como pp_1.py.
5. Clique em **Deploy**!
