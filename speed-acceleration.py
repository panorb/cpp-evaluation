import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

trace_file_name = "D:/OneDrive/Dokumente/Masterarbeit/Traces/PAULMANUSPARKNORM.csv"

mapping_names = {
    "/Channel/!SEGA/vaIbc [u1  1]": "X",
    "/Channel/!SEGA/vaIbc [u1  2]": "Y",
    "/Channel/!SEGA/vaIbc [u1  3]": "Z",
    "/Channel/!SEGA/vaIbc [u1  4]": "A",
    "/Channel/!SEGA/vaIbc [u1  5]": "B",
    "/Channel/!SEGA/vaIbc [u1  6]": "C",
    "/Channel/!SPARP/actLineNumber [u1  1]": "LineNumber",
    "/Channel/!S/actProgNetTime [u1  1]": "ProgTime"
}

trace_dtypes = {
    "Time": np.float64,
    "X": np.float64,
    "Y": np.float64,
    "Z": np.float64,
    "A": np.float64,
    "B": np.float64,
    "C": np.float64,
    "LineNumber": np.int64,
    "ProgTime": np.float64
}

with open(trace_file_name, encoding="iso-8859-1") as trace_file:
    for line_num, line in enumerate(trace_file.readlines(), 1):
        if line == ",\n":
            print(f"Trennzeile ist Zeile {line_num}")
            break

    header_df = pd.read_csv(trace_file_name, encoding="iso-8859-1", sep=',', nrows=line_num - 1)
    headings = ["Time"]

    for index, row in header_df.iterrows():
        headings.append(mapping_names.get(row["name"], row["name"]))

    headings.pop()

    trace_df = pd.read_csv(trace_file_name, index_col=False, encoding="iso-8859-1", sep=',', skiprows=line_num + 1, names=headings, dtype=trace_dtypes)

trace_df = trace_df[trace_df["LineNumber"] > 1]

# Berechne Geschwindigkeiten
trace_df['Vx'] = trace_df['X'].diff() / 0.004  # 4ms pro Tick in Sekunden
trace_df['Vy'] = trace_df['Y'].diff() / 0.004
trace_df['Vz'] = trace_df['Z'].diff() / 0.004
trace_df['Ges'] = np.sqrt(trace_df['Vx']**2 + 
                                     trace_df['Vy']**2 + trace_df['Vz'])
    # trace_df['Vz']**2)

# Berechne Beschleunigungen
trace_df['Ax'] = trace_df['Vx'].diff() / 0.004
trace_df['Ay'] = trace_df['Vy'].diff() / 0.004
trace_df['Az'] = trace_df['Vz'].diff() / 0.004
trace_df['Bes'] = trace_df['Ges'].diff() / 0.004 

# Berechne Ruck (JERK)
trace_df['Jx'] = trace_df['Ax'].diff() / 0.004
trace_df['Jy'] = trace_df['Ay'].diff() / 0.004
trace_df['Jz'] = trace_df['Az'].diff() / 0.004
trace_df['Ruc'] = trace_df['Bes'].diff() / 0.004

# Fülle fehlende Werte (z.B. in der ersten Zeile) mit 0
# trace_df.fillna(0, inplace=True)

# Subplots erstellen
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 15))

# x-Werte plotten
axes[0].plot(trace_df['Time'], trace_df['X'], label='X')
axes[0].set_ylabel('X [m]')
axes[0].legend()

# y-Werte plotten
axes[1].plot(trace_df['Time'], trace_df['Y'], label='Y')
axes[1].set_ylabel('Y [m]')
axes[1].legend()

# z-Werte plotten
axes[2].plot(trace_df['Time'], trace_df['Z'], label='Z')
axes[2].set_ylabel('Z [m]')
axes[2].legend()

# Geschwindigkeit plotten
axes[3].plot(trace_df['Time'], trace_df['Ges'], label='Geschwindigkeit')
axes[3].set_ylabel('Geschwindigkeit [m/s]')
axes[3].legend()


trace_df = trace_df[trace_df['Ges'] > 0]
# Beschleunigung plotten
# axes[4].plot(trace_df['Time'], trace_df['Bes'], label='Beschleunigung')
# axes[4].set_ylabel('Beschleunigung [m/s^2]')
# axes[4].legend()
# 
# # Ruck plotten
# axes[5].plot(trace_df['Time'], trace_df['Ruc'], label='Ruck')
# axes[5].set_ylabel('Ruck [m/s^3]')
# axes[5].legend()

# Allgemeine Einstellungen für alle Subplots
for ax in axes:
    ax.set_xlabel('Zeit [s]')
    ax.grid(True)

# Layout anpassen
plt.tight_layout()

# Plot anzeigen
plt.show()
