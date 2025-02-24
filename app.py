import streamlit as st
import random

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Sidebar para cargar archivo
    st.sidebar.header("Cargar Lista de Alumnos")
    uploaded_file = st.sidebar.file_uploader("Seleccione un archivo .txt", type=['txt'])
    
    # Lista de nombres
    nombres = []
    
    # Procesar archivo cargado
    if uploaded_file is not None:
        # Leer el archivo
        file_contents = uploaded_file.getvalue().decode("utf-8")
        # Dividir por líneas y limpiar
        nombres = [name.strip() for name in file_contents.split('\n') if name.strip()]
        
        # Mostrar cuántos nombres se cargaron
        st.sidebar.success(f"Se cargaron {len(nombres)} nombres")
    
    # Botón para girar la ruleta
    if st.sidebar.button("Girar Ruleta") and nombres:
        # Mostrar ruleta usando emojis
        st.markdown("### 🎡 Ruleta Girando...")
        
        # Efecto de giro
        for _ in range(5):
            st.write(random.choice(nombres))
        
        # Seleccionar ganador
        winner = random.choice(nombres)
        
        # Mostrar ganador
        st.markdown(f"### 🏆 ¡GANADOR! 🏆")
        st.markdown(f"## {winner}")
    
    # Advertencia si no hay nombres
    elif st.sidebar.button("Girar Ruleta"):
        st.warning("Por favor, cargue un archivo con nombres de alumnos")

if __name__ == "__main__":
    main()
