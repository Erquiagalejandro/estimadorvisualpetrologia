import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Estimador Visual de Porcentajes", layout="centered")

st.title("Estimador Visual de Porcentajes")
st.write("Generador interactivo con cobertura real de píxeles.")

col1, col2 = st.columns(2)

with col1:
    porcentaje_obj = st.slider("% Objetivo Real", min_value=1.0, max_value=99.0, value=10.0, step=1.0)
    granulometria = st.selectbox("Granulometría", ["Fino", "Medio", "Grueso"])

with col2:
    forma = st.selectbox("Geometría", ["Mezcla", "Óvalo", "Rectángulo"])
    semillero = st.number_input("Semilla / Muestra", min_value=1, max_value=1000, value=1, step=1)

np.random.seed(int(semillero))

res = 400
y_grid, x_grid = np.ogrid[-1:1:complex(0, res), -1:1:complex(0, res)]
mascara_circulo = (x_grid**2 + y_grid**2) <= 1.0
area_circulo_px = np.sum(mascara_circulo)

imagen_negra = np.zeros((res, res), dtype=bool)

escala = {'Fino': 0.03, 'Medio': 0.07, 'Grueso': 0.14}
r_med = escala[granulometria]

x_coords = np.linspace(-1, 1, res)
y_coords = np.linspace(-1, 1, res)

max_pasos = 3000
paso = 0

while paso < max_pasos:
    negros_en_circulo = np.sum(imagen_negra & mascara_circulo)
    pct_actual = (negros_en_circulo / area_circulo_px) * 100
    
    if pct_actual >= porcentaje_obj:
        break

    # Detectar píxeles blancos que quedan sin cubrir dentro del círculo
    huecos_y, huecos_x = np.where((~imagen_negra) & mascara_circulo)
    
    if len(huecos_y) == 0:
        break

    # Seleccionar un hueco blanco al azar para ubicar el nuevo grano
    idx = np.random.randint(0, len(huecos_y))
    cy = y_coords[huecos_y[idx]]
    cx = x_coords[huecos_x[idx]]

    tipo_actual = forma
    if forma == 'Mezcla':
        tipo_actual = np.random.choice(['Óvalo', 'Rectángulo'])

    w = np.random.uniform(r_med * 0.7, r_med * 1.3)
    h = np.random.uniform(r_med * 0.7, r_med * 1.3)
    angulo = np.random.uniform(0, np.pi)

    xr = (x_grid - cx) * np.cos(angulo) + (y_grid - cy) * np.sin(angulo)
    yr = -(x_grid - cx) * np.sin(angulo) + (y_grid - cy) * np.cos(angulo)

    if tipo_actual == 'Óvalo':
        figura = ((xr / (w/2))**2 + (yr / (h/2))**2) <= 1.0
    else:
        figura = (np.abs(xr) <= w/2) & (np.abs(yr) <= h/2)

    imagen_negra |= figura
    paso += 1

imagen_final = imagen_negra & mascara_circulo
porcentaje_real = (np.sum(imagen_final) / area_circulo_px) * 100

fig, ax = plt.subplots(figsize=(6, 6))
canvas = np.ones((res, res, 3))
canvas[imagen_final] = [0, 0, 0]

ax.imshow(canvas)
circulo_borde = plt.Circle((res/2, res/2), res/2 - 1, color='black', fill=False, lw=2)
ax.add_patch(circulo_borde)
plt.axis('off')

st.pyplot(fig)
st.info(f"**Porcentaje real alcanzado:** {porcentaje_real:.2f}%")
