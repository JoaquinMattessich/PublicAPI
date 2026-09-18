import streamlit as st
import requests
from google.transit import gtfs_realtime_pb2

st.set_page_config(page_title="Colectivos CABA", page_icon="🚌", layout="wide")
st.title("🚌 Posiciones de Colectivos de CABA en Tiempo Real")

st.sidebar.header("Credenciales de la API")
client_id = st.sidebar.text_input("Client ID", value="", type="password")
client_secret = st.sidebar.text_input("Client Secret", value="", type="password")

URL = "https://apitransporte.buenosaires.gob.ar/colectivos/feed-gtfs"

if st.button("Obtener Ubicaciones de Colectivos", type="primary"):
    if not client_id or not client_secret:
        st.error("⚠️ Debes ingresar el Client ID y Client Secret en el panel izquierdo.")
    else:
        try:
            with st.spinner("Consultando servidor de Transporte CABA..."):
                response = requests.get(URL, params={"client_id": client_id, "client_secret": client_secret}, timeout=15)
                
            if response.status_code == 200:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(response.content)
                
                colectivos = []
                for entity in feed.entity:
                    if entity.HasField('vehicle'):
                        pos = entity.vehicle.position
                        colectivos.append({
                            "lat": pos.latitude,
                            "lon": pos.longitude,
                            "id": entity.vehicle.vehicle.label or entity.id
                        })
                
                st.success(f"✅ Se detectaron {len(colectivos)} colectivos en tiempo real.")
                st.map(colectivos)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

