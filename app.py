import streamlit as st
import random
import time

def main():
    st.title("🎡 Ruleta de Selección de Alumnos")
    
    # Archivo de texto
    uploaded_file = st.file_uploader("Cargar archivo de nombres", type="txt")
    
    # Contenedor para mostrar el resultado
    result_container = st.empty()
    winner_container = st.empty()
    
    if uploaded_file is not None:
        # Leer nombres del archivo
        nombres = uploaded_file.getvalue().decode("utf-8").splitlines()
        nombres = [nombre.strip() for nombre in nombres if nombre.strip()]
        
        # Mostrar número de nombres cargados
        st.write(f"Nombres cargados: {len(nombres)}")
        
        # Botón para girar
        if st.button("Girar Ruleta"):
            # Efecto de giro
            for _ in range(5):
                result_container.write(f"🎲 Girando... {random.choice(nombres)}")
                time.sleep(0.5)
            
            # Seleccionar ganador
            ganador = random.choice(nombres)
            
            # Mostrar ganador con flecha
            result_container.markdown(f"### 🏆 ¡GANADOR! 🏆")
            winner_container.markdown(f"## ➡️ {ganador}")

if __name__ == "__main__":
    main()
