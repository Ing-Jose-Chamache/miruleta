import streamlit as st
import random
import plotly.graph_objs as go
import time
import uuid

class RuletaApp:
    def __init__(self):
        # Inicializar estado de la aplicación
        if 'nombres' not in st.session_state:
            st.session_state.nombres = []
        if 'grupos' not in st.session_state:
            st.session_state.grupos = []
        if 'ultima_ruleta_nombres_id' not in st.session_state:
            st.session_state.ultima_ruleta_nombres_id = None
        if 'ultima_ruleta_grupos_id' not in st.session_state:
            st.session_state.ultima_ruleta_grupos_id = None

    def crear_ruleta_animada(self, elementos):
        """Crear animación de giro de ruleta"""
        # Colores pasteles
        colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', 
                   '#87CEFA', '#DDA0DD', '#F0E68C', '#90EE90', '#FFA07A']
        
        # Número de secciones
        n = len(elementos)
        
        # Generar rotación total
        rotacion_total = random.randint(5000, 7000)  # Muchas vueltas
        
        # Calcular ganador
        angulo_seccion = 360 / n
        indice_ganador = int((360 - (rotacion_total % 360)) / angulo_seccion)
        ganador = elementos[indice_ganador % n]
        
        return rotacion_total, ganador

    def crear_figura_ruleta(self, elementos, rotacion_inicial=0):
        """Crear figura de la ruleta con Plotly"""
        # Colores pasteles
        colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', 
                   '#87CEFA', '#DDA0DD', '#F0E68C', '#90EE90', '#FFA07A']
        n = len(elementos)
        
        # Crear figura de la ruleta
        fig = go.Figure(data=[go.Pie(
            labels=elementos,
            values=[1]*n,
            hole=0.3,
            marker_colors=colores[:n],
            textinfo='label',
            textposition='inside',
            rotation=rotacion_inicial  # Rotación inicial
        )])
        
        # Configurar layout
        fig.update_layout(
            height=600,
            width=600,
            showlegend=False,
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
        
        # Dividir la pantalla en tres columnas
        col1, col2, col3 = st.columns([3, 3, 1])
        
        # Columna para Nombres
        with col1:
            st.subheader("Ruleta de Nombres")
            # Sidebar para cargar archivo de nombres
            uploaded_file_nombres = st.file_uploader("Cargar lista de alumnos", type=['txt'], key="nombres_uploader")
        
        # Columna para Grupos
        with col2:
            st.subheader("Ruleta de Grupos")
            # Sidebar para cargar archivo de grupos
            uploaded_file_grupos = st.file_uploader("Cargar lista de grupos", type=['txt'], key="grupos_uploader")
        
        # Cargar nombres
        if uploaded_file_nombres is not None:
            # Leer nombres
            nombres = uploaded_file_nombres.getvalue().decode("utf-8").splitlines()
            st.session_state.nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
            
            with col1:
                # Mostrar número de nombres
                st.success(f"Se cargaron {len(st.session_state.nombres)} nombres")
        
        # Cargar grupos
        if uploaded_file_grupos is not None:
            # Leer grupos
            grupos = uploaded_file_grupos.getvalue().decode("utf-8").splitlines()
            st.session_state.grupos = [grupo.strip() for grupo in grupos if grupo.strip()]
            
            with col2:
                # Mostrar número de grupos
                st.success(f"Se cargaron {len(st.session_state.grupos)} grupos")
        
        # Columna de botones
        with col3:
            # Botón para girar ruleta de nombres
            if (hasattr(st.session_state, 'nombres') and st.session_state.nombres and 
                st.button("Girar Ruleta Nombres", key="girar_nombres")):
                # Generar un ID único para esta ruleta
                st.session_state.ultima_ruleta_nombres_id = str(uuid.uuid4())
                
                # Crear animación de giro
                rotacion_total, ganador = self.crear_ruleta_animada(st.session_state.nombres)
                
                # Contenedor con ID único
                with col1:
                    ruleta_container = st.empty()
                    
                    # Simular giro
                    for i in range(20):
                        rotacion_actual = int(rotacion_total * (i + 1) / 20)
                        fig = self.crear_figura_ruleta(st.session_state.nombres, rotacion_actual)
                        
                        # Usar key con ID único para prevenir errores
                        ruleta_container.plotly_chart(
                            fig, 
                            use_container_width=True, 
                            key=f'{st.session_state.ultima_ruleta_nombres_id}_{i}'
                        )
                        time.sleep(0.1)  # Pequeña pausa entre frames
            
            # Botón para girar ruleta de grupos
            if (hasattr(st.session_state, 'grupos') and st.session_state.grupos and 
                st.button("Girar Ruleta Grupos", key="girar_grupos")):
                # Generar un ID único para esta ruleta
                st.session_state.ultima_ruleta_grupos_id = str(uuid.uuid4())
                
                # Crear animación de giro
                rotacion_total, ganador = self.crear_ruleta_animada(st.session_state.grupos)
                
                # Contenedor con ID único
                with col2:
                    ruleta_container = st.empty()
                    
                    # Simular giro
                    for i in range(20):
                        rotacion_actual = int(rotacion_total * (i + 1) / 20)
                        fig = self.crear_figura_ruleta(st.session_state.grupos, rotacion_actual)
                        
                        # Usar key con ID único para prevenir errores
                        ruleta_container.plotly_chart(
                            fig, 
                            use_container_width=True, 
                            key=f'{st.session_state.ultima_ruleta_grupos_id}_{i}'
                        )
                        time.sleep(0.1)  # Pequeña pausa entre frames

def main():
    app = RuletaApp()
    app.run()

if __name__ == "__main__":
    main()
# Editado por José Yván Chamache para evitar eliminación automática de Codespace (25/08/2025)


