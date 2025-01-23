import pandas as pd
import numpy as np
from pygame.math import Vector2
import datetime

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

def get_path(project):
    trace_df = get_trace_df(project)

    min_x = trace_df["X"].min()
    max_x = trace_df["X"].max()
    min_y = trace_df["Y"].min()
    max_y = trace_df["Y"].max()

    print(f"MIN X={min_x:.2f} Y={min_y:.2f}")
    print(f"MAX X={max_x:.2f} Y={max_y:.2f}")

    width = max_x - min_x
    height = max_y - min_y

    points = []

    for index, row in trace_df.iterrows():
        x_norm = (row["X"] - min_x) / width
        y_norm = (row["Y"] - min_y) / height
        x_norm = min(1.0, max(0.0, x_norm))
        y_norm = min(1.0, max(0.0, y_norm))

        points.append(Vector2(x_norm, y_norm))

    return points

sensor_dtypes = {
    # "Epoch time (ms)": np.float64,
    # "ShutterTime_Ch1 (µs)": np.float64,
    # "Intensity1_Ch1 (%)": np.float64,
    # "Distance1_Ch1 (mm)": np.float64
    # "# Data acquisition time": datetime.datetime
}

def get_trace_df(project):
    with open(project.trace_file.get(), encoding="iso-8859-1") as trace_file:
        for line_num, line in enumerate(trace_file.readlines(), 1):
            if line == ",\n":
                print(f"Trennzeile ist Zeile {line_num}")
                break

    header_df = pd.read_csv(project.trace_file.get(), encoding="iso-8859-1", sep=',', nrows=line_num - 1)
    headings = ["Time"]

    for index, row in header_df.iterrows():
        headings.append(mapping_names.get(row["name"], row["name"]))

    headings.pop()

    trace_df = pd.read_csv(project.trace_file.get(), index_col=False, encoding="iso-8859-1", sep=',', skiprows=line_num + 1, names=headings, dtype=trace_dtypes)
    return trace_df

def get_sensor_df(project):
    sensor_df = pd.read_csv(project.sensor_file.get(), encoding="iso-8859-1", sep=';', skiprows=7, skipinitialspace=True, dtype=sensor_dtypes, parse_dates = ["# Data acquisition time"], date_format="%Y-%M-%D %H:%M:%S,%f", decimal=",")
    sensor_df.loc[sensor_df['Distance1_Ch1 (mm)'] < 0, 'Distance1_Ch1 (mm)'] = np.nan
    return sensor_df


def get_distances(project):
    result = []

    sensor_df = get_sensor_df(project) 

    last_time = None
    for index, row in sensor_df.iterrows():
        cur_time = row["Epoch time (ms)"]

        if last_time:
            if cur_time - last_time >= 4.0:
                distance = cur_time - last_time
                result.append(row["Distance1_Ch1 (mm)"])
                last_time = cur_time
        else:
            last_time = cur_time

    return result
    # print(sensor_df.columns)
    # print(result)

def sync_values(project):
    sensor_df = get_sensor_df(project)
    trace_df = get_trace_df(project)
    
    min_x = trace_df["X"].min()
    max_x = trace_df["X"].max()
    min_y = trace_df["Y"].min()
    max_y = trace_df["Y"].max()

    print(f"MIN X={min_x:.2f} Y={min_y:.2f}")
    print(f"MAX X={max_x:.2f} Y={max_y:.2f}")

    width = max_x - min_x
    height = max_y - min_y

    x_vals = []
    y_vals = [] 

    for index, row in trace_df.iterrows():
        x_norm = (row["X"] - min_x) / width
        y_norm = (row["Y"] - min_y) / height
        x_norm = min(1.0, max(0.0, x_norm))
        y_norm = min(1.0, max(0.0, y_norm))

        x_vals.append(x_norm)
        y_vals.append(y_norm)

    trace_df["X_Norm"] = pd.Series(x_vals)
    trace_df["Y_Norm"] = pd.Series(y_vals)

    trace_df = trace_df[trace_df["LineNumber"] >= 2]

    sensor_df = sensor_df[["Epoch time (ms)", "Distance1_Ch1 (mm)"]]

    filtered_rows = []

    previous_time = sensor_df.iloc[project.begin_index.get()]['Epoch time (ms)']
    filtered_rows.append(sensor_df.iloc[project.begin_index.get()])

    # Loop through the DataFrame and select rows every 4 seconds
    for index, row in sensor_df.iloc[project.begin_index.get()+1:].iterrows():
        current_time = row['Epoch time (ms)']
        if current_time >= previous_time + 4:
            # If the value is NaN, skip forward until a non-NaN is found while staying within the 4-second rule
            if pd.isna(row['Distance1_Ch1 (mm)']):
                # Find the next valid value within the next few rows
                valid_rows = sensor_df[(sensor_df['Epoch time (ms)'] > current_time) & (sensor_df['Epoch time (ms)'] < current_time + 4) & (~sensor_df['Distance1_Ch1 (mm)'].isna())]
                if not valid_rows.empty:
                    row = valid_rows.iloc[0]  # Take the next valid row
            filtered_rows.append(row)
            previous_time = row['Epoch time (ms)']

    filtered_df = pd.DataFrame(filtered_rows)
    trace_df["Distance"] = filtered_df["Distance1_Ch1 (mm)"].iloc[:len(trace_df)].values
    
    return trace_df

   # # Identify the last point where the column changes
   # last_change_index = trace_df[trace_df['ProgTime'] != trace_df['ProgTime'].iloc[-1]].last_valid_index()
   # print(last_change_index)

   # # Keep only rows up to the last change
   # trace_df = trace_df.iloc[:last_change_index + 1] if last_change_index is not None else trace_df.iloc[:0]
   # 
   # print(trace_df)

   # sensor_df["diff"] = sensor_df["Distance1_Ch1 (mm)"].diff()
   # # print(sensor_df.iloc[:,5:])
   # # print(sensor_df["diff"].to_frame()[:5000].to_string())
   # # print(sensor_df[~sensor_df["Distance1_Ch1 (mm)"].isna() and sensor_df["diff"].abs() >= 0.001].iloc[0])
   # sensor_df.to_csv("sensor.csv",na_rep="NaN")
   # trace_df.to_csv("trace.csv",na_rep="NaN")
   # # print(trace_df.to_string())


def check_valid(value):
    try:
        val = float(value)
        return val >= 0
    except ValueError:
        print(f"ValueError value:{value}")
        return False

if __name__ == "__main__":
    import tkinter as tk
    from utils.project import Project
    root = tk.Tk()
    project = Project()
    project.load("./projects/manuell_spark_norm.toml")
    sync_values(project)

