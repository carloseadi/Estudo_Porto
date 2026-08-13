import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuração da página
st.set_page_config(page_title="Case - Novos Negócios", layout="wide", page_icon="🚗")

# Função para carregar os dados
@st.cache_data
def load_data():
    file_path = "Case Contratação - Dados.xlsx"
    df = pd.read_excel(file_path)
    
    # Renomeando as colunas para facilitar o uso e remover caracteres especiais
    new_cols = [
        'Periodo', 'Perfil_Cliente', 'Vendas', 
        'Preco_Cia_Interna', 'Preco_Concorrente_1', 'Preco_Concorrente_2', 'Preco_Concorrente_3', 'Preco_Concorrente_4', 'Preco_Mercado',
        'Cotacoes_Cia_Interna', 'Cotacoes_Concorrente_1', 'Cotacoes_Concorrente_2', 'Cotacoes_Concorrente_3', 'Cotacoes_Concorrente_4', 'Cotacoes_Mercado'
    ]
    df.columns = new_cols
    
    # Adicionando métricas calculadas
    df['Competitividade_Preco'] = df['Preco_Cia_Interna'] / df['Preco_Mercado'] - 1 # % acima/abaixo do mercado
    df['Share_Cotacoes'] = df['Cotacoes_Cia_Interna'] / df['Cotacoes_Mercado']
    
    # Ordenar período cronologicamente
    periodo_ordem = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
    df['Mes_Num'] = df['Periodo'].map(periodo_ordem)
    df = df.sort_values(['Mes_Num', 'Perfil_Cliente'])
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo excel: {e}")
    st.stop()

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.image("Porto_Holding_RGB_Horizontal-Cyan.webp")
st.sidebar.title("Filtros")

perfil_selecionado = st.sidebar.selectbox("Perfil de Cliente", ["Todos", "Perfil 1", "Perfil 2"])
periodo_selecionado = st.sidebar.multiselect("Período", df['Periodo'].unique(), default=df['Periodo'].unique())

# Aplicar filtros
df_filtered = df[df['Periodo'].isin(periodo_selecionado)]
if perfil_selecionado != "Todos":
    perfil_val = int(perfil_selecionado.replace("Perfil ", ""))
    df_filtered = df_filtered[df_filtered['Perfil_Cliente'] == perfil_val]

# ==========================================
# HEADER
# ==========================================
st.title("🚗 Análise de Posicionamento - Novos Negócios")
st.markdown("---")

if df_filtered.empty:
    st.warning("Selecione pelo menos um período nos filtros.")
    st.stop()

# ==========================================
# TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Posicionamento de Mercado", "🧩 Análise de Cluster", "📈 Meta de 15% de Vendas", "🔮 Cenário Simulado", "🧠 Racional Matemático"])

with tab1:
    st.header("Análise de Posicionamento de Mercado")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_price_cia = df_filtered['Preco_Cia_Interna'].mean()
        st.metric("Preço Médio Cia", f"R$ {avg_price_cia:,.2f}")
    with col2:
        avg_price_mkt = df_filtered['Preco_Mercado'].mean()
        delta_mkt = (avg_price_cia / avg_price_mkt) - 1 if avg_price_mkt > 0 else 0
        st.metric("Preço Médio Mercado", f"R$ {avg_price_mkt:,.2f}", f"{delta_mkt:.1%} vs Cia", delta_color="inverse")
    with col3:
        avg_vendas = df_filtered['Vendas'].mean()
        st.metric("Média de Vendas", f"{avg_vendas:.2%}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos
    col_chart1, col_chart_mid, col_chart2 = st.columns(3)
    
    with col_chart1:
        st.subheader("Evolução do Preço Médio")
        
        opcao_visao = st.radio("Visão de Comparativo:", ["Porto vs Mercado (Apenas)", "Visão Geral (Todos os Players)"], horizontal=True)
        cols_price = ['Preco_Cia_Interna', 'Preco_Mercado', 'Preco_Concorrente_1', 'Preco_Concorrente_2', 'Preco_Concorrente_3', 'Preco_Concorrente_4']
        cols_plot = ['Preco_Cia_Interna', 'Preco_Mercado'] if opcao_visao == "Porto vs Mercado (Apenas)" else cols_price
        
        periodo_ordem = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
        df_price = df_filtered.groupby('Periodo')[cols_price].mean().reset_index()
        # Ordenação cronológica
        df_price['Mes_Num'] = df_price['Periodo'].map(periodo_ordem)
        df_price = df_price.sort_values('Mes_Num')
        
        # --- Lógica de Previsão (Setembro) ---
        if len(df_price) >= 3:
            ultimo_mes_num = df_price['Mes_Num'].max()
            mes_futuro = ultimo_mes_num + 1
            ordem_periodo_rev = {v: k for k, v in periodo_ordem.items()}
            mes_futuro_str = ordem_periodo_rev.get(mes_futuro, f"Mês {mes_futuro}")
            
            nova_linha_dict = {'Periodo': mes_futuro_str, 'Mes_Num': mes_futuro}
            for col in cols_price:
                z_trend = np.polyfit(df_price['Mes_Num'], df_price[col], 1)
                nova_linha_dict[col] = z_trend[0] * mes_futuro + z_trend[1]
                
            nova_linha = pd.DataFrame([nova_linha_dict])
            df_price = pd.concat([df_price, nova_linha], ignore_index=True)
            ultimo_mes_hist = ordem_periodo_rev.get(ultimo_mes_num, "AGO")
        else:
            ultimo_mes_hist = None
            
        # Mapeamento de cores fixas
        color_map = {
            'Preco_Cia_Interna': '#00A1FC',
            'Preco_Mercado': '#8a8d90',
            'Preco_Concorrente_1': '#F2A900',
            'Preco_Concorrente_2': '#E5004D',
            'Preco_Concorrente_3': '#00B050',
            'Preco_Concorrente_4': '#8b4513'
        }
        
        fig_price = px.line(df_price, x='Periodo', y=cols_plot,
                            labels={'value': 'Preço (R$)', 'variable': 'Player', 'Periodo': 'Mês'},
                            title='Evolução do Preço Médio (com Previsão)', markers=True, 
                            color_discrete_map=color_map)
                            
        # Adicionar a linha vertical cortando o eixo Y (separando histórico da previsão)
        if ultimo_mes_hist and len(df_price) >= 3:
            fig_price.add_vline(x=len(df_price) - 1.5, line_dash="dash", line_color="#c2c4c6")
            
        newnames = {'Preco_Cia_Interna': 'Porto', 'Preco_Mercado': 'Mercado Médio', 
                    'Preco_Concorrente_1': 'Congênere 1', 'Preco_Concorrente_2': 'Congênere 2', 
                    'Preco_Concorrente_3': 'Congênere 3', 'Preco_Concorrente_4': 'Congênere 4'}
        fig_price.for_each_trace(lambda t: t.update(name = newnames.get(t.name, t.name), legendgroup = newnames.get(t.name, t.name)))
        
        fig_price.update_traces(connectgaps=False)
        fig_price.update_layout(
            yaxis_tickprefix='R$ ',
            legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_price, width="stretch")
        
    with col_chart_mid:
        st.subheader("Conversão de Vendas (%)")
        st.markdown("<div style='height: 68px;'></div>", unsafe_allow_html=True)
        
        df_vendas = df_filtered.groupby('Periodo')['Vendas'].mean().reset_index()
        df_vendas['Mes_Num'] = df_vendas['Periodo'].map(periodo_ordem)
        df_vendas = df_vendas.sort_values('Mes_Num')
        
        # --- Lógica de Previsão de Vendas (Setembro) ---
        if len(df_vendas) >= 3:
            ultimo_mes_num = df_vendas['Mes_Num'].max()
            mes_futuro = ultimo_mes_num + 1
            ordem_periodo_rev = {v: k for k, v in periodo_ordem.items()}
            mes_futuro_str = ordem_periodo_rev.get(mes_futuro, f"Mês {mes_futuro}")
            
            z_trend_v = np.polyfit(df_vendas['Mes_Num'], df_vendas['Vendas'], 1)
            venda_futura = max(0, z_trend_v[0] * mes_futuro + z_trend_v[1])
            
            nova_linha_v = {'Periodo': mes_futuro_str, 'Mes_Num': mes_futuro, 'Vendas': venda_futura}
            df_vendas = pd.concat([df_vendas, pd.DataFrame([nova_linha_v])], ignore_index=True)
            ultimo_mes_hist_v = ordem_periodo_rev.get(ultimo_mes_num, "AGO")
        else:
            ultimo_mes_hist_v = None
            
        fig_vendas = px.line(df_vendas, x='Periodo', y='Vendas', markers=True,
                             title='Evolução do Fechamento (com Previsão)',
                             labels={'Vendas': 'Vendas (%)', 'Periodo': 'Mês'},
                             color_discrete_sequence=['#00B050'])
                             
        if ultimo_mes_hist_v and len(df_vendas) >= 3:
            fig_vendas.add_vline(x=len(df_vendas) - 1.5, line_dash="dash", line_color="#c2c4c6")
            
        fig_vendas.add_hline(y=0.15, line_dash="dash", line_color="#E5004D", annotation_text="Meta (15%)")
        
        fig_vendas.update_traces(connectgaps=False)
        fig_vendas.update_layout(
            yaxis_tickformat='.1%',
            legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_vendas, width="stretch")
        
    with col_chart2:
        st.subheader("Volume de Cotações (Porto vs Congêneres)")
        
        # Espaçador invisível para alinhar a altura com o botão de radio do gráfico ao lado
        st.markdown("<div style='height: 68px;'></div>", unsafe_allow_html=True)
        
        cols_cotacoes = ['Cotacoes_Cia_Interna', 'Cotacoes_Concorrente_1', 'Cotacoes_Concorrente_2', 'Cotacoes_Concorrente_3', 'Cotacoes_Concorrente_4']
        df_cot = df_filtered.groupby('Periodo')[cols_cotacoes].sum().reset_index()
        df_cot['Mes_Num'] = df_cot['Periodo'].map(periodo_ordem)
        df_cot = df_cot.sort_values('Mes_Num')
        
        # --- Lógica de Previsão de Cotações (Setembro) ---
        if len(df_cot) >= 3:
            ultimo_mes_num = df_cot['Mes_Num'].max()
            mes_futuro = ultimo_mes_num + 1
            ordem_periodo_rev = {v: k for k, v in periodo_ordem.items()}
            mes_futuro_str = ordem_periodo_rev.get(mes_futuro, f"Mês {mes_futuro}")
            
            nova_linha_cot = {'Periodo': mes_futuro_str, 'Mes_Num': mes_futuro}
            for col in cols_cotacoes:
                z_trend = np.polyfit(df_cot['Mes_Num'], df_cot[col], 1)
                nova_linha_cot[col] = max(0, z_trend[0] * mes_futuro + z_trend[1]) # Evitar cotação negativa
                
            df_cot = pd.concat([df_cot, pd.DataFrame([nova_linha_cot])], ignore_index=True)
            ultimo_mes_hist_cot = ordem_periodo_rev.get(ultimo_mes_num, "AGO")
        else:
            ultimo_mes_hist_cot = None
        
        fig_cot = px.bar(df_cot, x='Periodo', y=cols_cotacoes, barmode='group',
                         labels={'value': 'Volume de Cotações', 'variable': 'Porto/Congênere', 'Periodo': 'Mês'},
                         title='Distribuição de Cotações no Mês (com Previsão)',
                         color_discrete_sequence=['#00A1FC', '#5c6368', '#8a8d90', '#a0a3a5', '#c2c4c6'])
                         
        if ultimo_mes_hist_cot and len(df_cot) >= 3:
            fig_cot.add_vline(x=len(df_cot) - 1.5, line_dash="dash", line_color="#c2c4c6")
            
        newnames_cot = {'Cotacoes_Cia_Interna': 'Porto', 'Cotacoes_Concorrente_1': 'Congênere 1', 'Cotacoes_Concorrente_2': 'Congênere 2', 'Cotacoes_Concorrente_3': 'Congênere 3', 'Cotacoes_Concorrente_4': 'Congênere 4'}
        fig_cot.for_each_trace(lambda t: t.update(name = newnames_cot.get(t.name, t.name), legendgroup = newnames_cot.get(t.name, t.name)))
        
        fig_cot.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_cot, width="stretch")
        
    st.markdown("---")
    st.subheader("Relação: Preço vs Volume de Vendas")
    
    # Adicionando o grafico de dispersao
    fig_scatter = px.scatter(df_filtered, x='Competitividade_Preco', y='Vendas', 
                             color='Perfil_Cliente', text='Periodo', hover_data=['Preco_Cia_Interna', 'Preco_Mercado'],
                             labels={'Competitividade_Preco': 'Preço Porto vs Mercado (%)', 'Vendas': 'Vendas (%)'},
                             title='Impacto do Posicionamento de Preço na Conversão de Vendas',
                             color_discrete_sequence=['#00A1FC', '#004691'])
                             
    fig_scatter.update_traces(textposition='top center')
                             
    # --- Adicionar Ponto de Previsão (Próximo Mês) ---
    if len(df_filtered) >= 3:
        try:
            periodo_ordem = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
            df_price_t1 = df_filtered.groupby('Periodo')[['Preco_Cia_Interna', 'Preco_Mercado']].mean().reset_index()
            df_price_t1['Mes_Num'] = df_price_t1['Periodo'].map(periodo_ordem)
            df_price_t1 = df_price_t1.sort_values('Mes_Num')
            
            z_trend_mkt = np.polyfit(df_price_t1['Mes_Num'], df_price_t1['Preco_Mercado'], 1)
            z_trend_cia = np.polyfit(df_price_t1['Mes_Num'], df_price_t1['Preco_Cia_Interna'], 1)
            
            ultimo_mes_num = df_price_t1['Mes_Num'].max()
            mes_futuro = ultimo_mes_num + 1
            
            ordem_periodo_rev = {v: k for k, v in periodo_ordem.items()}
            mes_futuro_str = ordem_periodo_rev.get(mes_futuro, f"Mês {mes_futuro}")
            
            preco_mercado_set = z_trend_mkt[0] * mes_futuro + z_trend_mkt[1]
            preco_cia_set = z_trend_cia[0] * mes_futuro + z_trend_cia[1]
            
            comp_set = (preco_cia_set / preco_mercado_set) - 1
            
            # Calcular a previsão de vendas usando a elasticidade geral
            x_hist = df_filtered['Competitividade_Preco']
            y_hist = df_filtered['Vendas']
            z_elasticidade = np.polyfit(x_hist, y_hist, 1)
            
            vendas_set = z_elasticidade[0] * comp_set + z_elasticidade[1]
            label_prev = f'Projeção {mes_futuro_str}'
            
            fig_scatter.add_scatter(x=[comp_set], y=[vendas_set], mode='markers+text', 
                                    marker=dict(size=18, color='#F2A900', symbol='star', line=dict(width=1, color='DarkSlateGrey')),
                                    name=label_prev, text=[f'⭐ {label_prev}'], textposition='top center')
        except Exception as e:
            pass
            
    fig_scatter.update_layout(xaxis_tickformat='.1%', yaxis_tickformat='.1%')
    # Garantir que o eixo Y expanda até a meta de 15% e adicionar linha alvo
    fig_scatter.update_yaxes(range=[df_filtered['Vendas'].min() * 0.95, max(df_filtered['Vendas'].max(), 0.15) * 1.05])
    fig_scatter.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
    
    st.plotly_chart(fig_scatter, width="stretch")
    st.info("💡 **Insight de Posicionamento:** O gráfico acima ilustra a sensibilidade de preço. Observe se em pontos onde o preço da Porto é mais competitivo (valores menores ou negativos no eixo X) o percentual de Vendas (eixo Y) tende a ser maior.")

with tab2:
    st.header("Análise de Cluster (Agrupamento das Seguradoras)")
    st.markdown("Nesta seção utilizamos K-Means para agrupar as **Seguradoras** (Porto e Congêneres) de acordo com o **Preço Médio** e o **Volume Total de Cotações**. O objetivo é entender quem são os nossos concorrentes diretos no mesmo 'grupo' de atuação.")
    
    # Preparar dados agregados por seguradora
    companies = ['Cia_Interna', 'Concorrente_1', 'Concorrente_2', 'Concorrente_3', 'Concorrente_4']
    company_data = []
    
    for comp in companies:
        preco_col = f'Preco_{comp}'
        cot_col = f'Cotacoes_{comp}'
        
        # Calcular média de preço e soma de cotações para o período filtrado
        mean_preco = df_filtered[preco_col].mean()
        sum_cot = df_filtered[cot_col].sum()
        
        # Nome amigável para o gráfico
        nome = "Porto" if comp == 'Cia_Interna' else comp.replace('_', ' ').replace('Concorrente', 'Congênere')
        
        company_data.append({'Seguradora': nome, 'Preco_Medio': mean_preco, 'Volume_Cotacoes': sum_cot})
        
    df_comp = pd.DataFrame(company_data)
    
    if df_comp['Preco_Medio'].notna().all() and not df_comp.empty:
        # Algoritmo de Cluster
        features = df_comp[['Preco_Medio', 'Volume_Cotacoes']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Como temos 5 seguradoras, dividimos em 3 grupos para mapear nichos (Preço e Volume)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters_raw = kmeans.fit_predict(features_scaled)
        df_comp['Cluster_ID'] = clusters_raw
        
        # Calcular médias globais para classificar dinamicamente os clusters
        overall_preco = df_comp['Preco_Medio'].mean()
        overall_vol = df_comp['Volume_Cotacoes'].mean()
        
        cluster_means = df_comp.groupby('Cluster_ID')[['Preco_Medio', 'Volume_Cotacoes']].mean()
        
        cluster_labels = {}
        for cluster_id, row in cluster_means.iterrows():
            # Diferença percentual em relação à média geral do mercado (todas seguradoras)
            preco_diff = row['Preco_Medio'] / overall_preco - 1
            vol_diff = row['Volume_Cotacoes'] / overall_vol - 1
            
            p_label = "Alto" if preco_diff > 0.03 else ("Baixo" if preco_diff < -0.03 else "Médio")
            v_label = "Alto" if vol_diff > 0.15 else ("Baixo" if vol_diff < -0.15 else "Médio")
            
            cluster_labels[cluster_id] = f"Preço {p_label} / Volume {v_label}"
            
        df_comp['Cluster'] = df_comp['Cluster_ID'].map(cluster_labels)
        df_comp = df_comp.sort_values(by=['Volume_Cotacoes', 'Preco_Medio'], ascending=False)
        
        # Identificar onde a Porto está
        porto_cluster = df_comp[df_comp['Seguradora'] == 'Porto']['Cluster'].values[0]
        st.success(f"**Atenção:** A **Porto** foi classificada matematicamente junto aos congêneres do grupo: **{porto_cluster}**.")
        
        # Gráfico
        fig_cluster = px.scatter(df_comp, x='Preco_Medio', y='Volume_Cotacoes', 
                                 color='Cluster', text='Seguradora',
                                 labels={'Preco_Medio': 'Preço Médio Praticado (R$)', 'Volume_Cotacoes': 'Volume Total de Cotações'},
                                 title='Mapa de Competição: Em qual grupo cada Seguradora se encaixa?',
                                 color_discrete_sequence=['#00A1FC', '#F2A900', '#E5004D'])
        fig_cluster.update_traces(marker=dict(size=12), textposition='top center')
        fig_cluster.update_layout(xaxis_tickprefix='R$ ')
        
        st.plotly_chart(fig_cluster, width="stretch")
        
        st.info("💡 **Interpretação dos Grupos:** O K-Means avaliou o eixo X (Preço) e Y (Volume) e identificou quem 'briga' no mesmo território que nós. As empresas que estiverem no mesmo grupo da Porto são nossos concorrentes mais diretos nas características atuais de mercado. O que diferencia um cluster do outro aqui é, majoritariamente, a capacidade de gerar cotações e a política de precificação (Líderes de Volume costumam ter preços em uma faixa mais agressiva).")
    else:
        st.warning("Selecione períodos válidos nos filtros para que as seguradoras possam ser analisadas.")

with tab3:
    st.header("Plano de Ação: Atingir 15% de Vendas no Mês")
    st.markdown("O desafio é entender o que é preciso fazer para atingir **15% de vendas**. Abaixo, detalhamos a estratégia em três pilares fundamentais.")
    
    subtab1, subtab2, subtab3 = st.tabs(["📊 Cenário Histórico", "🔮 Previsão para Setembro", "📐 Elasticidade de Preço"])
    
    with subtab1:
        st.subheader("Simulador Baseado no Comportamento Histórico")
        st.markdown("Cálculo do preço ideal baseado estritamente na média histórica dos meses selecionados no filtro.")
        
        filtro_hist = st.radio("Selecione o recorte de tempo para esta simulação:", ["Histórico Completo", "Últimos 3 Meses", "Apenas Último Mês (Ex: Agosto)"], horizontal=True)
        
        if filtro_hist == "Últimos 3 Meses":
            meses_disp = sorted(df_filtered['Mes_Num'].unique())
            meses_alvo = meses_disp[-3:] if len(meses_disp) >= 3 else meses_disp
            df_sim_hist = df_filtered[df_filtered['Mes_Num'].isin(meses_alvo)]
        elif filtro_hist == "Apenas Último Mês (Ex: Agosto)":
            mes_alvo = df_filtered['Mes_Num'].max()
            df_sim_hist = df_filtered[df_filtered['Mes_Num'] == mes_alvo]
        else:
            df_sim_hist = df_filtered
            
        if len(df_sim_hist) > 0:
            # Para a regressão, precisamos de pelo menos 2 pontos. 
            # Se o filtro resultar em apenas 1 ponto (ex: Agosto com 1 perfil selecionado), 
            # usamos a elasticidade (tendência) do histórico completo como fallback.
            if len(df_sim_hist) >= 2:
                x_reg = df_sim_hist['Competitividade_Preco']
                y_reg = df_sim_hist['Vendas']
            else:
                x_reg = df_filtered['Competitividade_Preco']
                y_reg = df_filtered['Vendas']
            
            try:
                z = np.polyfit(x_reg, y_reg, 1)
                meta_vendas = 0.15
                preco_alvo_competitividade = (meta_vendas - z[1]) / z[0]
                
                st.info(f"De acordo com a linha de tendência estatística histórica, para atingir **15% de Vendas**, a relação do preço da Porto contra o Mercado deve ser de aproximadamente **{preco_alvo_competitividade:.1%}**.")
                
                col_sim1, col_sim2, col_sim3 = st.columns([2, 1.5, 1.2])
                with col_sim1:
                    mercado_simulado = st.number_input("Insira a estimativa de Preço Médio do Mercado (R$):", value=float(df_sim_hist['Preco_Mercado'].mean()), step=100.0)
                    preco_sugerido = mercado_simulado * (1 + preco_alvo_competitividade)
                    st.success(f"**Preço Médio Sugerido para a Porto:** R$ {preco_sugerido:,.2f}")
                    
                diferenca = preco_sugerido - df_sim_hist['Preco_Cia_Interna'].mean()
                fator_ajuste = diferenca / df_sim_hist['Preco_Cia_Interna'].mean()
                texto_diff = "Aumento" if diferenca > 0 else "Redução"
                
                with col_sim2:
                    st.metric("Ajuste Médio Necessário", f"R$ {diferenca:,.2f}", f"{texto_diff} vs médio praticado", delta_color="inverse" if diferenca < 0 else "normal")
                with col_sim3:
                    st.metric("Fator de Ajuste (%)", f"{fator_ajuste:+.2%}", "Ajuste na tarifa base", delta_color="inverse" if fator_ajuste < 0 else "normal")
                    
                # Gráfico interativo da curva de preço
                precos = np.linspace(mercado_simulado * 0.8, mercado_simulado * 1.2, 100)
                vendas_simuladas = z[0] * ((precos / mercado_simulado) - 1) + z[1]
                df_sim_curva1 = pd.DataFrame({'Preco': precos, 'Vendas': vendas_simuladas})
                
                fig_curva1 = px.line(df_sim_curva1, x='Preco', y='Vendas', 
                                     title='Simulador de Cenários: Impacto do Preço no Fechamento',
                                     labels={'Preco': 'Preço Simulado da Porto (R$)', 'Vendas': 'Fechamento Previsto (%)'},
                                     color_discrete_sequence=['#00A1FC'])
                fig_curva1.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
                fig_curva1.add_vline(x=preco_sugerido, line_dash="dot", line_color="#F2A900", annotation_text="Preço Alvo Sugerido")
                fig_curva1.update_layout(yaxis_tickformat='.1%', xaxis_tickprefix='R$ ', hovermode="x unified")
                st.plotly_chart(fig_curva1, width="stretch")
            except Exception as e:
                st.warning("Não foi possível calcular a projeção com a seleção atual.")
        else:
            st.warning("Não há dados suficientes no recorte selecionado.")
            
    with subtab2:
        st.subheader("Meta Aplicada na Previsão de Setembro")
        st.markdown("Cálculo do preço ideal **projetando a tendência matemática do mercado para Setembro**, garantindo uma decisão que olha para o futuro.")
        
        periodo_ordem_t3 = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
        df_trend_t3 = df_filtered.groupby('Periodo')[['Preco_Mercado']].mean().reset_index()
        df_trend_t3['Mes_Num'] = df_trend_t3['Periodo'].map(periodo_ordem_t3)
        df_trend_t3 = df_trend_t3.sort_values('Mes_Num')
        
        if len(df_trend_t3) >= 3 and len(df_filtered) > 2:
            x_hist = df_filtered['Competitividade_Preco']
            y_hist = df_filtered['Vendas']
            z_hist = np.polyfit(x_hist, y_hist, 1)
            preco_alvo_comp_set = (0.15 - z_hist[1]) / z_hist[0]
            
            z_trend_mkt = np.polyfit(df_trend_t3['Mes_Num'], df_trend_t3['Preco_Mercado'], 1)
            mes_setembro = df_trend_t3['Mes_Num'].max() + 1
            preco_mercado_set = z_trend_mkt[0] * mes_setembro + z_trend_mkt[1]
            
            preco_sugerido_set = preco_mercado_set * (1 + preco_alvo_comp_set)
            
            st.info(f"A previsão estatística aponta que o Preço do Mercado em Setembro será de **R$ {preco_mercado_set:,.2f}**. Para atingirmos os 15% de vendas neste cenário, o preço da Porto deve ser:")
            
            st.success(f"**Preço Alvo Estratégico (Setembro):** R$ {preco_sugerido_set:,.2f}")
            
            diferenca_set = preco_sugerido_set - df_filtered['Preco_Cia_Interna'].mean()
            fator_ajuste_set = diferenca_set / df_filtered['Preco_Cia_Interna'].mean()
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("Esforço de Preço (Real vs Setembro)", f"R$ {diferenca_set:,.2f}", "Ganho/Desconto frente à média", delta_color="inverse" if diferenca_set < 0 else "normal")
            with col_met2:
                st.metric("Fator de Ajuste Estimado (%)", f"{fator_ajuste_set:+.2%}", "Necessidade de repasse", delta_color="inverse" if fator_ajuste_set < 0 else "normal")
            
            # Gráfico interativo da curva de preço projetada
            precos_set = np.linspace(preco_mercado_set * 0.85, preco_mercado_set * 1.15, 100)
            vendas_simuladas_set = z_hist[0] * ((precos_set / preco_mercado_set) - 1) + z_hist[1]
            df_sim_curva2 = pd.DataFrame({'Preco': precos_set, 'Vendas': vendas_simuladas_set})
            
            fig_curva2 = px.line(df_sim_curva2, x='Preco', y='Vendas', 
                                 title='Simulador de Cenários: Impacto do Preço Projetado no Fechamento',
                                 labels={'Preco': 'Preço Simulado da Porto (R$)', 'Vendas': 'Fechamento Previsto (%)'},
                                 color_discrete_sequence=['#00A1FC'])
            fig_curva2.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
            fig_curva2.add_vline(x=preco_sugerido_set, line_dash="dot", line_color="#F2A900", annotation_text="Preço Alvo (SET)")
            fig_curva2.update_layout(yaxis_tickformat='.1%', xaxis_tickprefix='R$ ', hovermode="x unified")
            st.plotly_chart(fig_curva2, width="stretch")
        else:
            st.warning("Dados insuficientes para calcular a previsão.")
            
    with subtab3:
        st.subheader("Estudo de Elasticidade-Preço da Demanda")
        st.markdown("Compreendendo matematicamente a sensibilidade do cliente às nossas mudanças de preço.")
        
        if len(df_filtered) > 2:
            x_el = df_filtered['Competitividade_Preco']
            y_el = df_filtered['Vendas']
            z_el = np.polyfit(x_el, y_el, 1)
            
            slope = z_el[0]
            
            fig_elasticidade = px.scatter(df_filtered, x='Competitividade_Preco', y='Vendas', 
                                          color_discrete_sequence=['#00A1FC'],
                                          labels={'Competitividade_Preco': 'Preço Porto vs Mercado (%)', 'Vendas': 'Vendas (%)'},
                                          title='Curva de Demanda: Sensibilidade ao Preço')
                                          
            # Adicionar linha de tendência customizada estendida até a meta
            x_alvo = (0.15 - z_el[1]) / z_el[0]
            x_min_trend = min(x_alvo - 0.02, df_filtered['Competitividade_Preco'].min() - 0.01)
            x_max_trend = df_filtered['Competitividade_Preco'].max() + 0.01
            
            x_trend = np.array([x_min_trend, x_max_trend])
            y_trend = slope * x_trend + z_el[1]
            
            fig_elasticidade.add_scatter(x=x_trend, y=y_trend, mode='lines', name='Tendência (OLS)', line=dict(color='#F2A900', width=2))
            
            # Adicionar marcador do ponto exato onde cruza 15%
            fig_elasticidade.add_scatter(x=[x_alvo], y=[0.15], mode='markers+text', 
                                         marker=dict(size=12, color='#E5004D', symbol='x'),
                                         name='Ponto de Alvo', text=[f'{x_alvo:.1%} (Competitividade Alvo)'], textposition='bottom right')
            
            fig_elasticidade.update_layout(xaxis_tickformat='.1%', yaxis_tickformat='.1%', showlegend=False)
            fig_elasticidade.update_yaxes(range=[df_filtered['Vendas'].min() * 0.95, max(df_filtered['Vendas'].max(), 0.15) * 1.05])
            fig_elasticidade.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
            st.plotly_chart(fig_elasticidade, width="stretch")
            
            st.info(f"💡 **Fator de Elasticidade Linear:** {slope:.2f}")
            st.markdown(f"Isso significa que, a cada **1%** que a Porto sobe o seu preço (ficando mais cara que a média do mercado), nós perdemos em média **{abs(slope):.2f} p.p.** na conversão de vendas. A curva de tendência acima (reta amarela) comprova que nossos clientes possuem alta sensibilidade a preço neste produto.")
        else:
            st.warning("Dados insuficientes para cálculo de elasticidade.")

with tab4:
    st.header("Simulação de Posicionamento Estratégico")
    st.markdown("Visualize o preço alvo da Porto comparado aos congêneres sob três óticas estatísticas diferentes trazidas na aba anterior.")
    
    opcao_cenario = st.radio("Selecione a ótica da simulação:", 
                             ["1. Cenário Histórico Completo", 
                              "2. Cenário Histórico (Últimos 3 Meses)",
                              "3. Cenário Histórico (Último Mês)",
                              "4. Cenário de Previsão (Projeção Setembro)", 
                              "5. Cenário de Elasticidade (Base: Último Mês)"], horizontal=True)
                              
    if len(df_filtered) > 2:
        x_hist = df_filtered['Competitividade_Preco']
        y_hist = df_filtered['Vendas']
        z_hist = np.polyfit(x_hist, y_hist, 1)
        slope = z_hist[0]
        intercept = z_hist[1]
        comp_alvo_geral = (0.15 - intercept) / slope
        
        meses_selecionados = df_filtered['Periodo'].unique()
        df_filtered['Mes_Num'] = df_filtered['Periodo'].map({'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12})
        ultimo_mes = df_filtered.loc[df_filtered['Mes_Num'].idxmax(), 'Periodo'] if 'Mes_Num' in df_filtered.columns else meses_selecionados[-1]
        df_ultimo = df_filtered[df_filtered['Periodo'] == ultimo_mes]
        
        # Coletar dados base dos congêneres dependendo do cenário
        if "Histórico Completo" in opcao_cenario:
            df_base = df_filtered.mean(numeric_only=True).to_frame().T
            mercado_base = df_base['Preco_Mercado'].iloc[0]
            preco_alvo_porto = mercado_base * (1 + comp_alvo_geral)
            titulo_cenario = "Cenário Base: Média Histórica (Todos os Meses)"
            preco_atual_porto = df_base['Preco_Cia_Interna'].iloc[0]
            nome_mes = "Média Histórica (Todos os Meses)"
            
        elif "Últimos 3 Meses" in opcao_cenario:
            meses_disp = sorted(df_filtered['Mes_Num'].unique())
            meses_alvo = meses_disp[-3:] if len(meses_disp) >= 3 else meses_disp
            df_base = df_filtered[df_filtered['Mes_Num'].isin(meses_alvo)].mean(numeric_only=True).to_frame().T
            mercado_base = df_base['Preco_Mercado'].iloc[0]
            preco_alvo_porto = mercado_base * (1 + comp_alvo_geral)
            titulo_cenario = "Cenário Base: Média Histórica (Últimos 3 Meses)"
            preco_atual_porto = df_base['Preco_Cia_Interna'].iloc[0]
            nome_mes = "Média (Últimos 3 Meses)"
            
        elif "Último Mês" in opcao_cenario and "Histórico" in opcao_cenario:
            df_base = df_ultimo.mean(numeric_only=True).to_frame().T
            mercado_base = df_base['Preco_Mercado'].iloc[0]
            preco_alvo_porto = mercado_base * (1 + comp_alvo_geral)
            titulo_cenario = f"Cenário Base: Foto do Último Mês ({ultimo_mes})"
            preco_atual_porto = df_base['Preco_Cia_Interna'].iloc[0]
            nome_mes = f"Último Mês ({ultimo_mes})"
            
        elif "Previsão" in opcao_cenario:
            periodo_ordem_t4 = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
            df_trend_t4 = df_filtered.groupby('Periodo').mean(numeric_only=True).reset_index()
            df_trend_t4['Mes_Num'] = df_trend_t4['Periodo'].map(periodo_ordem_t4)
            mes_set = df_trend_t4['Mes_Num'].max() + 1
            
            cols_to_predict = ['Preco_Mercado', 'Preco_Cia_Interna', 'Preco_Concorrente_1', 'Preco_Concorrente_2', 'Preco_Concorrente_3', 'Preco_Concorrente_4']
            df_base = pd.DataFrame(index=[0])
            for c in cols_to_predict:
                zt = np.polyfit(df_trend_t4['Mes_Num'], df_trend_t4[c], 1)
                df_base[c] = zt[0] * mes_set + zt[1]
                
            mercado_base = df_base['Preco_Mercado'].iloc[0]
            preco_alvo_porto = mercado_base * (1 + comp_alvo_geral)
            titulo_cenario = "Cenário Base: Previsão para Setembro"
            preco_atual_porto = df_base['Preco_Cia_Interna'].iloc[0] 
            nome_mes = "Projeção Estatística SET"
            
        else:
            df_base = df_ultimo.mean(numeric_only=True).to_frame().T
            mercado_base = df_base['Preco_Mercado'].iloc[0]
            vendas_atual = df_base['Vendas'].iloc[0]
            preco_atual_porto = df_base['Preco_Cia_Interna'].iloc[0]
            
            delta_vendas = 0.15 - vendas_atual
            delta_comp = delta_vendas / slope
            preco_alvo_porto = preco_atual_porto + (delta_comp * mercado_base)
            
            titulo_cenario = f"Cenário Base: Elasticidade (Partindo da foto de {ultimo_mes})"
            nome_mes = f"Último Mês ({ultimo_mes}) + Elasticidade"
            
        # Preparar plot_data
        dados_plot = []
        fator_ajuste_sim = (preco_alvo_porto - preco_atual_porto) / preco_atual_porto
        
        dados_plot.append({'Seguradora': 'Porto', 'Preco': preco_atual_porto, 'Tipo': 'Atual (Porto)', 'Rotulo': f"Atual: R$ {preco_atual_porto:,.0f}"})
        dados_plot.append({'Seguradora': 'Porto', 'Preco': preco_alvo_porto, 'Tipo': 'Simulado (Meta 15%)', 'Rotulo': f"Alvo: R$ {preco_alvo_porto:,.0f} ({fator_ajuste_sim:+.1%})"})
        dados_plot.append({'Seguradora': 'Média Mercado', 'Preco': mercado_base, 'Tipo': 'Mercado Médio', 'Rotulo': f"Média: R$ {mercado_base:,.0f}"})
        
        for i in range(1, 5):
            preco_conc = df_base[f'Preco_Concorrente_{i}'].iloc[0]
            dados_plot.append({'Seguradora': f'Concorrente {i}', 'Preco': preco_conc, 'Tipo': 'Congêneres', 'Rotulo': f"R$ {preco_conc:,.0f}"})
            
        plot_data = pd.DataFrame(dados_plot)
        # Padronizar a ordem do eixo X: Congêneres (ordenados por preço), Média Mercado, Porto
        plot_data['Ordem_X'] = plot_data['Seguradora'].map({'Porto': 2, 'Média Mercado': 1}).fillna(0)
        plot_data = plot_data.sort_values(by=['Ordem_X', 'Preco'], ascending=[True, False])
        
        st.subheader(titulo_cenario)
        fig_sim = px.scatter(plot_data, x='Seguradora', y='Preco', color='Tipo', text='Rotulo',
                             title=f"Posicionamento de Prêmios ({nome_mes})",
                             labels={'Preco': 'Prêmio Praticado (R$)'},
                             color_discrete_map={'Atual (Porto)': '#00A1FC', 'Congêneres': '#a0a3a5', 'Simulado (Meta 15%)': '#00B050', 'Mercado Médio': '#8a8d90'})
                             
        fig_sim.update_traces(marker=dict(size=22), textposition='middle right')
        fig_sim.update_layout(yaxis_tickprefix='R$ ', xaxis_title=None)
        fig_sim.update_xaxes(range=[-0.5, 5.8])
        
        st.plotly_chart(fig_sim, width="stretch")
        
        diferenca_sim = preco_alvo_porto - preco_atual_porto
        texto_diff = "redução" if diferenca_sim < 0 else "aumento"
        st.success(f"**Conclusão Estratégica:** Sob a ótica deste cenário, a Porto precisaria realizar uma **{texto_diff} de R\$ {abs(diferenca_sim):.2f}** no preço frente à sua média local, reposicionando-se de **R\$ {preco_atual_porto:,.2f}** para **R\$ {preco_alvo_porto:,.2f}** para bater a meta de 15%.")

    else:
        st.warning("Selecione um histórico maior nos filtros para gerar as simulações.")

with tab5:
    st.header("Racional Matemático e Metodologia")
    st.markdown("""
    Neste painel, utilizamos técnicas de **Estatística** e **Inteligência Artificial (Machine Learning)** para basear a tomada de decisão puramente em dados (Data-Driven), e não apenas em intuição. Abaixo detalhamos a matemática por trás das recomendações exibidas:
    
    ### 1. Simulação da Meta de 15% (Regressão Linear)
    Para descobrir qual preço exato a Porto deve aplicar para cruzar a meta de 15% de vendas, utilizamos uma técnica chamada **Regressão Linear Simples (OLS)**. 
    
    * **Como funciona:** O algoritmo mapeou todo o nosso histórico, cruzando a nossa *Competitividade de Preço* (eixo X) com a nossa *Conversão de Vendas* (eixo Y). Ele então traçou a "linha de melhor ajuste" (equação matemática: `y = ax + b`) que melhor descreve a elasticidade do nosso preço.
    * **A Tomada de Decisão:** Sabendo a equação da reta, nós programamos o sistema para definir que a nossa conversão deve ser `y = 15% (0.15)` e isolamos a variável `x`. O resultado matemático disso é a exata competitividade (o desconto ou ágio) que precisamos ter frente ao mercado atual para performar naquele patamar. Ao aplicar esse percentual gerado no Preço Médio do Mercado de hoje, chegamos ao preço alvo em Reais (R$) sugerido na aba de simulação.
    
    ---
    
    ### 2. Mapa de Competição e Nichos (Algoritmo K-Means)
    Para identificar quem são os nossos reais congêneres e em qual território a Porto está competindo atualmente, rodamos um modelo de aprendizado de máquina não supervisionado chamado **K-Means**.
    
    * **Como funciona:** O algoritmo recebe os dados de Preço e de Volume de Cotações de todas as seguradoras. Antes do cálculo, nós usamos o `StandardScaler` para normalizar essas métricas (já que Preço está na casa dos milhares e Volume na casa dos milhões, não queremos que o volume ofusque o preço na conta). Depois disso, o K-Means tenta agrupar as seguradoras minimizando a distância espacial (euclidiana) entre elas no plano cartesiano.
    * **A Tomada de Decisão:** Em vez de um ser humano classificar "quem é quem" por achismo, o algoritmo dividiu automaticamente o mercado em 3 grupos puramente pelo comportamento de tração e precificação. Isso permite que a diretoria enxergue, sem qualquer viés, se o nosso preço atual nos coloca lado a lado com os Líderes de Volume, ou se estamos perdendo competitividade e caindo para um nicho de baixa atratividade.
    
    ---
    
    ### 3. Previsão de Setembro (Projeção de Séries Temporais)
    Para não basearmos as metas da diretoria apenas olhando para o retrovisor (Cenário Histórico), aplicamos algoritmos preditivos para estimar qual será o cenário real do mercado no próximo mês.
    
    * **Como funciona:** Utilizamos uma Regressão de Séries Temporais. O sistema plota o tempo (Meses passados) no eixo X e as variáveis de negócio (Preço e Volume) no eixo Y. Ao analisar o comportamento histórico dessa reta estatística, conseguimos extrapolar e prever o valor do mês seguinte (Setembro).
    * **A Tomada de Decisão:** Isso muda radicalmente o jogo! O sistema calcula o preço sugerido da Porto cruzando a meta de 15% **em cima do preço futuro projetado do mercado**. Isso previne a Cia de dar descontos exagerados em um mês em que o mercado tenderá a encarecer naturalmente, ou alerta a Cia de que um esforço maior será necessário se a tendência do mercado for de baratear.
    
    ---
    
    ### 4. Coeficiente de Elasticidade-Preço da Demanda (Epd)
    Uma das métricas econômicas mais valiosas do painel.
    
    * **Como funciona:** O painel extrai estatisticamente o **Coeficiente Angular (Slope)** da regressão que correlaciona nossa competitividade com as nossas conversões. Esse coeficiente matemático representa exatamente a sensibilidade do nosso consumidor a preço.
    * **A Tomada de Decisão:** O resultado mostra precisamente quantos pontos percentuais (p.p.) perdemos em vendas para cada 1% que aumentamos nosso preço. Com esse dado validado matematicamente, qualquer reajuste de prêmio passa a ter um impacto previsível na tração, permitindo que a companhia planeje descontos sabendo antecipadamente se o ganho de volume compensará a perda de margem de lucro.
    """)

