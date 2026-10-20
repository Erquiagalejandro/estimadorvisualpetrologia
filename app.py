import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Estimador Visual de Porcentajes", layout="centered")

st.title("Estimador Visual de Porcentajes")
st.write("Generador con medición real de cobertura de píxeles (sin error por solapamiento).")

col1, col2 = st.columns(2)

with col1:
    porcentaje_obj = st.slider("% Objetivo Real", min_value=1.0, max_value=95.0, value=10.0, step=1.0)
    granulometria = st.selectbox("Granulometría", ["Fino", "Medio", "Grueso"])

with col2:
    forma = st.selectbox("Geometría", ["Mezcla", "Óvalo", "Rectángulo"])
    semillero = st.number_input("Semilla / Muestra", min_value=1, max_value=1000, value=1, step=1)

# Resolución de la máscara (500x500 píxeles)
res = 500
y, x = np.ogrid[-1:1:complex(0, res), -1:1:complex(0, res)]
mascara_circulo = (x**2 + y**2) <= 1.0
area_circulo_px = np.sum(mascara_circulo)

np.random.seed(int(semillero))
imagen_negra = np.zeros((res, res), dtype=bool)

escala = {'Fino': 0.03, 'Medio': 0.07, 'Grueso': 0.14}
r_med = escala[granulometria]

max_intentos = 8000
intentos = 0

# El bucle evalúa los píxeles negros reales en pantalla
while (np.sum(imagen_negra & mascara_circulo) / area_circulo_px * 100) < porcentaje_obj and intentos < max_intentos:
    intentos += 1
    
    r_pos = np.sqrt(np.random.uniform(0, (1.0 - r_med)**2))
    theta = np.random.uniform(0, 2 * np.pi)
    cx, cy = r_pos * np.cos(theta), r_pos * np.sin(theta)

    tipo_actual = forma
    if forma == 'Mezcla':
        tipo_actual = np.random.choice(['Óvalo', 'Rectángulo'])

    w = np.random.uniform(r_med * 0.7, r_med * 1.3)
    h = np.random.uniform(r_med * 0.7, r_med * 1.3)
    angulo = np.random.uniform(0, np.pi)

    # Rotación de coordenadas
    xr = (x - cx) * np.cos(angulo) + (y - cy) * np.sin(angulo)
    yr = -(x - cx) * np.sin(angulo) + (y - cy) * np.cos(angulo)

    if tipo_actual == 'Óvalo':
        figura = ((xr / (w/2))**2 + (yr / (h/2))**2) <= 1.0
    else:
        figura = (np.abs(xr) <= w/2) & (np.abs(yr) <= h/2)

    # Suma lógica (OR): solo añade píxeles nuevos
    imagen_negra |= figura

# Recorte al círculo delimitador
imagen_final = imagen_negra & mascara_circulo
porcentaje_real = (np.sum(imagen_final) / area_circulo_px) * 100

# Renderizado gráfico
fig, ax = plt.subplots(figsize=(6, 6))
canvas = np.ones((res, res, 3))
canvas[imagen_final] = [0, 0, 0]

ax.imshow(canvas)
circulo_borde = plt.Circle((res/2, res/2), res/2 - 1, color='black', fill=False, lw=2)
ax.add_patch(circulo_borde)
plt.axis('off')

st.pyplot(fig)
st.info(f"**Porcentaje real visible en pantalla:** {porcentaje_real:.2f}%")
