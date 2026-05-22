import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Se cargan los resultados desde un CSV para trabajar con una fuente tabular
# simple y reproducible dentro de la estructura del proyecto.
df = pd.read_csv("datos/resultados.csv")

# Se obtiene la lista única de equipos a partir de locales y visitantes para
# construir una estructura común de estadísticas acumuladas por equipo.
equipos = pd.unique(df[["equipo_local", "equipo_visitante"]].values.ravel())
stats = {e: {"PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "Pts": 0} for e in equipos}

# Se recorre cada partido para actualizar de forma incremental los indicadores
# principales de la tabla: partidos jugados, goles, resultados y puntos.
for _, fila in df.iterrows():
    local = fila["equipo_local"]
    visitante = fila["equipo_visitante"]
    gl = fila["goles_local"]
    gv = fila["goles_visitante"]

    stats[local]["PJ"] += 1
    stats[visitante]["PJ"] += 1
    stats[local]["GF"] += gl
    stats[local]["GC"] += gv
    stats[visitante]["GF"] += gv
    stats[visitante]["GC"] += gl

    # La asignación de puntos sigue la lógica estándar del fútbol:
    # victoria = 3 puntos, empate = 1 punto, derrota = 0 puntos.
    if gl > gv:
        stats[local]["PG"] += 1
        stats[local]["Pts"] += 3
        stats[visitante]["PP"] += 1
    elif gl < gv:
        stats[visitante]["PG"] += 1
        stats[visitante]["Pts"] += 3
        stats[local]["PP"] += 1
    else:
        stats[local]["PE"] += 1
        stats[local]["Pts"] += 1
        stats[visitante]["PE"] += 1
        stats[visitante]["Pts"] += 1

# Se transforma la estructura acumulada en un DataFrame y se ordena por puntos
# para obtener una tabla de posiciones legible y comparable.
tabla = pd.DataFrame(stats).T.sort_values("Pts", ascending=False)

print("=== TABLA DE POSICIONES ===")
print(tabla.to_string())

# El promedio de goles por partido se calcula como métrica general del torneo
# para resumir el nivel de anotación del conjunto de encuentros analizados.
total_goles = df["goles_local"].sum() + df["goles_visitante"].sum()
promedio = total_goles / len(df)
print(f"\nPromedio de goles por partido: {promedio:.2f}")

# Se exporta la tabla final para dejar una evidencia reutilizable del análisis.
tabla.to_csv("resultados/tabla_posiciones.csv")

# El gráfico permite visualizar de forma rápida la diferencia de puntos entre
# equipos y complementar la salida tabular del análisis.
fig, ax = plt.subplots(figsize=(10, 6))
tabla["Pts"].plot(kind="bar", ax=ax, color="steelblue")
ax.set_title("Tabla de Posiciones - Puntos por Equipo")
ax.set_xlabel("Equipo")
ax.set_ylabel("Puntos")
ax.set_xticklabels(tabla.index, rotation=30, ha="right")
plt.tight_layout()
plt.savefig("resultados/grafico_posiciones.png")
plt.show()
print("\n✅ Gráfico guardado en resultados/grafico_posiciones.png")
