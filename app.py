import streamlit as st
import random
import plotly.graph_objs as go
import time

class RuletaApp:
    def __init__(self):
        # Inicializar estado de la aplicación
        if 'nombres' not in st.session_state:
            st.session_state.nombres = []
        if 'rotacion_actual' not in st.session_state:
            st.session_state.rotacion_actual = 0
        if 'ganador' not in st.session_state:
            st.session_state.ganador = None

    def crear_ruleta_animada(self, nombres):
        """Crear animación de giro de ruleta"""
        # Colores pasteles
        colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
        
        # Número de secciones
        n = len(nombres)
        
        # Generar rotación total
        rotacion_total = random.randint(2000, 4000)  # Más rápido y más vueltas
        
        # Calcular ganador
        angulo_seccion = 360 / n
        indice_ganador = int((360 - (rotacion_total % 360)) / angulo_seccion)
        ganador = nombres[indice_ganador % n]
        
        return rotacion_total, ganador

    def crear_figura_ruleta(self, nombres, rotacion):
        """Crear figura de la ruleta con Plotly"""
        # Colores pasteles
        colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
        n = len(nombres)
        
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
            showlegend=False,
            transition=dict(
                duration=1000,  # Duración de la animación
                easing='cubic-in-out'
            ),
            annotations=[
                dict(
                    x=0.5,  # Centrado horizontalmente
                    y=1.15,  # Posición en la parte superior
                    text='👇',  # Emoji de mano señalando hacia abajo
                    font=dict(size=100),  # Tamaño grande
                    showarrow=False
                )
            ]
        )
        
        return fig

    def run(self):
        st.set_page_config(layout="wide")
        
        # Dividir la pantalla en dos columnas
        col1, col2 = st.columns([3, 1])
        
        with col2:
            # Sidebar para cargar archivo
            uploaded_file = st.file_uploader("Cargar lista de alumnos", type=['txt'])
        
        # Cargar nombres
        if uploaded_file is not None:
            # Leer nombres
            nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
            st.session_state.nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
            
            with col2:
                # Mostrar número de nombres
                st.success(f"Se cargaron {len(st.session_state.nombres)} nombres")
        
        # Verificar si hay nombres cargados
        if st.session_state.nombres:
            with col2:
                # Botón para girar
                if st.button("Girar Ruleta"):
                    # Crear animación de giro
                    rotacion, ganador = self.crear_ruleta_animada(st.session_state.nombres)
                    
                    # Crear figura de la ruleta
                    fig = self.crear_figura_ruleta(st.session_state.nombres, rotacion)
                    
                    # Mostrar ruleta
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.warning("Por favor, cargue un archivo con nombres de alumnos")

def main():
    app = RuletaApp()
    app.run()

if __name__ == "__main__":
    main()
