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
            title='Ruleta de Selección de Alumnos',
            height=600,
            width=600,
            showlegend=False
        )
        
        # Añadir flecha
        frame.add_annotation(
            x=0.5, 
            y=1.15,
            text='➡️',
            showarrow=False,
            font=dict(size=50)
        )
        
        frames.append(frame)
    
    # Calcular ganador
    angulo_seccion = 360 / n
    indice_ganador = int((360 - (rotacion_total % 360)) / angulo_seccion)
    ganador = nombres[indice_ganador % n]
    
    return frames, ganador

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    uploaded_file = st.sidebar.file_uploader("Cargar lista de alumnos", type=['txt'])
    
    # Contenedor para la ruleta
    ruleta_container = st.empty()
    
    # Cargar nombres
    if uploaded_file is not None:
        # Leer nombres
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        # Mostrar número de nombres
        st.sidebar.success(f"Se cargaron {len(nombres)} nombres")
        
        # Botón para girar
        if st.sidebar.button("Girar Ruleta"):
            # Crear animación de giro
            frames, ganador = crear_ruleta_animada(nombres)
            
            # Animar ruleta
            for frame in frames:
                ruleta_container.plotly_chart(frame)
                time.sleep(0.1)  # Controla la velocidad de la animación
            
            # Mostrar ganador final
            st.markdown("### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {ganador}")
    else:
        st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
