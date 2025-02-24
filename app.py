import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

def crear_ruleta(nombres):
    """Crear ruleta con secciones de colores"""
    # Colores pasteles
    colores = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', 
               '#FFD700', '#98FB98', '#87CEFA', '#DDA0DD', '#F0E68C']
    
    # Preparar figura
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Número de secciones
    n = len(nombres)
    
    # Ángulo de cada sección
    angulo = 360 / n
    
    # Girar ruleta
    rotacion = random.randint(0, 360)
    
    # Dibujar secciones
    for i in range(n):
        inicio = i * angulo + rotacion
        fin = (i + 1) * angulo + rotacion
        
        color = colores[i % len(colores)]
        
        # Dibujar sector
        ax.add_patch(plt.Wedge((0.5, 0.5), 0.4, inicio, fin, color=color, 
                               width=0.4, edgecolor='white', linewidth=2))
        
        # Agregar texto
        angulo_texto = np.deg2rad(inicio + angulo/2)
        x = 0.5 + 0.25 * np.cos(angulo_texto)
        y = 0.5 + 0.25 * np.sin(angulo_texto)
        
        plt.text(x, y, nombres[i], 
                 rotation=np.rad2deg(angulo_texto)-90,
                 ha='center', va='center', fontsize=10)
    
    # Dibujar centro
    ax.add_patch(plt.Circle((0.5, 0.5), 0.05, color='white', edgecolor='black'))
    
    # Configurar ejes
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis('off')
    
    # Añadir flecha
    plt.arrow(0.5, 1.05, 0, -0.1, head_width=0.05, head_length=0.05, 
              fc='red', ec='red', transform=ax.transAxes)
    
    return fig, rotacion

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    uploaded_file = st.sidebar.file_uploader("Cargar lista de alumnos", type=['txt'])
    
    # Contenedor para la ruleta
    ruleta_container = st.empty()
    
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
            ruleta_container.pyplot(fig)
            
            # Calcular ganador
            n = len(nombres)
            angulo_por_seccion = 360 / n
            indice_ganador = int((360 - (rotacion % 360)) / angulo_por_seccion)
            ganador = nombres[indice_ganador]
            
            # Mostrar ganador
            st.sidebar.markdown("### 🏆 ¡GANADOR! 🏆")
            st.sidebar.markdown(f"## {ganador}")

if __name__ == "__main__":
    main()
