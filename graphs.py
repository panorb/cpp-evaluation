import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.signal import detrend

sensor_file = "C:/Users/panor/AppData/Local/Micro-Epsilon/SensorTool/Protocols/protocol_confocalDT-IFC2422_2024-12-09_15-32-19.706_ManuellSparkNorm.csv"
sensor_file = "C:/Users/panor/AppData/Local/Micro-Epsilon/SensorTool/Protocols/snapshot_confocalDT-IFC2422_2024-12-09_13-44-17.474_NormSparkErosion.csv"

sensor_df = pd.read_csv(sensor_file, encoding="iso-8859-1", sep=';', skiprows=7, skipinitialspace=True, parse_dates = ["# Data acquisition time"], date_format="%Y-%M-%D %H:%M:%S,%f", decimal=",")


print(sensor_df.dtypes)

sensor_df.loc[sensor_df['Distance1_Ch1 (mm)'] < 0, 'Distance1_Ch1 (mm)'] = np.nan
# print(sensor_df)

# new_values = []

# for i, row in sensor_df.iterrows():
#     value = row["Distance1_Ch1 (mm)"]
# 
#     rand_n = random.randint(0, 10)
#     if rand_n <= 3:
#         value += random.uniform(0.000, 0.002)
#     elif rand_n <= 4:
#         value -= random.uniform(0.000, 0.001)
# 
#     if random.randint(0, 40) == 0:
#         value += random.uniform(-0.002, 0.002)
# 
#     new_values.append(value)
# 
# sensor_df["Distance1_Ch1 (mm) c"] = pd.Series(new_values)
# sensor_df["Distance1_Ch1 (mm) c"] = sensor_df["Distance1_Ch1 (mm) c"].round(3)
sensor_df[:34400].plot(y="Distance1_Ch1 (mm)", style="-")
sensor_df = sensor_df.dropna()
sensor_df['detrended_height'] = detrend(sensor_df['Distance1_Ch1 (mm)'])
#sensor_df[:34400].plot(y="detrended_height", style="-")

# Define the count for grouping
count = 60  # Number of measurements per segment
Ra_values = []

# Segment the data using the count variable
for start in range(0, len(sensor_df), count):
    segment = sensor_df.iloc[start:start + count]
    if not segment.empty:
        mean_height = segment['detrended_height'].mean()
        Ra = np.mean(np.abs(segment['detrended_height'] - mean_height))
        Ra_values.append(Ra * 1000)

# pd.Series(Ra_values).plot(style='-')
plt.show()
print(Ra_values)
# sensor_df[['Distance1_Ch1 (mm) c']][1400:34300][::3].to_csv("manuell-spark-norm2.dat", sep=" ", header=["distance"],index_label="idx", na_rep="NaN")


# plt.show()

