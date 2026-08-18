import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

csv_data = """Date,Temperature,Rainfall,Humidity
2026-01-01,24,2.5,65
2026-01-02,25,0.0,62
2026-01-03,23,5.2,70
2026-01-04,26,1.0,60
2026-01-05,27,0.0,58
2026-01-06,28,0.5,55
2026-01-07,26,3.2,63
2026-01-08,25,4.5,68
2026-01-09,29,0.0,52
2026-01-10,30,0.0,50
2026-01-11,31,1.5,48
2026-01-12,29,3.0,55
2026-01-13,27,6.5,72
2026-01-14,26,4.2,69
2026-01-15,28,0.0,57
"""
data = pd.read_csv(StringIO(csv_data))
data["Date"] = pd.to_datetime(data["Date"])
data = data.dropna()

print("=" * 45)
print("       WEATHER DATA ANALYSIS SYSTEM")
print("=" * 45)

print("\n--- TEMPERATURE ANALYSIS ---")

average_temp = data["Temperature"].mean()
minimum_temp = data["Temperature"].min()
maximum_temp = data["Temperature"].max()
std_temp = data["Temperature"].std()

print("Average Temperature :", round(average_temp, 2), "°C")
print("Minimum Temperature :", minimum_temp, "°C")
print("Maximum Temperature :", maximum_temp, "°C")
print("Standard Deviation  :", round(std_temp, 2), "°C")

print("\n--- RAINFALL ANALYSIS ---")

average_rain = data["Rainfall"].mean()
minimum_rain = data["Rainfall"].min()
maximum_rain = data["Rainfall"].max()
total_rain = data["Rainfall"].sum()

print("Average Rainfall :", round(average_rain, 2), "mm")
print("Minimum Rainfall :", minimum_rain, "mm")
print("Maximum Rainfall :", maximum_rain, "mm")
print("Total Rainfall   :", round(total_rain, 2), "mm")

print("\n--- HUMIDITY ANALYSIS ---")

average_humidity = data["Humidity"].mean()
minimum_humidity = data["Humidity"].min()
maximum_humidity = data["Humidity"].max()
std_humidity = data["Humidity"].std()

print("Average Humidity :", round(average_humidity, 2), "%")
print("Minimum Humidity :", minimum_humidity, "%")
print("Maximum Humidity :", maximum_humidity, "%")
print("Standard Deviation :", round(std_humidity, 2), "%")

plt.figure(figsize=(10, 5))

plt.plot(
    data["Date"],
    data["Temperature"],
    marker="o"
)

plt.title("Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

plt.bar(
    data["Date"].dt.strftime("%d-%m"),
    data["Rainfall"]
)

plt.title("Rainfall Pattern")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

plt.plot(
    data["Date"],
    data["Humidity"],
    marker="o"
)

plt.title("Humidity Variation")
plt.xlabel("Date")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()

print("\n" + "=" * 45)
print("          STATISTICAL SUMMARY")
print("=" * 45)

summary = pd.DataFrame({
    "Parameter": [
        "Temperature",
        "Rainfall",
        "Humidity"
    ],
    "Average": [
        average_temp,
        average_rain,
        average_humidity
    ],
    "Minimum": [
        minimum_temp,
        minimum_rain,
        minimum_humidity
    ],
    "Maximum": [
        maximum_temp,
        maximum_rain,
        maximum_humidity
    ]
})

print(summary.round(2).to_string(index=False))

print("\n" + "=" * 45)
print("       ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 45)
