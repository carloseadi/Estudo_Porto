import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuração da página
st.set_page_config(page_title="Case - Novos Negócios (Opção 4: Multi-Page Navigation Bar)", layout="wide", page_icon="🚗")

# Função para carregar os dados
@st.cache_data
def load_data():
    file_path = "Case Contratação - Dados.xlsx"
    df = pd.read_excel(file_path)
    
    new_cols = [
        'Periodo', 'Perfil_Cliente', 'Vendas', 
        'Preco_Cia_Interna', 'Preco_Concorrente_1', 'Preco_Concorrente_2', 'Preco_Concorrente_3', 'Preco_Concorrente_4', 'Preco_Mercado',
        'Cotacoes_Cia_Interna', 'Cotacoes_Concorrente_1', 'Cotacoes_Concorrente_2', 'Cotacoes_Concorrente_3', 'Cotacoes_Concorrente_4', 'Cotacoes_Mercado'
    ]
    df.columns = new_cols
    
    df['Competitividade_Preco'] = df['Preco_Cia_Interna'] / df['Preco_Mercado'] - 1
    df['Share_Cotacoes'] = df['Cotacoes_Cia_Interna'] / df['Cotacoes_Mercado']
    
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
# HEADER & BARRA DE NAVEGAÇÃO DE PÁGINAS (TOP BAR)
# ==========================================
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("Porto_Holding_RGB_Horizontal-Cyan.webp", width=180)
with col_header2:
    pagina_atual = st.radio(
        "Navegação por Seção do App:",
        ["🏠 1. Capa & Storytelling Executivo", "📊 2. Posicionamento de Mercado", "🧩 3. Análise de Cluster K-Means", "📈 4. Simuladores Meta 15%", "🧠 5. Metodologia Científica"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("---")

# ==========================================
# SIDEBAR (FILTROS)
# ==========================================
st.sidebar.title("Filtros Globais")
perfil_selecionado = st.sidebar.selectbox("Perfil de Cliente", ["Todos", "Perfil 1", "Perfil 2"])
periodo_selecionado = st.sidebar.multiselect("Período", df['Periodo'].unique(), default=df['Periodo'].unique())

df_filtered = df[df['Periodo'].isin(periodo_selecionado)]
if perfil_selecionado != "Todos":
    perfil_val = int(perfil_selecionado.replace("Perfil ", ""))
    df_filtered = df_filtered[df_filtered['Perfil_Cliente'] == perfil_val]

if df_filtered.empty:
    st.warning("Selecione pelo menos um período nos filtros.")
    st.stop()

# ==========================================
# CONTEÚDO DAS PÁGINAS
# ==========================================

# --- PÁGINA 1: CAPA & STORYTELLING ---
if "1. Capa" in pagina_atual:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #004691 0%, #00A1FC 100%); padding: 35px; border-radius: 15px; color: white; margin-bottom: 25px;">
        <h1 style="color: white; margin-bottom: 10px;">🚗 Análise de Posicionamento - Novos Negócios</h1>
        <h3 style="color: #e0f2fe; font-weight: 400; margin-top: 0;">Estratégia de Precificação, Elasticidade de Demanda e Meta de 15% de Conversão</h3>
        <p style="font-size: 1.1em; opacity: 0.95; max-width: 900px; margin-top: 15px;">
            Este painel oferece uma navegação modular em formato de páginas independentes para orientar os decisores da Porto Seguro no alinhamento de prêmios e alcance da meta de vendas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px; text-align: center;">
            <h4 style="color: #166534; margin: 0; font-weight: 600;">Share de Cotações</h4>
            <div style="display: flex; justify-content: space-around; margin: 15px 0 10px 0; align-items: center;">
                <div style="border-right: 1px solid #cbd5e1; padding-right: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 1</span>
                    <span style="font-size: 1.8em; color: #15803d; font-weight: 700;">72,4%</span>
                    <span style="font-size: 0.75em; color: #64748b; display: block;">856k cotações</span>
                </div>
                <div style="padding-left: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 2</span>
                    <span style="font-size: 1.8em; color: #15803d; font-weight: 700;">67,6%</span>
                    <span style="font-size: 0.75em; color: #64748b; display: block;">545k cotações</span>
                </div>
            </div>
            <p style="color: #166534; margin: 5px 0 0 0; font-size: 0.82em; font-weight: 500;">Dominância de atração em ambos os perfis</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 20px; text-align: center;">
            <h4 style="color: #991b1b; margin: 0; font-weight: 600;">Conversão Atual vs Meta (15%)</h4>
            <div style="display: flex; justify-content: space-around; margin: 15px 0 10px 0; align-items: center;">
                <div style="border-right: 1px solid #cbd5e1; padding-right: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 1</span>
                    <span style="font-size: 1.8em; color: #dc2626; font-weight: 700;">12,54%</span>
                    <span style="font-size: 0.75em; color: #991b1b; display: block;">Gap -2,46 p.p.</span>
                </div>
                <div style="padding-left: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 2</span>
                    <span style="font-size: 1.8em; color: #d97706; font-weight: 700;">13,40%</span>
                    <span style="font-size: 0.75em; color: #b45309; display: block;">Gap -1,60 p.p.</span>
                </div>
            </div>
            <p style="color: #991b1b; margin: 5px 0 0 0; font-size: 0.82em; font-weight: 500;">Meta Corporativa de Fechamento: 15,00%</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 20px; text-align: center;">
            <h4 style="color: #1e40af; margin: 0; font-weight: 600;">Ajuste Tarifário (Setembro)</h4>
            <div style="display: flex; justify-content: space-around; margin: 15px 0 10px 0; align-items: center;">
                <div style="border-right: 1px solid #cbd5e1; padding-right: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 1</span>
                    <span style="font-size: 1.8em; color: #2563eb; font-weight: 700;">-2,50%</span>
                    <span style="font-size: 0.75em; color: #1e40af; display: block;">Alvo R$ 2.773</span>
                </div>
                <div style="padding-left: 12px; width: 50%;">
                    <span style="font-size: 0.8em; color: #475569; font-weight: 600; display: block;">PRODUTO 2</span>
                    <span style="font-size: 1.8em; color: #2563eb; font-weight: 700;">-2,84%</span>
                    <span style="font-size: 0.75em; color: #1e40af; display: block;">Alvo R$ 4.427</span>
                </div>
            </div>
            <p style="color: #1e40af; margin: 5px 0 0 0; font-size: 0.82em; font-weight: 500;">Ajuste preditivo necessário para meta</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Navegação Modular:** Selecione uma das seções na barra de opções localizada no topo da página para visualizar os detalhes.")

# --- PÁGINA 2: POSICIONAMENTO DE MERCADO ---
elif "2. Posicionamento" in pagina_atual:
    st.header("🎯 Análise de Posicionamento de Mercado")
    
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
    col_chart1, col_chart_mid, col_chart2 = st.columns(3)
    
    with col_chart1:
        st.subheader("Evolução do Preço Médio")
        opcao_visao = st.radio("Visão de Comparativo:", ["Porto vs Mercado (Apenas)", "Visão Geral (Todos os Players)"], horizontal=True)
        cols_price = ['Preco_Cia_Interna', 'Preco_Mercado', 'Preco_Concorrente_1', 'Preco_Concorrente_2', 'Preco_Concorrente_3', 'Preco_Concorrente_4']
        cols_plot = ['Preco_Cia_Interna', 'Preco_Mercado'] if opcao_visao == "Porto vs Mercado (Apenas)" else cols_price
        
        periodo_ordem = {'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12}
        df_price = df_filtered.groupby('Periodo')[cols_price].mean().reset_index()
        df_price['Mes_Num'] = df_price['Periodo'].map(periodo_ordem)
        df_price = df_price.sort_values('Mes_Num')
        
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
            
        color_map = {
            'Preco_Cia_Interna': '#00A1FC', 'Preco_Mercado': '#8a8d90',
            'Preco_Concorrente_1': '#F2A900', 'Preco_Concorrente_2': '#E5004D',
            'Preco_Concorrente_3': '#00B050', 'Preco_Concorrente_4': '#8b4513'
        }
        
        fig_price = px.line(df_price, x='Periodo', y=cols_plot,
                            labels={'value': 'Preço (R$)', 'variable': 'Player', 'Periodo': 'Mês'},
                            title='Evolução do Preço Médio (com Previsão)', markers=True, 
                            color_discrete_map=color_map)
                            
        if ultimo_mes_hist and len(df_price) >= 3:
            fig_price.add_vline(x=len(df_price) - 1.5, line_dash="dash", line_color="#c2c4c6")
            
        newnames = {'Preco_Cia_Interna': 'Porto', 'Preco_Mercado': 'Mercado Médio', 
                    'Preco_Concorrente_1': 'Congênere 1', 'Preco_Concorrente_2': 'Congênere 2', 
                    'Preco_Concorrente_3': 'Congênere 3', 'Preco_Concorrente_4': 'Congênere 4'}
        fig_price.for_each_trace(lambda t: t.update(name = newnames.get(t.name, t.name), legendgroup = newnames.get(t.name, t.name)))
        
        fig_price.update_traces(connectgaps=False)
        fig_price.update_layout(yaxis_tickprefix='R$ ', legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_price, width="stretch")
        
    with col_chart_mid:
        st.subheader("Conversão de Vendas (%)")
        st.markdown("<div style='height: 68px;'></div>", unsafe_allow_html=True)
        
        df_vendas = df_filtered.groupby('Periodo')['Vendas'].mean().reset_index()
        df_vendas['Mes_Num'] = df_vendas['Periodo'].map(periodo_ordem)
        df_vendas = df_vendas.sort_values('Mes_Num')
        
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
        fig_vendas.update_layout(yaxis_tickformat='.1%', legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_vendas, width="stretch")
        
    with col_chart2:
        st.subheader("Volume de Cotações (Porto vs Congêneres)")
        st.markdown("<div style='height: 68px;'></div>", unsafe_allow_html=True)
        
        cols_cotacoes = ['Cotacoes_Cia_Interna', 'Cotacoes_Concorrente_1', 'Cotacoes_Concorrente_2', 'Cotacoes_Concorrente_3', 'Cotacoes_Concorrente_4']
        df_cot = df_filtered.groupby('Periodo')[cols_cotacoes].sum().reset_index()
        df_cot['Mes_Num'] = df_cot['Periodo'].map(periodo_ordem)
        df_cot = df_cot.sort_values('Mes_Num')
        
        if len(df_cot) >= 3:
            ultimo_mes_num = df_cot['Mes_Num'].max()
            mes_futuro = ultimo_mes_num + 1
            ordem_periodo_rev = {v: k for k, v in periodo_ordem.items()}
            mes_futuro_str = ordem_periodo_rev.get(mes_futuro, f"Mês {mes_futuro}")
            
            nova_linha_cot = {'Periodo': mes_futuro_str, 'Mes_Num': mes_futuro}
            for col in cols_cotacoes:
                z_trend = np.polyfit(df_cot['Mes_Num'], df_cot[col], 1)
                nova_linha_cot[col] = max(0, z_trend[0] * mes_futuro + z_trend[1])
                
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
        fig_cot.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_cot, width="stretch")
        
    st.markdown("---")
    st.subheader("Relação: Preço vs Volume de Vendas")
    fig_scatter = px.scatter(df_filtered, x='Competitividade_Preco', y='Vendas', 
                             color='Perfil_Cliente', text='Periodo', hover_data=['Preco_Cia_Interna', 'Preco_Mercado'],
                             labels={'Competitividade_Preco': 'Preço Porto vs Mercado (%)', 'Vendas': 'Vendas (%)'},
                             title='Impacto do Posicionamento de Preço na Conversão de Vendas',
                             color_discrete_sequence=['#00A1FC', '#004691'])
                             
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(xaxis_tickformat='.1%', yaxis_tickformat='.1%')
    fig_scatter.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
    st.plotly_chart(fig_scatter, width="stretch")

# --- PÁGINA 3: CLUSTER K-MEANS ---
elif "3. Análise de Cluster" in pagina_atual:
    st.header("🧩 Análise de Cluster (Agrupamento das Seguradoras)")
    companies = ['Cia_Interna', 'Concorrente_1', 'Concorrente_2', 'Concorrente_3', 'Concorrente_4']
    company_data = []
    for comp in companies:
        preco_col = f'Preco_{comp}'
        cot_col = f'Cotacoes_{comp}'
        mean_preco = df_filtered[preco_col].mean()
        sum_cot = df_filtered[cot_col].sum()
        nome = "Porto" if comp == 'Cia_Interna' else comp.replace('_', ' ').replace('Concorrente', 'Congênere')
        company_data.append({'Seguradora': nome, 'Preco_Medio': mean_preco, 'Volume_Cotacoes': sum_cot})
        
    df_comp = pd.DataFrame(company_data)
    
    if df_comp['Preco_Medio'].notna().all() and not df_comp.empty:
        features = df_comp[['Preco_Medio', 'Volume_Cotacoes']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters_raw = kmeans.fit_predict(features_scaled)
        df_comp['Cluster_ID'] = clusters_raw
        
        overall_preco = df_comp['Preco_Medio'].mean()
        overall_vol = df_comp['Volume_Cotacoes'].mean()
        cluster_means = df_comp.groupby('Cluster_ID')[['Preco_Medio', 'Volume_Cotacoes']].mean()
        
        cluster_labels = {}
        for cluster_id, row in cluster_means.iterrows():
            preco_diff = row['Preco_Medio'] / overall_preco - 1
            vol_diff = row['Volume_Cotacoes'] / overall_vol - 1
            p_label = "Alto" if preco_diff > 0.03 else ("Baixo" if preco_diff < -0.03 else "Médio")
            v_label = "Alto" if vol_diff > 0.15 else ("Baixo" if vol_diff < -0.15 else "Médio")
            cluster_labels[cluster_id] = f"Preço {p_label} / Volume {v_label}"
            
        df_comp['Cluster'] = df_comp['Cluster_ID'].map(cluster_labels)
        df_comp = df_comp.sort_values(by=['Volume_Cotacoes', 'Preco_Medio'], ascending=False)
        
        porto_cluster = df_comp[df_comp['Seguradora'] == 'Porto']['Cluster'].values[0]
        st.success(f"**Atenção:** A **Porto** foi classificada no grupo: **{porto_cluster}**.")
        
        fig_cluster = px.scatter(df_comp, x='Preco_Medio', y='Volume_Cotacoes', 
                                 color='Cluster', text='Seguradora',
                                 labels={'Preco_Medio': 'Preço Médio Praticado (R$)', 'Volume_Cotacoes': 'Volume Total de Cotações'},
                                 title='Mapa de Competição: Em qual grupo cada Seguradora se encaixa?',
                                 color_discrete_sequence=['#00A1FC', '#F2A900', '#E5004D'])
        fig_cluster.update_traces(marker=dict(size=12), textposition='top center')
        fig_cluster.update_layout(xaxis_tickprefix='R$ ')
        st.plotly_chart(fig_cluster, width="stretch")
    else:
        st.warning("Selecione períodos válidos nos filtros.")

# --- PÁGINA 4: SIMULADORES META 15% ---
elif "4. Simuladores" in pagina_atual:
    st.header("📈 Simuladores para Atingir a Meta de 15% de Vendas")
    subtab1, subtab2 = st.tabs(["🔮 Previsão para Setembro", "📐 Elasticidade de Preço"])
    
    with subtab1:
        st.subheader("Meta Aplicada na Previsão de Setembro")
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
            
            st.info(f"Preço projetado do Mercado em Setembro: **R$ {preco_mercado_set:,.2f}**.")
            st.success(f"**Preço Alvo Sugerido para a Porto:** R$ {preco_sugerido_set:,.2f}")
            
            precos_set = np.linspace(preco_mercado_set * 0.85, preco_mercado_set * 1.15, 100)
            vendas_simuladas_set = z_hist[0] * ((precos_set / preco_mercado_set) - 1) + z_hist[1]
            df_sim_curva2 = pd.DataFrame({'Preco': precos_set, 'Vendas': vendas_simuladas_set})
            
            fig_curva2 = px.line(df_sim_curva2, x='Preco', y='Vendas', 
                                 title='Simulador de Cenários: Preço Simulado vs Conversão Prevista',
                                 labels={'Preco': 'Preço Simulado (R$)', 'Vendas': 'Fechamento Previsto (%)'},
                                 color_discrete_sequence=['#00A1FC'])
            fig_curva2.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
            fig_curva2.add_vline(x=preco_sugerido_set, line_dash="dot", line_color="#F2A900", annotation_text="Preço Alvo (SET)")
            fig_curva2.update_layout(yaxis_tickformat='.1%', xaxis_tickprefix='R$ ', hovermode="x unified")
            st.plotly_chart(fig_curva2, width="stretch")
            
    with subtab2:
        st.subheader("Estudo de Elasticidade-Preço")
        if len(df_filtered) > 2:
            x_el = df_filtered['Competitividade_Preco']
            y_el = df_filtered['Vendas']
            z_el = np.polyfit(x_el, y_el, 1)
            slope = z_el[0]
            st.info(f"💡 **Sensibilidade (Slope):** {slope:.2f}. A cada 1% de aumento relativo no preço, a Porto perde {abs(slope):.2f} p.p. em vendas.")

# --- PÁGINA 5: METODOLOGIA ---
else:
    st.header("🧠 Metodologia e Racional Científico")
    st.markdown("""
    ### 1. Regressão Linear Simples (OLS)
    Cálculo exato da competitividade relativa necessária para atingir `y = 15%`.
    
    ### 2. Algoritmo K-Means
    Clusterização com normalização Z-score via `StandardScaler`.
    
    ### 3. Previsão Temporal de Séries Temporais
    Extrapolação estatística de tendências de mercado para o próximo mês (Setembro).
    """)
