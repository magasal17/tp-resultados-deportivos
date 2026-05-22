import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("datos/resultados.csv")

equipos = pd.unique(df[["equipo_local", "equipo_visitante"]].values.ravel())
stats = {e: {"PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "Pts": 0} for e in equipos}

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

tabla = pd.DataFrame(stats).T.sort_values("Pts", ascending=False)

print("=== TABLA DE POSICIONES ===")
print(tabla.to_string())

total_goles = df["goles_local"].sum() + df["goles_visitante"].sum()
promedio = total_goles / len(df)
print(f"\nPromedio de goles por partido: {promedio:.2f}")

tabla.to_csv("resultados/tabla_posiciones.csv", index=True)

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
