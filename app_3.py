import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuração da página
st.set_page_config(page_title="Case - Novos Negócios (Opção 3: Sidebar Menu)", layout="wide", page_icon="🚗")

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
# SIDEBAR COM NAVEGAÇÃO E FILTROS
# ==========================================
st.sidebar.image("Porto_Holding_RGB_Horizontal-Cyan.webp")
st.sidebar.title("Navegação")

menu_selecionado = st.sidebar.radio("Selecione a Visão:", ["🏠 Tela Inicial (Capa)", "📊 Dashboard Interativo"])

st.sidebar.markdown("---")

if menu_selecionado == "🏠 Tela Inicial (Capa)":
    # RENDERIZAR CAPA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #004691 0%, #00A1FC 100%); padding: 35px; border-radius: 15px; color: white; margin-bottom: 25px;">
        <h1 style="color: white; margin-bottom: 10px;">🚗 Análise de Posicionamento - Novos Negócios</h1>
        <h3 style="color: #e0f2fe; font-weight: 400; margin-top: 0;">Estratégia de Precificação, Elasticidade de Demanda e Meta de 15% de Conversão</h3>
        <p style="font-size: 1.1em; opacity: 0.95; max-width: 900px; margin-top: 15px;">
            Painel Executivo desenvolvido para avaliar a competitividade da Porto Seguro frente às seguradoras concorrentes no produto auto, mapeando alvos tarifários para atingimento da meta corporativa de 15% de vendas.
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
    st.subheader("💡 Como navegar?")
    st.markdown("Use o **menu lateral à esquerda** trocando de `🏠 Tela Inicial (Capa)` para `📊 Dashboard Interativo` para explorar os dados detalhados e simulações.")

else:
    # RENDERIZAR DASHBOARD COMPLETO
    st.sidebar.title("Filtros")
    perfil_selecionado = st.sidebar.selectbox("Perfil de Cliente", ["Todos", "Perfil 1", "Perfil 2"])
    periodo_selecionado = st.sidebar.multiselect("Período", df['Periodo'].unique(), default=df['Periodo'].unique())

    df_filtered = df[df['Periodo'].isin(periodo_selecionado)]
    if perfil_selecionado != "Todos":
        perfil_val = int(perfil_selecionado.replace("Perfil ", ""))
        df_filtered = df_filtered[df_filtered['Perfil_Cliente'] == perfil_val]

    st.title("🚗 Análise de Posicionamento - Novos Negócios")
    st.markdown("---")

    if df_filtered.empty:
        st.warning("Selecione pelo menos um período nos filtros.")
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Posicionamento de Mercado", "🧩 Análise de Cluster", "📈 Meta de 15% de Vendas", "🔮 Cenário Simulado", "🧠 Racional Matemático"])

    with tab1:
        st.header("Análise de Posicionamento de Mercado")
        
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
        fig_scatter.update_yaxes(range=[df_filtered['Vendas'].min() * 0.95, max(df_filtered['Vendas'].max(), 0.15) * 1.05])
        fig_scatter.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
        st.plotly_chart(fig_scatter, width="stretch")
        st.info("💡 **Insight de Posicionamento:** O gráfico acima ilustra a sensibilidade de preço.")

    with tab2:
        st.header("Análise de Cluster (Agrupamento das Seguradoras)")
        st.markdown("Nesta seção utilizamos K-Means para agrupar as **Seguradoras**.")
        
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
            st.success(f"**Atenção:** A **Porto** foi classificada matematicamente no grupo: **{porto_cluster}**.")
            
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

    with tab3:
        st.header("Plano de Ação: Atingir 15% de Vendas no Mês")
        subtab1, subtab2, subtab3 = st.tabs(["📊 Cenário Histórico", "🔮 Previsão para Setembro", "📐 Elasticidade de Preço"])
        
        with subtab1:
            st.subheader("Simulador Baseado no Comportamento Histórico")
            filtro_hist = st.radio("Selecione o recorte de tempo:", ["Histórico Completo", "Últimos 3 Meses", "Apenas Último Mês (Ex: Agosto)"], horizontal=True)
            
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
                x_reg = df_sim_hist['Competitividade_Preco'] if len(df_sim_hist) >= 2 else df_filtered['Competitividade_Preco']
                y_reg = df_sim_hist['Vendas'] if len(df_sim_hist) >= 2 else df_filtered['Vendas']
                
                try:
                    z = np.polyfit(x_reg, y_reg, 1)
                    meta_vendas = 0.15
                    preco_alvo_competitividade = (meta_vendas - z[1]) / z[0]
                    st.info(f"De acordo com a tendência estatística, para atingir **15% de Vendas**, a relação deve ser de **{preco_alvo_competitividade:.1%}**.")
                    
                    col_sim1, col_sim2, col_sim3 = st.columns([2, 1.5, 1.2])
                    with col_sim1:
                        mercado_simulado = st.number_input("Preço Médio do Mercado (R$):", value=float(df_sim_hist['Preco_Mercado'].mean()), step=100.0)
                        preco_sugerido = mercado_simulado * (1 + preco_alvo_competitividade)
                        st.success(f"**Preço Sugerido para a Porto:** R$ {preco_sugerido:,.2f}")
                        
                    diferenca = preco_sugerido - df_sim_hist['Preco_Cia_Interna'].mean()
                    fator_ajuste = diferenca / df_sim_hist['Preco_Cia_Interna'].mean()
                    texto_diff = "Aumento" if diferenca > 0 else "Redução"
                    
                    with col_sim2:
                        st.metric("Ajuste Médio Necessário", f"R$ {diferenca:,.2f}", delta_color="inverse" if diferenca < 0 else "normal")
                    with col_sim3:
                        st.metric("Fator de Ajuste (%)", f"{fator_ajuste:+.2%}", delta_color="inverse" if fator_ajuste < 0 else "normal")
                        
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
                    st.warning("Não foi possível calcular.")
            else:
                st.warning("Sem dados suficientes.")
                
        with subtab2:
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
                
                st.info(f"Previsão de Preço do Mercado em Setembro: **R$ {preco_mercado_set:,.2f}**.")
                st.success(f"**Preço Alvo Estratégico (Setembro):** R$ {preco_sugerido_set:,.2f}")
                
                diferenca_set = preco_sugerido_set - df_filtered['Preco_Cia_Interna'].mean()
                fator_ajuste_set = diferenca_set / df_filtered['Preco_Cia_Interna'].mean()
                
                col_met1, col_met2 = st.columns(2)
                with col_met1:
                    st.metric("Esforço de Preço", f"R$ {diferenca_set:,.2f}", delta_color="inverse" if diferenca_set < 0 else "normal")
                with col_met2:
                    st.metric("Fator de Ajuste Estimado (%)", f"{fator_ajuste_set:+.2%}", delta_color="inverse" if fator_ajuste_set < 0 else "normal")
                
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
                st.warning("Dados insuficientes.")
                
        with subtab3:
            st.subheader("Estudo de Elasticidade-Preço da Demanda")
            if len(df_filtered) > 2:
                x_el = df_filtered['Competitividade_Preco']
                y_el = df_filtered['Vendas']
                z_el = np.polyfit(x_el, y_el, 1)
                slope = z_el[0]
                
                fig_elasticidade = px.scatter(df_filtered, x='Competitividade_Preco', y='Vendas', 
                                              color_discrete_sequence=['#00A1FC'],
                                              labels={'Competitividade_Preco': 'Preço Porto vs Mercado (%)', 'Vendas': 'Vendas (%)'},
                                              title='Curva de Demanda: Sensibilidade ao Preço')
                                              
                x_alvo = (0.15 - z_el[1]) / z_el[0]
                x_min_trend = min(x_alvo - 0.02, df_filtered['Competitividade_Preco'].min() - 0.01)
                x_max_trend = df_filtered['Competitividade_Preco'].max() + 0.01
                
                x_trend = np.array([x_min_trend, x_max_trend])
                y_trend = slope * x_trend + z_el[1]
                fig_elasticidade.add_scatter(x=x_trend, y=y_trend, mode='lines', name='Tendência (OLS)', line=dict(color='#F2A900', width=2))
                fig_elasticidade.add_scatter(x=[x_alvo], y=[0.15], mode='markers+text', 
                                             marker=dict(size=12, color='#E5004D', symbol='x'),
                                             name='Ponto de Alvo', text=[f'{x_alvo:.1%} (Competitividade Alvo)'], textposition='bottom right')
                
                fig_elasticidade.update_layout(xaxis_tickformat='.1%', yaxis_tickformat='.1%', showlegend=False)
                fig_elasticidade.update_yaxes(range=[df_filtered['Vendas'].min() * 0.95, max(df_filtered['Vendas'].max(), 0.15) * 1.05])
                fig_elasticidade.add_hline(y=0.15, line_dash="dash", line_color="#00B050", annotation_text="Meta de Vendas (15%)")
                st.plotly_chart(fig_elasticidade, width="stretch")
                st.info(f"💡 **Fator de Elasticidade Linear:** {slope:.2f}")
            else:
                st.warning("Dados insuficientes.")

    with tab4:
        st.header("Simulação de Posicionamento Estratégico")
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
                
            dados_plot = []
            fator_ajuste_sim = (preco_alvo_porto - preco_atual_porto) / preco_atual_porto
            
            dados_plot.append({'Seguradora': 'Porto', 'Preco': preco_atual_porto, 'Tipo': 'Atual (Porto)', 'Rotulo': f"Atual: R$ {preco_atual_porto:,.0f}"})
            dados_plot.append({'Seguradora': 'Porto', 'Preco': preco_alvo_porto, 'Tipo': 'Simulado (Meta 15%)', 'Rotulo': f"Alvo: R$ {preco_alvo_porto:,.0f} ({fator_ajuste_sim:+.1%})"})
            dados_plot.append({'Seguradora': 'Média Mercado', 'Preco': mercado_base, 'Tipo': 'Mercado Médio', 'Rotulo': f"Média: R$ {mercado_base:,.0f}"})
            
            for i in range(1, 5):
                preco_conc = df_base[f'Preco_Concorrente_{i}'].iloc[0]
                dados_plot.append({'Seguradora': f'Concorrente {i}', 'Preco': preco_conc, 'Tipo': 'Congêneres', 'Rotulo': f"R$ {preco_conc:,.0f}"})
                
            plot_data = pd.DataFrame(dados_plot)
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
            st.success(f"**Conclusão Estratégica:** Reposicionamento para **R$ {preco_alvo_porto:,.2f}**.")
        else:
            st.warning("Selecione um histórico maior.")

    with tab5:
        st.header("Racional Matemático e Metodologia")
        st.markdown("""
        ### 1. Simulação da Meta de 15% (Regressão Linear)
        Mapeamento OLS.
        ### 2. Mapa de Competição (Algoritmo K-Means)
        Clusterização K-Means.
        ### 3. Previsão de Setembro
        Polyfit linear temporal.
        ### 4. Coeficiente de Elasticidade-Preço
        Slope OLS.
        """)
