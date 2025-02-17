import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


def home_page():
    st.title("GridVision")
    st.write("Bem-vindo ao sistema GridVision, um hub centralizado de dados elétricos e meteorológicos do Brasil.")
    st.header("Sistema de Notificações")
    
    data = {
        "Data do Evento": [
            "2023-04-01", "2023-04-02", "2023-04-03", 
            "2023-04-04", "2023-04-05", "2023-04-06"
        ],
        "Relevância": [
            "🔥 Alta", "⚠️ Média", "🙂 Baixa", 
            "🔥 Alta", "⚠️ Média", "🙂 Baixa"
        ],
        "Descrição do Evento": [
            "Falha em subestação no Sul",
            "Manutenção programada na região Sudeste",
            "Variação de tensão detectada no Nordeste",
            "Sobrecarga na rede de transmissão no Centro-Oeste",
            "Interrupção temporária devido a tempestade no Norte",
            "Atraso na manutenção preventiva no Sudeste"
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)


def weather_page():
    st.header("Previsão do Tempo")
    st.subheader("Previsão do tempo nos proximos dias")
    

    brazil_center = [-14.2350, -51.9253]
    

    np.random.seed(42)
    latitudes = np.random.uniform(-33, 5, 150)
    longitudes = np.random.uniform(-74, -34, 150)  
    intensities = np.random.uniform(0, 100, 150)
    heat_data = pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes,
        "intensity": intensities
    })
    

    layer = pdk.Layer(
        "HeatmapLayer",
        data=heat_data,
        get_position='[lon, lat]',
        get_weight="intensity",
        radiusPixels=100,  
        colorRange=[
            [0, 0, 255, 0],
            [0, 0, 255, 64],
            [0, 0, 255, 128],
            [0, 0, 255, 192],
            [0, 0, 255, 255]
        ]
    )
    
    view_state = pdk.ViewState(
        latitude=brazil_center[0],
        longitude=brazil_center[1],
        zoom=4,
        pitch=0,
    )
    
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(deck)


def financial_page():
    st.header("Dados Financeiros")
    

    dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
    kpis = ["IPCA", "IGPM", "Taxa Tr", "Cambio"]
    data = []
    np.random.seed(42)
    for kpi in kpis:
        for d in dates:
            data.append({
                "date": d,
                "value": np.random.uniform(0, 100),
                "label": kpi
            })
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)
    for i, kpi in enumerate(kpis):
        df_kpi = df[df["label"] == kpi]
        fig = px.line(df_kpi, x="date", y="value", title=kpi,
                      labels={"date": "Data", "value": kpi})
        if i % 2 == 0:
            col1.plotly_chart(fig, use_container_width=True)
        else:
            col2.plotly_chart(fig, use_container_width=True)


def grid_page():
    st.header("Dados da Rede Elétrica")

    csv_files = [f"grid_data_{i}.csv" for i in range(1, 7)]

    cols = st.columns(2)
    for i, file_name in enumerate(csv_files):
        dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
        df = pd.DataFrame({
            "date": dates,
            "value": np.random.uniform(0, 100, len(dates)),
            "label": file_name.split(".")[0]
        })
        fig = px.line(df, x="date", y="value", title=df["label"].iloc[0],
                      labels={"date": "Data", "value": df["label"].iloc[0]})
        cols[i % 2].plotly_chart(fig, use_container_width=True)


if "page" not in st.session_state:
    st.session_state.page = "Home"


if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Previsão do Tempo"):
    st.session_state.page = "Previsão do Tempo"
if st.sidebar.button("Dados Financeiros"):
    st.session_state.page = "Dados Financeiros"
if st.sidebar.button("Rede Elétrica"):
    st.session_state.page = "Rede Elétrica"

page = st.session_state.page


if page == "Home":
    home_page()
elif page == "Previsão do Tempo":
    weather_page()
elif page == "Dados Financeiros":
    financial_page()
elif page == "Rede Elétrica":
    grid_page()
