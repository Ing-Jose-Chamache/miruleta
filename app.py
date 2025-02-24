import streamlit as st
import random
import plotly.graph_objs as go
import time
import math

def crear_ruleta_animada(nombres):
    """Crear animación de giro de ruleta"""
    # Colores pasteles
    colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
    
    # Número de secciones
    n = len(nombres)
    
    # Generar secuencia de rotaciones para simular giro
    rotaciones = []
    rotacion_total = random.randint(720, 3600)  # 2-10 vueltas
    
    # Crear pasos de rotación
    pasos = 20
    for i in range(pasos):
        # Interpolar la rotación
        rotacion_actual = int(rotacion_total * (i + 1) / pasos)
        rotaciones.append(rotacion_actual)
    
    # Calcular ganador
    angulo_seccion = 360 / n
    indice_ganador = int((360 - (rotacion_total % 360)) / angulo_seccion)
    ganador = nombres[indice_ganador % n]
    
    return rotaciones, ganador, indice_ganador % n

def main():
    st.set_page_config(layout="wide")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Sidebar para cargar archivo
        uploaded_file = st.file_uploader("Cargar lista de alumnos", type=['txt'])
    
    # Contenedor para la ruleta
    with col1:
        ruleta_container = st.empty()
    
    # Cargar nombres
    if uploaded_file is not None:
        # Leer nombres
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        with col2:
            # Mostrar número de nombres
            st.success(f"Se cargaron {len(nombres)} nombres")
        
        with col2:
            # Botón para girar
            if st.button("Girar Ruleta"):
                # Crear animación de giro
                rotaciones, ganador, indice_ganador = crear_ruleta_animada(nombres)
                
                # Colores pasteles
                colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
                n = len(nombres)
                
                # Animar ruleta
                for rotacion in rotaciones:
                    # Crear figura de la ruleta
                    fig = go.Figure(data=[go.Pie(
                        labels=nombres,
                        values=[1]*n,
                        hole=0.3,
                        marker_colors=colores[:n],
                        textinfo='label',
                        textposition='inside',
                        rotation=rotacion
                    )])
                    
                    # Configurar layout
                    fig.update_layout(
                        height=600,
                        width=600,
                        showlegend=False
                    )
                    
                    # Mostrar ruleta
                    with col1:
                        ruleta_container.plotly_chart(fig)
                    time.sleep(0.1)
                
                # Crear figura final
                fig_final = go.Figure(data=[go.Pie(
                    labels=nombres,
                    values=[1]*n,
                    hole=0.3,
                    marker_colors=colores[:n],
                    textinfo='label',
                    textposition='inside',
                    rotation=rotaciones[-1]
                )])
                
                # Configurar layout
                fig_final.update_layout(
                    height=600,
                    width=600,
                    showlegend=False,
                    annotations=[
                        dict(
                            x=0.5,  # Centrado horizontalmente
                            y=1.15,  # Posición en la parte superior
                            text='👆',  # Emoji de mano señalando hacia abajo
                            font=dict(size=100),  # Tamaño grande
                            showarrow=False
                        )
                    ]
                )
                
                # Mostrar ruleta final
                with col1:
                    ruleta_container.plotly_chart(fig_final)
    else:
        with col2:
            st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
