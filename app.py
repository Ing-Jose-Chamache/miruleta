import streamlit as st
import random
import plotly.graph_objs as go

def crear_ruleta(nombres):
    """Crear ruleta interactiva con Plotly y giro aleatorio"""
    # Colores pasteles
    colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', 
               '#FFD700', '#98FB98', '#87CEFA', '#DDA0DD', '#F0E68C']
    
    # Número de secciones
    n = len(nombres)
    
    # Rotación aleatoria con múltiples vueltas
    rotacion_base = random.randint(3600, 7200)  # 10-20 vueltas completas
    
    # Preparar datos para la ruleta
    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=[1]*n,  # Secciones iguales
        hole=0.3,  # Efecto de dona
        marker_colors=colores[:n],
        textinfo='label',
        textposition='inside',
        rotation=rotacion_base  # Rotación dinámica
    )])
    
    # Configurar layout para giro
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
        width=600,
        updatemenus=[{
            'buttons': [{
                'args': [{'pie.rotation': rotacion_base}, 
                         {'duration': 3000, 'transition': {'duration': 3000}}],
                'label': 'Girar',
                'method': 'animate'
            }],
            'direction': 'left',
            'pad': {'r': 10, 't': 10},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'top'
        }]
    )
    
    return fig, rotacion_base

def calcular_ganador(nombres, rotacion, n):
    """Calcular el ganador basado en la rotación"""
    # Ángulo por sección
    angulo_seccion = 360 / n
    
    # Ajustar rotación
    rotacion_final = rotacion % 360
    
    # Calcular índice del ganador
    indice_ganador = int((360 - rotacion_final) / angulo_seccion)
    
    return nombres[indice_ganador % n]

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
            fig, rotacion = crear_ruleta(nombres)
            
            # Mostrar ruleta
            st.plotly_chart(fig)
            
            # Calcular ganador
            ganador = calcular_ganador(nombres, rotacion, len(nombres))
            
            # Mostrar ganador
            st.sidebar.markdown("### 🏆 ¡GANADOR! 🏆")
            st.sidebar.markdown(f"## {ganador}")

if __name__ == "__main__":
    main()
