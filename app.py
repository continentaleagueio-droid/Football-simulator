import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Simulador de Fútbol", layout="centered")

st.title("⚽ Simulador de Partidos de Fútbol")

st.markdown("Crea equipos personalizados y simula partidos o ligas completas.")

# -------------------------
# CREACIÓN DE EQUIPOS
# -------------------------
st.header("Crear equipos")

num_equipos = st.slider("Número de equipos", 2, 10, 4)

equipos = []

for i in range(num_equipos):
    st.subheader(f"Equipo {i+1}")
    nombre = st.text_input(f"Nombre equipo {i+1}", f"Equipo {i+1}", key=f"nombre_{i}")
    ataque = st.slider(f"Ataque {i+1}", 50, 100, 70, key=f"ataque_{i}")
    defensa = st.slider(f"Defensa {i+1}", 50, 100, 70, key=f"defensa_{i}")
    
    equipos.append({
        "nombre": nombre,
        "ataque": ataque,
        "defensa": defensa,
        "puntos": 0,
        "goles_favor": 0,
        "goles_contra": 0
    })

# -------------------------
# FUNCIÓN DE PARTIDO
# -------------------------
def simular_partido(eq1, eq2):
    factor1 = eq1["ataque"] - eq2["defensa"]
    factor2 = eq2["ataque"] - eq1["defensa"]
    
    goles1 = max(0, int(random.gauss(1.5 + factor1/50, 1)))
    goles2 = max(0, int(random.gauss(1.5 + factor2/50, 1)))
    
    return goles1, goles2

# -------------------------
# SIMULAR PARTIDO INDIVIDUAL
# -------------------------
st.header("Simular partido")

equipo1 = st.selectbox("Equipo 1", equipos, format_func=lambda x: x["nombre"])
equipo2 = st.selectbox("Equipo 2", equipos, format_func=lambda x: x["nombre"], index=1)

if st.button("Jugar partido"):
    g1, g2 = simular_partido(equipo1, equipo2)
    
    st.subheader("Resultado")
    st.write(f"**{equipo1['nombre']} {g1} - {g2} {equipo2['nombre']}**")

# -------------------------
# SIMULAR LIGA COMPLETA
# -------------------------
st.header("Simular liga completa")

if st.button("Simular liga"):
    
    # Reset stats
    for eq in equipos:
        eq["puntos"] = 0
        eq["goles_favor"] = 0
        eq["goles_contra"] = 0
    
    resultados = []
    
    for i in range(len(equipos)):
        for j in range(i+1, len(equipos)):
            eq1 = equipos[i]
            eq2 = equipos[j]
            
            g1, g2 = simular_partido(eq1, eq2)
            
            eq1["goles_favor"] += g1
            eq1["goles_contra"] += g2
            
            eq2["goles_favor"] += g2
            eq2["goles_contra"] += g1
            
            if g1 > g2:
                eq1["puntos"] += 3
            elif g2 > g1:
                eq2["puntos"] += 3
            else:
                eq1["puntos"] += 1
                eq2["puntos"] += 1
            
            resultados.append(f"{eq1['nombre']} {g1} - {g2} {eq2['nombre']}")
    
    st.subheader("Resultados")
    for r in resultados:
        st.write(r)
    
    # Tabla
    tabla = pd.DataFrame(equipos)
    tabla["diferencia"] = tabla["goles_favor"] - tabla["goles_contra"]
    
    tabla = tabla.sort_values(by=["puntos", "diferencia", "goles_favor"], ascending=False)
    
    st.subheader("Clasificación")
    st.dataframe(tabla[["nombre", "puntos", "goles_favor", "goles_contra", "diferencia"]])
