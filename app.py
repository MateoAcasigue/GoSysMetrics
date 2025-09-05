import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard de Métricas del Sistema",
    page_icon="🖥️",
    layout="wide"
)

# --- Funciones de Lógica ---

def initialize_state():
    """Inicializa el estado de la sesión si no existe."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.metrics = {
            "CPU": {"value": 0, "last_update": time.time(), "interval": 1},
            "RAM": {"value": 0, "last_update": time.time(), "interval": 2},
            "Disco": {"value": 0, "last_update": time.time(), "interval": 3},
        }
        st.session_state.metrics_processed_count = 0
        
        # Limpia el archivo de log al iniciar
        with open("metrics_log.txt", "w") as f:
            f.write("--- Inicio del Log de Métricas ---\n")

def log_metric_to_file(name, value):
    """Añade una línea de registro al archivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {name}: {value}%\n"
    with open("metrics_log.txt", "a") as f:
        f.write(log_line)

def update_metrics():
    """
    Verifica si es tiempo de actualizar alguna métrica según su intervalo.
    Si se actualiza, genera un nuevo valor y lo guarda en el estado.
    """
    now = time.time()
    for name, data in st.session_state.metrics.items():
        if now - data["last_update"] > data["interval"]:
            new_value = random.randint(0, 100)
            st.session_state.metrics[name]["value"] = new_value
            st.session_state.metrics[name]["last_update"] = now
            st.session_state.metrics_processed_count += 1
            log_metric_to_file(name, new_value)

# --- Interfaz de Usuario ---

st.title("🖥️ Dashboard de Métricas del Sistema (Simulado)")
st.markdown("Esta aplicación replica la lógica de un programa en Go y la visualiza en tiempo real.")

# Inicializa el estado la primera vez que se ejecuta el script
initialize_state()

# Contenedor para la parte dinámica del dashboard
placeholder = st.empty()

# Bucle infinito para mantener la aplicación "viva"
while True:
    # 1. Actualiza la lógica de las métricas
    update_metrics()

    # 2. Dibuja la interfaz dentro del contenedor
    with placeholder.container():
        # Extraer valores actuales para fácil acceso
        cpu_val = st.session_state.metrics["CPU"]["value"]
        ram_val = st.session_state.metrics["RAM"]["value"]
        disk_val = st.session_state.metrics["Disco"]["value"]
        count = st.session_state.metrics_processed_count

        st.markdown("### Métricas Principales")
        
        # Mostrar métricas en columnas
        col1, col2, col3 = st.columns(3)
        col1.metric("Uso de CPU", f"{cpu_val}%")
        col2.metric("Uso de RAM", f"{ram_val}%")
        col3.metric("Uso de Disco", f"{disk_val}%")

        st.markdown("### Visualización en Barras")

        # Barras de progreso
        st.text(f"CPU ({st.session_state.metrics['CPU']['interval']}s)")
        st.progress(cpu_val / 100.0)

        st.text(f"RAM ({st.session_state.metrics['RAM']['interval']}s)")
        st.progress(ram_val / 100.0)

        st.text(f"Disco ({st.session_state.metrics['Disco']['interval']}s)")
        st.progress(disk_val / 100.0)
        
        st.info(f"**Total de Métricas Procesadas:** {count}")

        # Expander para mostrar el log
        with st.expander("Ver Log de Métricas en Vivo (metrics_log.txt)"):
            with open("metrics_log.txt", "r") as f:
                # Leemos las líneas y las invertimos para mostrar la más reciente arriba
                log_content = f.readlines()
                st.code("".join(reversed(log_content)), language="text")

    # 3. Espera un breve momento antes de la siguiente iteración
    # Esto controla la fluidez de la UI y evita que el script consuma demasiada CPU.
    time.sleep(0.5)

