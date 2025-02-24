import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def create_wheel_plot(nombres, colors):
    """Create a matplotlib wheel plot."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    
    # Number of sections
    n = len(nombres)
    
    # Angle for each section
    angle_per_section = 360 / n
    
    # Plot colored sections
    for i in range(n):
        start_angle = i * angle_per_section
        end_angle = (i + 1) * angle_per_section
        
        # Create wedge
        wedge = plt.Circle((0.5, 0.5), 0.4, 
                           theta1=start_angle, 
                           theta2=end_angle, 
                           color=colors[i % len(colors)],
                           fill=True)
        ax.add_artist(wedge)
        
        # Add text
        text_angle = math.radians(start_angle + angle_per_section/2)
        text_x = 0.5 + 0.25 * math.cos(text_angle)
        text_y = 0.5 + 0.25 * math.sin(text_angle)
        
        plt.text(text_x, text_y, nombres[i], 
                 horizontalalignment='center', 
                 verticalalignment='center',
                 rotation=start_angle + angle_per_section/2)
    
    # Draw center point
    plt.scatter(0.5, 0.5, color='white', edgecolors='black', s=100)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis('off')
    
    return fig

def main():
    st.title("🎡 Ruleta de Selección")
    
    # Default colors
    default_colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
    
    # Sidebar for input
    st.sidebar.header("Configuración de la Ruleta")
    
    # Text area for names
    nombres_input = st.sidebar.text_area(
        "Lista de Nombres (uno por línea)", 
        value="TUPIA\nALVITES\nCHAVEZ\nESPINOZA\nTORRES"
    )
    
    # Process names
    nombres = [name.strip() for name in nombres_input.split('\n') if name.strip()]
    
    # Button to spin
    if st.sidebar.button("Girar Ruleta"):
        if nombres:
            # Simulate wheel spin
            rotaciones = random.randint(10, 20)  # Multiple full rotations
            winner_index = random.randint(0, len(nombres) - 1)
            
            # Create and display wheel
            fig = create_wheel_plot(nombres, default_colors)
            
            # Wheel display
            st.pyplot(fig)
            
            # Display winner
            st.markdown(f"### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {nombres[winner_index]}")
        else:
            st.warning("Por favor, ingrese al menos un nombre.")

if __name__ == "__main__":
    main()
