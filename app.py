import streamlit as st
import random
import plotly.graph_objs as go

def crear_ruleta(nombres, rotacion=0):
    """Crear ruleta interactiva con Plotly y rotación"""
    # Colores pasteles
    colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
    
    # Número de secciones
    n = len(nombres)
    
    # Preparar datos para la ruleta
    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=[1]*n,  # Secciones iguales
        hole=0.3,  # Efecto de dona
        marker_colors=colores[:n],
        textinfo='label',
        textposition='inside',
        rotation=rotacion  # Añadir rotación
    )])
    
    # Configurar layout
    fig.update_layout(
        title='Ruleta de Selección de Alumnos',
        height=600,
        width=600,
        showlegend=False
    )
    
    # Añadir flecha
    fig.add_annotation(
        x=0.5, 
        y=1.15,
        text='➡️',
        showarrow=False,
        font=dict(size=50)
    )
    
    return fig

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    uploaded_file = st.sidebar.file_uploader("Cargar lista de alumnos", type=['txt'])
    
    # Estado para almacenar nombres y ganador
    if 'nombres' not in st.session_state:
        st.session_state.nombres = []
    if 'rotacion' not in st.session_state:
        st.session_state.rotacion = 0
    if 'ganador' not in st.session_state:
        st.session_state.ganador = None
    
    if uploaded_file is not None:
        # Leer nombres
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        st.session_state.nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        # Mostrar número de nombres
        st.sidebar.success(f"Se cargaron {len(st.session_state.nombres)} nombres")
    
    # Verificar si hay nombres cargados
    if st.session_state.nombres:
        # Botón para girar
        if st.button("Girar Ruleta"):
            # Generar rotación aleatoria (varias vueltas completas)
            st.session_state.rotacion = random.randint(720, 3600)
            
            # Crear ruleta con rotación
            fig = crear_ruleta(st.session_state.nombres, st.session_state.rotacion)
            
            # Mostrar ruleta
            st.plotly_chart(fig)
            
            # Calcular ganador
            n = len(st.session_state.nombres)
            angulo_seccion = 360 / n
            indice_ganador = int((360 - (st.session_state.rotacion % 360)) / angulo_seccion)
            st.session_state.ganador = st.session_state.nombres[indice_ganador % n]
            
            # Mostrar ganador
            st.markdown("### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {st.session_state.ganador}")
        
        # Si ya hay un ganador previo, mostrar ruleta con última rotación
        elif st.session_state.ganador:
            fig = crear_ruleta(st.session_state.nombres, st.session_state.rotacion)
            st.plotly_chart(fig)
            
            # Mostrar ganador previo
            st.markdown("### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {st.session_state.ganador}")
    else:
        st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
