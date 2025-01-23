import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

trace_file_name = "C:/Users/panor/OneDrive/Dokumente/Masterarbeit/Traces/PAULMANUSPARKNORM.csv"

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

# Berechnungen
trace_df['Geschwindigkeit_X'] = np.diff(trace_df['X']) / np.diff(trace_df['Time'])
trace_df['Geschwindigkeit_Y'] = np.diff(trace_df['Y']) / np.diff(trace_df['Time'])
trace_df['Geschwindigkeit_Z'] = np.diff(trace_df['Z']) / np.diff(trace_df['Time'])

trace_df['Beschleunigung_X'] = np.diff(trace_df['Geschwindigkeit_X']) / np.diff(trace_df['Time'])
trace_df['Beschleunigung_Y'] = np.diff(trace_df['Geschwindigkeit_Y']) / np.diff(trace_df['Time'])
trace_df['Beschleunigung_Z'] = np.diff(trace_df['Geschwindigkeit_Z']) / np.diff(trace_df['Time'])

trace_df['Ruck_X'] = np.diff(trace_df['Beschleunigung_X']) / np.diff(trace_df['Time'])[1:]
trace_df['Ruck_Y'] = np.diff(trace_df['Beschleunigung_Y']) / np.diff(trace_df['Time'])[1:]
trace_df['Ruck_Z'] = np.diff(trace_df['Beschleunigung_Z']) / np.diff(trace_df['Time'])[1:]

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(trace_df['Time'][1:], trace_df['Geschwindigkeit_X'], label='Geschwindigkeit X')
plt.plot(trace_df['Time'][1:], trace_df['Geschwindigkeit_Y'], label='Geschwindigkeit Y')
plt.plot(trace_df['Time'][1:], trace_df['Geschwindigkeit_Z'], label='Geschwindigkeit Z')
plt.xlabel('Zeit')
plt.ylabel('Geschwindigkeit')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(trace_df['Time'][2:], trace_df['Beschleunigung_X'], label='Beschleunigung X')
plt.plot(trace_df['Time'][2:], trace_df['Beschleunigung_Y'], label='Beschleunigung Y')
plt.plot(trace_df['Time'][2:], trace_df['Beschleunigung_Z'], label='Beschleunigung Z')
plt.xlabel('Zeit')
plt.ylabel('Beschleunigung')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(trace_df['Time'][3:], trace_df['Ruck_X'], label='Ruck X')
plt.plot(trace_df['Time'][3:], trace_df['Ruck_Y'], label='Ruck Y')
plt.plot(trace_df['Time'][3:], trace_df['Ruck_Z'], label='Ruck Z')
plt.xlabel('Zeit')
plt.ylabel('Ruck')
plt.legend()

plt.tight_layout()
plt.show()

print(trace_df)
