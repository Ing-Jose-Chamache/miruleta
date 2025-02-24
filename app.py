import streamlit as st
import random
import plotly.graph_objs as go

def crear_ruleta(nombres):
    """Crear ruleta interactiva con Plotly"""
    # Colores pasteles
    colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', 
               '#FFD700', '#98FB98', '#87CEFA', '#DDA0DD', '#F0E68C']
    
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
        rotation=random.randint(0, 360)  # Rotación aleatoria
    )])
    
    # Configurar layout
    fig.update_layout(
        title='Ruleta de Selección de Alumnos',
        annotations=[
            dict(
                x=0.5,
                y=1.1,
                text='➡️',  # Flecha
                showarrow=False,
                font=dict(size=50)
            )
        ],
        height=600,
        width=600
    )
    
    return fig

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    uploaded_file = st.sidebar.file_uploader("Cargar lista de alumnos", type=['txt'])
    
    if uploaded_file is not None:
        # Leer nombres
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        # Mostrar número de nombres
        st.sidebar.success(f"Se cargaron {len(nombres)} nombres")
        
        # Botón para girar
        if st.sidebar.button("Girar Ruleta"):
            # Crear ruleta
            fig = crear_ruleta(nombres)
            
            # Mostrar ruleta
            st.plotly_chart(fig)
            
            # Seleccionar ganador (aleatorio)
            ganador = random.choice(nombres)
            
            # Mostrar ganador
            st.sidebar.markdown("### 🏆 ¡GANADOR! 🏆")
            st.sidebar.markdown(f"## {ganador}")

if __name__ == "__main__":
    main()
