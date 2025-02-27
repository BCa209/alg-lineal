import numpy as np
import plotly.graph_objects as go
import streamlit as st

def combinaciones_lineales(vectores, coeficientes):
    vectores = np.array(vectores)
    coeficientes = np.array(coeficientes).reshape(-1, 1)
    resultado = vectores.T @ coeficientes
    return resultado.flatten()

def genera_Rn(vectores, n):
    matriz = np.array(vectores).T
    rango = np.linalg.matrix_rank(matriz)
    return rango == n

def graficar_vectores(vectores, resultado):
    dim = len(vectores[0])
    fig = go.Figure()
    colores = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
    
    for i, v in enumerate(vectores):
        if dim == 2:
            fig.add_trace(go.Scatter(x=[0, v[0]], y=[0, v[1]], mode='lines+markers',
                                    name=f"v{i+1}",
                                    line=dict(color=colores[i % len(colores)], width=3)))
        elif dim == 3:
            fig.add_trace(go.Scatter3d(x=[0, v[0]], y=[0, v[1]], z=[0, v[2]], mode='lines+markers',
                                    name=f"v{i+1}",
                                    line=dict(color=colores[i % len(colores)], width=5)))

    if dim == 2:
        fig.add_trace(go.Scatter(x=[0, resultado[0]], y=[0, resultado[1]], mode='lines+markers',
                                name="Resultado", line=dict(color='black', width=4, dash="dash")))
    elif dim == 3:
        fig.add_trace(go.Scatter3d(x=[0, resultado[0]], y=[0, resultado[1]], z=[0, resultado[2]], mode='lines+markers',
                                name="Resultado", line=dict(color='black', width=6, dash="dash")))

    valores = np.array(vectores + [resultado.tolist()])
    min_val, max_val = valores.min() - 1, valores.max() + 1

    fig.update_layout(scene=dict(
        xaxis=dict(range=[min_val, max_val]),
        yaxis=dict(range=[min_val, max_val]),
        zaxis=dict(range=[min_val, max_val]) if dim == 3 else {}
    ), title="Gráfica Interactiva de Vectores", margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig)

def main():
    st.title("Combinaciones Lineales en Álgebra Lineal")
    input_text = st.text_area("Introduce los vectores separados por comas y líneas (ejemplo: '1,2' en una línea y '3,4' en otra):")
    input_coef = st.text_input("Introduce los coeficientes separados por comas (ejemplo: '0.5, 2'):")
    input_dim = st.number_input("Determina si genera R^n (ingresa n):", min_value=1, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        calcular_btn = st.button("Calcular Combinación Lineal")
    with col2:
        determinar_btn = st.button("Determinar")
    
    if calcular_btn:
        try:
            lineas = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
            vectores = [list(map(float, line.split(','))) for line in lineas]
            coeficientes = list(map(float, input_coef.split(',')))
            
            dimensiones = {len(v) for v in vectores}
            if len(dimensiones) > 1:
                st.error("Error: Todos los vectores deben tener la misma cantidad de dimensiones.")
                return
            
            if len(coeficientes) != len(vectores):
                st.error("Error: La cantidad de coeficientes debe coincidir con la cantidad de vectores.")
                return
            
            resultado = combinaciones_lineales(vectores, coeficientes)
            st.write("Resultado de la combinación lineal:", resultado)
            
            if len(vectores[0]) in [2, 3]:
                graficar_vectores(vectores, resultado)
        except ValueError:
            st.error("Error: Asegúrate de que todos los valores sean números y estén correctamente separados por comas.")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
    
    if determinar_btn:
        try:
            lineas = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
            vectores = [list(map(float, line.split(','))) for line in lineas]
            
            if genera_Rn(vectores, input_dim):
                st.markdown(f'<div style="background-color:#0D6719;padding:10px;border-radius:5px;">Los vectores generan R^{int(input_dim)}.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color:#7F0000;padding:10px;border-radius:5px;">Los vectores NO generan R^{int(input_dim)}.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error inesperado: {e}")
