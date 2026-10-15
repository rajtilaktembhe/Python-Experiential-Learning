import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

weather_data = {
    "Date": pd.date_range("2026-01-01", periods=15, freq="D"),
    "Temperature": [24, 25, 23, 26, 27, 28, 26, 25, 29, 30, 31, 29, 27, 26, 28],
    "Rainfall": [2.5, 0, 5.2, 1, 0, 0.5, 3.2, 4.5, 0, 0, 1.5, 3, 6.5, 4.2, 0],
    "Humidity": [65, 62, 70, 60, 58, 55, 63, 68, 52, 50, 48, 55, 72, 69, 57]
}

data = pd.DataFrame(weather_data)
data.to_csv("weather_data.csv", index=False)

data = pd.read_csv("weather_data.csv")
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

for col in ["Temperature", "Rainfall", "Humidity"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()
data = data[
    (data["Rainfall"] >= 0) &
    (data["Humidity"] >= 0) &
    (data["Humidity"] <= 100)
].sort_values("Date")

def show_data(df):
    print("\n--- WEATHER RECORDS ---")
    print(df.to_string(index=False))

def show_statistics(df):
    if df.empty:
        print("No weather records available.")
        return

    print("\n--- STATISTICAL REPORT ---")

    for col, unit in [
        ("Temperature", "°C"),
        ("Rainfall", "mm"),
        ("Humidity", "%")
    ]:
        print(f"\n{col.upper()}")
        print("Average:", round(df[col].mean(), 2), unit)
        print("Minimum:", round(df[col].min(), 2), unit)
        print("Maximum:", round(df[col].max(), 2), unit)
        print("Standard Deviation:", round(df[col].std(), 2), unit)

    print("\nTotal Rainfall:", round(df["Rainfall"].sum(), 2), "mm")

def show_graph(df, choice):
    if df.empty:
        print("No data available to plot.")
        return

    columns = {
        "1": ("Temperature", "Temperature Trend", "Temperature (°C)", "line"),
        "2": ("Rainfall", "Rainfall Pattern", "Rainfall (mm)", "bar"),
        "3": ("Humidity", "Humidity Variation", "Humidity (%)", "line")
    }

    if choice not in columns:
        print("Invalid graph selection.")
        return

    col, title, ylabel, kind = columns[choice]

    plt.figure(figsize=(10, 5))

    if kind == "bar":
        plt.bar(df["Date"].dt.strftime("%d-%m"), df[col])
        plt.xticks(rotation=45)
    else:
        plt.plot(df["Date"], df[col], marker="o")
        plt.xticks(rotation=45)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.4)
    plt.tight_layout()

    filename = {
        "1": "temperature_trend.png",
        "2": "rainfall_pattern.png",
        "3": "humidity_variation.png"
    }[choice]

    plt.savefig(filename)
    print("Graph saved as", filename)
    plt.show()
    plt.close()

def filter_dates(df):
    print("\nEnter dates in YYYY-MM-DD format.")
    print("Press Enter to use the earliest or latest available date.")

    start = input("Start date: ").strip()
    end = input("End date: ").strip()

    try:
        start_date = pd.to_datetime(start) if start else df["Date"].min()
        end_date = pd.to_datetime(end) if end else df["Date"].max()

        if start_date > end_date:
            print("Start date cannot be after end date.")
            return df

        result = df[
            (df["Date"] >= start_date) &
            (df["Date"] <= end_date)
        ]

        if result.empty:
            print("No records found for this date range.")
            return df

        print("Filtered records:", len(result))
        return result

    except (ValueError, TypeError):
        print("Invalid date. Please use YYYY-MM-DD.")
        return df

def export_report(df):
    if df.empty:
        print("No data available to export.")
        return

    report = df[["Temperature", "Rainfall", "Humidity"]].agg(
        ["mean", "min", "max", "std"]
    ).round(2)

    report.to_csv("weather_statistical_report.csv")
    df.to_csv("filtered_weather_data.csv", index=False)

    print("Reports saved successfully:")
    print("weather_statistical_report.csv")
    print("filtered_weather_data.csv")

current_data = data.copy()

while True:
    print("\n" + "=" * 45)
    print("     WEATHER DATA ANALYSIS SYSTEM")
    print("=" * 45)
    print("1. View Weather Data")
    print("2. Statistical Report")
    print("3. Temperature Trend Graph")
    print("4. Rainfall Pattern Graph")
    print("5. Humidity Variation Graph")
    print("6. Filter Data by Date")
    print("7. Export Reports")
    print("8. Reset Date Filter")
    print("9. Exit")

    choice = input("\nEnter your choice (1-9): ").strip()

    if choice == "1":
        show_data(current_data)
    elif choice == "2":
        show_statistics(current_data)
    elif choice in ["3", "4", "5"]:
        show_graph(current_data, str(int(choice) - 2))
    elif choice == "6":
        current_data = filter_dates(current_data)
    elif choice == "7":
        export_report(current_data)
    elif choice == "8":
        current_data = data.copy()
        print("Date filter reset.")
    elif choice == "9":
        print("Weather Data Analysis System closed.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 9.")
