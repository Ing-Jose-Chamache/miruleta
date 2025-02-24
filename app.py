import streamlit as st
import random
import plotly.graph_objs as go

def crear_ruleta(nombres):
    """Crear ruleta interactiva con Plotly"""
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
        textposition='inside'
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
    if 'ganador' not in st.session_state:
        st.session_state.ganador = None
    
    if uploaded_file is not None:
        # Leer nombres
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        st.session_state.nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        # Mostrar número de nombres
        st.sidebar.success(f"Se cargaron {len(st.session_state.nombres)} nombres")
    
    # Contenedor para la ruleta
    ruleta_container = st.empty()
    
    # Verificar si hay nombres cargados
    if st.session_state.nombres:
        # Botón para girar
        if st.button("Girar Ruleta"):
            # Crear ruleta
            fig = crear_ruleta(st.session_state.nombres)
            
            # Mostrar ruleta
            ruleta_container.plotly_chart(fig)
            
            # Seleccionar ganador
            st.session_state.ganador = random.choice(st.session_state.nombres)
            
            # Mostrar ganador
            st.markdown("### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {st.session_state.ganador}")
        
        # Si ya hay un ganador previo
        elif st.session_state.ganador:
            # Mostrar ruleta
            fig = crear_ruleta(st.session_state.nombres)
            ruleta_container.plotly_chart(fig)
            
            # Mostrar ganador previo
            st.markdown("### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {st.session_state.ganador}")
    else:
        st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
