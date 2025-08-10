# ui_app.py
"""
Script da UI em Streamlit para a Calculadora de Pesquisa Operacional.
Este script importa funções de um módulo separado que consome a API do OpenStreetMap.
"""
import streamlit as st
import pandas as pd
import time
from io import BytesIO, StringIO
from osm import geocode_address, get_osrm_matrix

st.set_page_config(page_title="OR Engineering", layout="wide")

st.title("🗺️ OR Engineering")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Endereços de Origem")
    origins_input = st.text_area("Insira um endereço por linha", key="origens_input")

with col2:
    st.subheader("Endereços de Destino")
    destinations_input = st.text_area("Insira um endereço por linha", key="destinos_input")

# Botão para selecionar o tipo de unidade de medida para a distância
with col1:
    st.subheader("Unidade de Medida Distância")
    dist_unit = st.selectbox("Selecione a unidade de medida para distâncias:", ("km", "m"))

# Botão para calcular o tipo de unidade de medida para o tempo
with col2:
    st.subheader("Unidade de Medida Tempo")
    time_unit = st.selectbox("Selecione a unidade de medida para tempos:", ("s", "min", "h"))

# Selecione o formato de download
tipo_download = st.selectbox("Selecione o formato de download:", ("Excel", "CSV"))

if st.button("Calcular Matriz"):
    origins = [line.strip() for line in origins_input.splitlines() if line.strip()]
    destinations = [line.strip() for line in destinations_input.splitlines() if line.strip()]
    
    total = len(origins) + len(destinations)
    progress_bar = st.progress(0)
    progress_step = 1 / total

    info = st.info("Geocodificando endereços...")

    orig_coords, orig_names = [], []
    for i, o in enumerate(origins):
        res = geocode_address(o)
        if res is None:
            st.error(f"Não foi possível geocodificar: {o}")
            st.stop()
        lat, lon, name = res
        orig_coords.append((lat, lon))
        orig_names.append(name)
        time.sleep(1.1)
        progress_bar.progress((i + 1) * progress_step)

    dest_coords, dest_names = [], []
    for j, d in enumerate(destinations):
        res = geocode_address(d)
        if res is None:
            st.error(f"Não foi possível geocodificar: {d}")
            st.stop()
        lat, lon, name = res
        dest_coords.append((lat, lon))
        dest_names.append(name)
        time.sleep(1.1)
        progress_bar.progress((len(origins) + j + 1) * progress_step)

    finish = st.success("Geocodificação concluída. Obtendo matriz...")
    matrix = get_osrm_matrix(orig_coords, dest_coords)

    # Retorno das distâncias
    match dist_unit:
        case "m":
            distances = matrix.get("distances")
        case "km":
            distances = list(map(lambda sublista: list(map(lambda x: x / 1000, sublista)), matrix.get("distances")))
    # Retorno dos tempos
    match time_unit:
        case "s":
            durations = matrix.get("durations")
        case "min":
            durations = list(map(lambda sublista: list(map(lambda x: x / 60, sublista)), matrix.get("durations")))
        case "h":
            durations = list(map(lambda sublista: list(map(lambda x: x / 3600, sublista)), matrix.get("durations")))

    df_dist = pd.DataFrame(distances, index=orig_names, columns=dest_names)
    df_dur = pd.DataFrame(durations, index=orig_names, columns=dest_names)

    st.subheader(f"Matriz de Distâncias ({dist_unit})")
    st.dataframe(df_dist)
    st.subheader(f"Matriz de Duração ({time_unit})")
    st.dataframe(df_dur)

    # Remoção dos avisos de progresso e informação
    progress_bar.empty()
    info.empty()
    finish.empty()

    match tipo_download:
        case "Excel":
                # Excel - distâncias
                buffer_dist = BytesIO()
                df_dist.to_excel(buffer_dist, index=False, engine='openpyxl')
                buffer_dist.seek(0)
                st.download_button(
                    label="Baixar Excel (distâncias)",
                    data=buffer_dist,
                    file_name="distances_matrix.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # Excel - duração
                buffer_dur = BytesIO()
                df_dur.to_excel(buffer_dur, index=False, engine='openpyxl')
                buffer_dur.seek(0)
                st.download_button(
                    label="Baixar Excel (duração)",
                    data=buffer_dur,
                    file_name="durations_matrix.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        case "CSV":
            # CSV - duração
            csv_dur = df_dur.to_csv(index=False)
            st.download_button(
                label="Baixar CSV (duração)",
                data=csv_dur,
                file_name="durations_matrix.csv",
                mime="text/csv"
            )

            # CSV - distâncias
            csv_dist = df_dist.to_csv(index=False)
            st.download_button(
                label="Baixar CSV (distâncias)",
                data=csv_dist,
                file_name="distances_matrix.csv",
                mime="text/csv"
            )
