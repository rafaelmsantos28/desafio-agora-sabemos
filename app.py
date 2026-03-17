import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Consulta Qualis CAPES", page_icon="📚", layout="wide")

API_BASE_URL = "http://127.0.0.1:8000"

st.title("Consulta de Classificação QUALIS - CAPES")
st.markdown("Ferramenta de apoio para coordenadores de pós-graduação analisarem as classificações de periódicos científicos.")
st.sidebar.header("Filtros de Busca")

@st.cache_data(ttl=3600)
def fetch_areas():
    try:
        response = requests.get(f"{API_BASE_URL}/areas")
        if response.status_code == 200:
            return response.json().get("areas", [])
    except requests.exceptions.ConnectionError:
        st.sidebar.error("Erro de conexão: Verifique se a API está rodando.")
    return []

areas = fetch_areas()
selected_area = st.sidebar.selectbox("1. Selecione a Área de Avaliação:", [""] + areas)

if selected_area:
    area_response = requests.get(f"{API_BASE_URL}/periodicos/{selected_area}")
    
    if area_response.status_code == 200:
        area_data = area_response.json().get("journals", [])
        df_area = pd.DataFrame(area_data)
        
        available_strata = ["Todos"] + sorted(df_area['estrato'].unique().tolist())
        selected_stratum = st.sidebar.selectbox("2. Filtrar por Classificação (Qualis):", available_strata)
        
        st.divider()

        if selected_stratum == "Todos":
            df_display = df_area
            st.subheader(f"Todos os periódicos da área: {selected_area}")
        else:
            filter_response = requests.get(f"{API_BASE_URL}/periodicos/{selected_area}/{selected_stratum}")
            if filter_response.status_code == 200:
                df_display = pd.DataFrame(filter_response.json().get("journals", []))
                st.subheader(f"Periódicos da área: {selected_area} (Filtro: {selected_stratum})")
            else:
                df_display = pd.DataFrame()
        
        if not df_display.empty:
            col1, col2 = st.columns(2)
            col1.metric("Total de Periódicos Listados", len(df_display))
            a1_count = len(df_display[df_display['estrato'] == 'A1'])
            col2.metric("Periódicos de Excelência (A1)", a1_count)
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            st.divider()
            st.subheader("📊 Distribuição de Classificações")
            strata_counts = df_area['estrato'].value_counts().sort_index()
            st.bar_chart(strata_counts)
        else:
            st.warning("Nenhum periódico encontrado com os filtros selecionados.")
    else:
        st.error("Erro ao buscar os dados da API.")
else:
    st.info("Por favor, selecione uma área de avaliação no menu lateral para iniciar a consulta.")