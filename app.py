import streamlit as st
import random
import plotly.graph_objs as go
import time

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
    
    # Preparar frames de animación
    frames = []
    for rotacion in rotaciones:
        frame = go.Figure(data=[go.Pie(
            labels=nombres,
            values=[1]*n,  # Secciones iguales
            hole=0.3,  # Efecto de dona
            marker_colors=colores[:n],
            textinfo='label',
            textposition='inside',
            rotation=rotacion  # Rotación dinámica
        )])
        
        # Configurar layout
        frame.update_layout(
            height=600,
            width=600,
            showlegend=False
        )
        
        frames.append(frame)
    
    # Calcular ganador
    angulo_seccion = 360 / n
    indice_ganador = int((360 - (rotacion_total % 360)) / angulo_seccion)
    ganador = nombres[indice_ganador % n]
    
    return frames, ganador, rotacion_total

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
                frames, ganador, rotacion_total = crear_ruleta_animada(nombres)
                
                # Animar ruleta
                for frame in frames:
                    with col1:
                        ruleta_container.plotly_chart(frame)
                    time.sleep(0.1)  # Controla la velocidad de la animación
                
                # Frame final con flecha roja
                frame_final = frames[-1]
                
                # Añadir flecha roja en 45 grados
                frame_final.add_annotation(
                    x=0.85, 
                    y=0.85,
                    text='➡️',
                    showarrow=True,
                    arrowcolor='red',
                    arrowsize=2,
                    arrowwidth=3,
                    arrowhead=1,
                    ax=-50,
                    ay=-50
                )
                
                # Mostrar frame final
                with col1:
                    ruleta_container.plotly_chart(frame_final)
    else:
        with col2:
            st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
