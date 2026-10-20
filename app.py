import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.title("Estimador Visual de Porcentajes")

porcentaje = st.slider("% Objetivo", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
granulometria = st.selectbox("Granulometría", ["Fino", "Medio", "Grueso"])
forma = st.selectbox("Geometría", ["Mezcla", "Óvalo", "Rectángulo"])
semillero = st.number_input("Semilla / Muestra", min_value=1, max_value=1000, value=1)

np.random.seed(semillero)
fig, ax = plt.subplots(figsize=(6, 6))
radio_campo = 1.0
area_total = np.pi * (radio_campo**2)
area_objetivo = (porcentaje / 100.0) * area_total

escala = {'Fino': 0.04, 'Medio': 0.08, 'Grueso': 0.15}
r_med = escala[granulometria]

campo = plt.Circle((0, 0), radio_campo, color='white', ec='black', lw=2)
ax.add_patch(campo)

area_acumulada = 0.0
intentos = 0
max_intentos = 3000

while area_acumulada < area_objetivo and intentos < max_intentos:
    intentos += 1
    r_pos = np.sqrt(np.random.uniform(0, (radio_campo - r_med)**2))
    theta = np.random.uniform(0, 2 * np.pi)
    cx, cy = r_pos * np.cos(theta), r_pos * np.sin(theta)

    tipo_actual = forma
    if forma == 'Mezcla':
        tipo_actual = np.random.choice(['Óvalo', 'Rectángulo'])

    w = np.random.uniform(r_med * 0.7, r_med * 1.3)
    h = np.random.uniform(r_med * 0.7, r_med * 1.3)
    angulo = np.random.uniform(0, 360)

    if tipo_actual == 'Óvalo':
        patch = patches.Ellipse((cx, cy), width=w, height=h, angle=angulo, color='black')
        area_patch = np.pi * (w / 2) * (h / 2)
    else:
        patch = patches.Rectangle((cx - w/2, cy - h/2), width=w, height=h, angle=angulo, color='black')
        area_patch = w * h

    ax.add_patch(patch)
    area_acumulada += area_patch

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
plt.axis('off')

porcentaje_real = (area_acumulada / area_total) * 100
st.caption(f"Porcentaje Real Generado: {porcentaje_real:.1f}%")

st.pyplot(fig)
