import streamlit as st
import random
import math
import plotly.graph_objs as go
import numpy as np

def create_wheel_plot(nombres):
    """Crear una ruleta blanca con nombres"""
    n = len(nombres)
    angle_per_section = 360 / n
    
    # Colores en blanco con bordes grises
    colors = ['white'] * n
    
    # Crear gráfico de pie
    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=[1]*n,  # Secciones iguales
        hole=0.3,  # Efecto de dona
        marker_colors=colors,
        marker_line_color='lightgrey',
        marker_line_width=2,
        textinfo='label',
        textfont=dict(size=14, color='black'),
        rotation=random.randint(0, 360)  # Rotación aleatoria
    )])
    
    # Configurar layout
    fig.update_layout(
        title='Ruleta de Selección',
        showlegend=False,
        height=600,
        width=600,
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                showarrow=False,
                text="Flecha indica el ganador →",
                font=dict(size=12)
            )
        ]
    )
    
    # Añadir flecha
    fig.add_annotation(
        x=0.5, y=1.15,
        text="▼",
        showarrow=False,
        font=dict(size=50, color='red')
    )
    
    return fig

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    st.sidebar.header("Cargar Lista de Alumnos")
    uploaded_file = st.sidebar.file_uploader("Seleccione un archivo .txt", type=['txt'])
    
    # Lista de nombres
    nombres = []
    
    # Procesar archivo cargado
    if uploaded_file is not None:
        # Leer el archivo
        file_contents = uploaded_file.getvalue().decode("utf-8")
        # Dividir por líneas y limpiar
        nombres = [name.strip() for name in file_contents.split('\n') if name.strip()]
        
        # Mostrar cuántos nombres se cargaron
        st.sidebar.success(f"Se cargaron {len(nombres)} nombres")
    
    # Botón para girar la ruleta
    if st.sidebar.button("Girar Ruleta") and nombres:
        # Crear ruleta
        fig = create_wheel_plot(nombres)
        
        # Mostrar ruleta
        st.plotly_chart(fig)
        
        # Seleccionar ganador
        winner_index = random.randint(0, len(nombres) - 1)
        
        # Mostrar ganador
        st.markdown(f"### 🏆 ¡GANADOR! 🏆")
        st.markdown(f"## {nombres[winner_index]}")
    
    # Advertencia si no hay nombres
    elif st.sidebar.button("Girar Ruleta"):
        st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
