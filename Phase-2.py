import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

weather_data = {
    "Date": [
        "2026-01-01", "2026-01-02", "2026-01-03",
        "2026-01-04", "2026-01-05", "2026-01-06",
        "2026-01-07", "2026-01-08", "2026-01-09",
        "2026-01-10", "2026-01-11", "2026-01-12",
        "2026-01-13", "2026-01-14", "2026-01-15"
    ],
    "Temperature": [
        24, 25, 23, 26, 27, 28, 26, 25,
        29, 30, 31, 29, 27, 26, 28
    ],
    "Rainfall": [
        2.5, 0.0, 5.2, 1.0, 0.0, 0.5, 3.2, 4.5,
        0.0, 0.0, 1.5, 3.0, 6.5, 4.2, 0.0
    ],
    "Humidity": [
        65, 62, 70, 60, 58, 55, 63, 68,
        52, 50, 48, 55, 72, 69, 57
    ]
}

data = pd.DataFrame(weather_data)

data.to_csv("weather_data.csv", index=False)

print("=" * 55)
print("           WEATHER DATA ANALYSIS SYSTEM")
print("=" * 55)

data = pd.read_csv("weather_data.csv")

data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
data["Temperature"] = pd.to_numeric(data["Temperature"], errors="coerce")
data["Rainfall"] = pd.to_numeric(data["Rainfall"], errors="coerce")
data["Humidity"] = pd.to_numeric(data["Humidity"], errors="coerce")

data = data.dropna()

data = data[
    (data["Humidity"] >= 0) &
    (data["Humidity"] <= 100) &
    (data["Rainfall"] >= 0)
]

data = data.sort_values("Date")

print("\nWeather data loaded successfully.")
print("Valid records:", len(data))

avg_temp = data["Temperature"].mean()
min_temp = data["Temperature"].min()
max_temp = data["Temperature"].max()
std_temp = data["Temperature"].std()

avg_rain = data["Rainfall"].mean()
min_rain = data["Rainfall"].min()
max_rain = data["Rainfall"].max()
total_rain = data["Rainfall"].sum()

avg_humidity = data["Humidity"].mean()
min_humidity = data["Humidity"].min()
max_humidity = data["Humidity"].max()
std_humidity = data["Humidity"].std()

print("\n" + "=" * 55)
print("             STATISTICAL REPORT")
print("=" * 55)

print("\nTEMPERATURE ANALYSIS")
print("-" * 35)
print("Average Temperature :", round(avg_temp, 2), "°C")
print("Minimum Temperature :", min_temp, "°C")
print("Maximum Temperature :", max_temp, "°C")
print("Standard Deviation  :", round(std_temp, 2), "°C")

print("\nRAINFALL ANALYSIS")
print("-" * 35)
print("Average Rainfall :", round(avg_rain, 2), "mm")
print("Minimum Rainfall :", min_rain, "mm")
print("Maximum Rainfall :", max_rain, "mm")
print("Total Rainfall   :", round(total_rain, 2), "mm")

print("\nHUMIDITY ANALYSIS")
print("-" * 35)
print("Average Humidity :", round(avg_humidity, 2), "%")
print("Minimum Humidity :", min_humidity, "%")
print("Maximum Humidity :", max_humidity, "%")
print("Standard Deviation :", round(std_humidity, 2), "%")

plt.figure(figsize=(10, 5))
plt.plot(data["Date"], data["Temperature"], marker="o")
plt.title("Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("temperature_trend.png")
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(data["Date"].dt.strftime("%d-%m"), data["Rainfall"])
plt.title("Rainfall Pattern")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("rainfall_pattern.png")
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(data["Date"], data["Humidity"], marker="o")
plt.title("Humidity Variation")
plt.xlabel("Date")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("humidity_variation.png")
plt.show()

summary = pd.DataFrame({
    "Parameter": [
        "Temperature",
        "Rainfall",
        "Humidity"
    ],
    "Average": [
        avg_temp,
        avg_rain,
        avg_humidity
    ],
    "Minimum": [
        min_temp,
        min_rain,
        min_humidity
    ],
    "Maximum": [
        max_temp,
        max_rain,
        max_humidity
    ]
})

summary = summary.round(2)

print("\n" + "=" * 55)
print("              SUMMARY TABLE")
print("=" * 55)

print(summary.to_string(index=False))

summary.to_csv(
    "weather_statistical_report.csv",
    index=False
)

print("\n" + "=" * 55)
print("           PROJECT OUTPUT FILES")
print("=" * 55)

print("weather_data.csv")
print("weather_statistical_report.csv")
print("temperature_trend.png")
print("rainfall_pattern.png")
print("humidity_variation.png")

print("\n" + "=" * 55)
print("       ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 55)
