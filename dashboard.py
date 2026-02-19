import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os # <--- ADICIONADO AQUI

st.set_page_config(page_title="Analytics de Produtos", layout="wide")

st.title("📊 Dashboard de Inventário Profissional")

# CORREÇÃO: Lê do ambiente, ou usa localhost como fallback
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if 'token' not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.header("🔑 Autenticação")
    if not st.session_state.token:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            try:
                res = requests.post(f"{API_URL}/api/v1/auth/token", data={"username": username, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
            except:
                st.error("API Offline!")
    else:
        st.success("Conectado!")
        if st.button("Sair"):
            st.session_state.token = None
            st.rerun()

def get_data(endpoint, protected=True):
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if protected else {}
    return requests.get(f"{API_URL}/api/v1/products/{endpoint}", headers=headers)

if st.session_state.token:
    res_stats = get_data("stats")
    res_list = get_data("", protected=False)

    if res_stats.status_code == 200:
        stats = res_stats.json()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", stats['total_count'])
        c2.metric("Média", f"R$ {stats['average_price']}")
        c3.metric("Mínimo", f"R$ {stats['min_price']}")
        c4.metric("Máximo", f"R$ {stats['max_price']}")

        products_data = res_list.json()['products']
        df = pd.DataFrame(products_data)
        
        if not df.empty:
            # CORREÇÃO: Garante que o preço seja tratado como número
            df['price'] = df['price'].astype(float)

            def categorize(price):
                if price < 500: return "Econômico (< 500)"
                elif price < 2000: return "Intermediário (500-2k)"
                return "Premium (> 2k)"
            
            df['Categoria'] = df['price'].apply(categorize)

            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("📈 Preços por Item")
                fig_bar = px.bar(df, x="name", y="price", color="Categoria",
                                 labels={"name": "Produto", "price": "Preço (R$)"})
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_b:
                st.subheader("🍕 Mix de Produtos")
                fig_pie = px.pie(df, names="Categoria", title="Distribuição por Faixa de Preço")
                st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.error("Sessão expirada. Faça login novamente.")
else:
    st.warning("⚠️ Faça login para ver a análise de dados.")