import streamlit as st
import random
import math
import plotly.graph_objs as go

def create_wheel_plot(nombres, colors):
    """Create a plotly wheel plot."""
    n = len(nombres)
    angle_per_section = 360 / n
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=[1]*n,  # Equal sections
        hole=0.3,  # Create a donut chart effect
        marker_colors=colors[:n],  # Use colors
        textinfo='label',
        rotation=random.randint(0, 360)  # Random rotation
    )])
    
    # Update layout
    fig.update_layout(
        title='Ruleta de Selección',
        showlegend=False,
        height=600,
        width=600
    )
    
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
            # Create wheel plot
            fig = create_wheel_plot(nombres, default_colors)
            
            # Display wheel
            st.plotly_chart(fig)
            
            # Select and display winner
            winner_index = random.randint(0, len(nombres) - 1)
            
            st.markdown(f"### 🏆 ¡GANADOR! 🏆")
            st.markdown(f"## {nombres[winner_index]}")
        else:
            st.warning("Por favor, ingrese al menos un nombre.")

if __name__ == "__main__":
    main()
