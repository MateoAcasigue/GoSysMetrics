import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard de Métricas del Sistema",
    page_icon="🖥️",
    layout="wide"
)

# --- Estilo para los gráficos ---
sns.set_style("darkgrid")
sns.set_palette("viridis")

# --- Funciones de Lógica ---

def initialize_state():
    """Inicializa el estado de la sesión si no existe."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.metrics = {
            "CPU": {"value": 0, "last_update": time.time(), "interval": 1, "history": []},
            "RAM": {"value": 0, "last_update": time.time(), "interval": 2, "history": []},
            "Disco": {"value": 0, "last_update": time.time(), "interval": 3, "history": []},
        }
        st.session_state.metrics_processed_count = 0
        
        with open("metrics_log.txt", "w") as f:
            f.write("--- Inicio del Log de Métricas ---\n")

def log_metric_to_file(name, value):
    """Añade una línea de registro al archivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {name}: {value}%\n"
    with open("metrics_log.txt", "a") as f:
        f.write(log_line)

def update_metrics():
    """Actualiza las métricas si ha pasado su intervalo de tiempo."""
    now = time.time()
    for name, data in st.session_state.metrics.items():
        if now - data["last_update"] >= data["interval"]:
            new_value = random.randint(0, 100)
            st.session_state.metrics[name]["value"] = new_value
            st.session_state.metrics[name]["last_update"] = now
            st.session_state.metrics[name]["history"].append(new_value)
            st.session_state.metrics_processed_count += 1
            log_metric_to_file(name, new_value)

# --- Interfaz de Usuario ---

st.title("🖥️ Dashboard de Métricas del Sistema (Simulado)")
st.markdown("Esta aplicación replica la lógica de un programa en Go y la visualiza en tiempo real.")

initialize_state()

placeholder = st.empty()

while True:
    update_metrics()

    with placeholder.container():
        # --- SECCIÓN DE MÉTRICAS Y BARRAS ---
        cpu_val = st.session_state.metrics["CPU"]["value"]
        ram_val = st.session_state.metrics["RAM"]["value"]
        disk_val = st.session_state.metrics["Disco"]["value"]
        count = st.session_state.metrics_processed_count

        st.markdown("### Métricas Principales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Uso de CPU", f"{cpu_val}%")
        col2.metric("Uso de RAM", f"{ram_val}%")
        col3.metric("Uso de Disco", f"{disk_val}%")

        st.markdown("### Visualización en Barras")
        st.text(f"CPU ({st.session_state.metrics['CPU']['interval']}s)")
        st.progress(cpu_val / 100.0)
        st.text(f"RAM ({st.session_state.metrics['RAM']['interval']}s)")
        st.progress(ram_val / 100.0)
        st.text(f"Disco ({st.session_state.metrics['Disco']['interval']}s)")
        st.progress(disk_val / 100.0)
        
        st.info(f"**Total de Métricas Procesadas:** {count}")
        st.markdown("---")

        # --- SECCIÓN: HISTOGRAMAS DE DISTRIBUCIÓN ---
        st.markdown("### Distribución Histórica de Métricas")
        hist_col1, hist_col2, hist_col3 = st.columns(3)

        for col, name in zip([hist_col1, hist_col2, hist_col3], ["CPU", "RAM", "Disco"]):
            with col:
                history = st.session_state.metrics[name]["history"]
                if len(history) > 1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(data=history, kde=True, ax=ax, bins=15)
                    ax.set_title(f"Distribución de {name}")
                    ax.set_xlabel("Uso (%)")
                    ax.set_ylabel("Frecuencia")
                    ax.set_xlim(0, 100)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.text(f"Esperando más datos para {name}...")

        # --- SECCIÓN DEL LOG ---
        st.markdown("---")
        st.subheader("Log de Métricas en Vivo")
        with open("metrics_log.txt", "r") as f:
            log_content_text = f.read()
        
        with st.expander("Ver contenido del archivo metrics_log.txt"):
            st.code(log_content_text, language="text")

    time.sleep(0.5)

