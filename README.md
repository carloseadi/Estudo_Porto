# 🚗 Análise Estratégica de Precificação e Posicionamento - Porto Seguro

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://estudoporto-casedash.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-00A1FC.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0+-3F4F75.svg?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E.svg?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🌐 **[Clique aqui para acessar o Dashboard Interativo Online](https://estudoporto-casedash.streamlit.app/)**

*Diagnóstico tarifário, modelagem preditiva de elasticidade e plano tático para atingimento da meta corporativa de 15% de conversão.*

</div>

---

## 📌 Sumário Executivo

Este projeto apresenta um estudo aprofundado de inteligência mercadológica e precificação para a divisão de **Novos Negócios (Auto)** da **Porto Seguro**. 

A partir de uma base com dados de cotações e vendas frente a **10 concorrentes do mercado** (com destaque para 4 congêneres diretas) no período de **Janeiro a Agosto**, foi desenvolvido um diagnóstico analítico e preditivo com foco em responder à pergunta executiva:

> **"O que a Porto Seguro precisa fazer para atingir a meta corporativa de 15% de conversão de vendas no mês?"**

---

## 🎯 Principais Descobertas & Big Numbers

<div align="center">

| Indicador | Produto 1 (Perfil Entrada) | Produto 2 (Perfil Alto) | Conclusão Estratégica |
| :--- | :---: | :---: | :--- |
| **Share de Cotações** | **72,4%** (856k cotações) | **67,6%** (545k cotações) | Dominância absoluta no topo de funil em ambos os perfis. |
| **Conversão Média Atual** | **12,54%** | **13,40%** | Forte tração, porém com gaps de -2,46 p.p. (P1) e -1,60 p.p. (P2). |
| **Posicionamento de Preço** | **+8,51% acima do mercado** | **+0,4% vs mercado** | P1 opera com prêmio acima do balizador; P2 já opera próximo à média. |
| **Prova Empírica (Julho)** | Conversão de 14,3% (menor gap) | **15,31% de Conversão (Meta Batida)** | Quando a Porto se posicionou a **-1,8% vs mercado**, a meta foi superada. |

</div>

### 💡 Fatos-Chave do Diagnóstico:
1. **O Cliente Quer a Porto (Força da Marca):** A Porto é líder destacada em cotações. O gargalo não é atratividade de marca, mas sim a calibragem tarifária de fechamento.
2. **Sensibilidade no Produto 1:** Opera historicamente R$ 241 acima do mercado (R$ 3.078 vs R$ 2.837), o que limita a conversão.
3. **Comprovação Prática no Produto 2:** Em Julho, o alinhamento de preço frente a congêneres agressivas impulsionou a conversão para **15,31%**, demonstrando que a companhia não precisa ser a mais barata, bastando estar alinhada ao mercado.

---

## 🧠 Metodologia e Racional Matemático

O dashboard utiliza técnicas avançadas de **Data Science e Machine Learning** para embasar a tomada de decisão:

```
                  ┌────────────────────────────────────────┐
                  │          Pesquisa de Mercado           │
                  │   (10 Concorrentes • Jan a Ago)        │
                  └───────────────────┬────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ Regressão Linear  │       │  Clusterização    │       │ Séries Temporais  │
│       (OLS)       │       │    (K-Means)      │       │   (Previsão SET)  │
├───────────────────┤       ├───────────────────┤       ├───────────────────┤
│ Equação da reta   │       │ Segmentação por   │       │ Tendência futura  │
│ para isolar meta  │       │ Preço x Volume    │       │ de mercado e      │
│ de 15% de vendas  │       │ em 3 clusters     │       │ esforço tarifário │
└───────────────────┘       └───────────────────┘       └───────────────────┘
```

1. **Regressão Linear Simples (OLS):** Mapeia a correlação entre a *Competitividade Relativa de Preço* e a *Taxa de Conversão*, permitindo calcular com precisão matemática o preço necessário para cruzar os 15%.
2. **Clusterização K-Means:** Agrupa automaticamente os concorrentes em 3 territórios (*Preço Médio/Volume Alto*, *Preço Baixo/Volume Baixo*, *Preço Alto/Volume Médio*), removendo achismos e vieses.
3. **Projeção de Séries Temporais:** Projeta a curva de preços do mercado para o mês seguinte (Setembro), evitando que a Cia conceda descontos estáticos excessivos caso o mercado se mova.
4. **Elasticidade-Preço da Demanda (Epd):** Mede a sensibilidade de volume a cada 1% de variação no prêmio.

---

## 📊 Estrutura e Navegação do Dashboard

O aplicativo foi construído com arquitetura sequencial por estados (`st.session_state`):

1. 🌟 **Tela 1: Capa (Splash Screen)**
   - Identidade visual oficial Porto Seguro, logo e slogan centralizados (*"Todo cuidado é Porto"*).
2. 📋 **Tela 2: Contexto & Desafio**
   - Apresentação das premissas da pesquisa mercadológica e dos objetivos executivos do estudo.
3. 📈 **Tela 3: Diagnóstico Executivo**
   - Big numbers de Share e Conversão + Storytelling dos 3 Pilares Estratégicos.
4. 🚀 **Tela 4: Dashboard Interativo Completo**
   - **Aba 1: Posicionamento de Mercado:** Análise temporal e gráficos de dispersão.
   - **Aba 2: Análise de Cluster:** Mapeamento espacial dos concorrentes via K-Means.
   - **Aba 3: Meta de 15% de Vendas:** Simulador interativo com ajuste dinâmico de prêmio.
   - **Aba 4: Cenário Simulado:** Comparativo visual de 5 cenários de precificação.
   - **Aba 5: Racional Matemático:** Explicação detalhada de todas as fórmulas e modelos.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** Streamlit
- **Análise & Manipulação de Dados:** Pandas, NumPy
- **Visualização de Dados:** Plotly Express & Plotly Graph Objects
- **Machine Learning & Estatística:** Scikit-Learn (K-Means, StandardScaler), NumPy Polyfit
- **Deploy:** Streamlit Community Cloud

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina (versão 3.10 ou superior).

### Passo a passo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/carloseadi/Estudo_Porto.git
   cd Estudo_Porto
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scriptsctivate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app_1.py
   ```

5. O dashboard abrirá automaticamente no seu navegador padrão no endereço `http://localhost:8501`.

---

## 👤 Autor

Desenvolvido por **Carlos Eduardo Isola**  
GitHub: [@carloseadi](https://github.com/carloseadi)  
Dashboard Online: [estudoporto-casedash.streamlit.app](https://estudoporto-casedash.streamlit.app/)
