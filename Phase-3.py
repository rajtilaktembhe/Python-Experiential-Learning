import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌦️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f1f7fa;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border-left: 4px solid #0891b2;
}
h1, h2, h3 {
    color: #164e63;
}
</style>
""", unsafe_allow_html=True)

st.title("🌦️ Weather Data Analysis System")
st.write("Interactive climate dashboard for historical weather data.")

sample = pd.DataFrame({
    "Date": pd.date_range("2026-01-01", periods=15),
    "Temperature": [24,25,23,26,27,28,26,25,29,30,31,29,27,26,28],
    "Rainfall": [2.5,0,5.2,1,0,0.5,3.2,4.5,0,0,1.5,3,6.5,4.2,0],
    "Humidity": [65,62,70,60,58,55,63,68,52,50,48,55,72,69,57]
})

uploaded = st.sidebar.file_uploader("Upload weather CSV", type=["csv"])

if uploaded:
    try:
        data = pd.read_csv(uploaded)
        data.columns = data.columns.str.strip()
        required = ["Date", "Temperature", "Rainfall", "Humidity"]

        if not all(c in data.columns for c in required):
            st.error("CSV must contain Date, Temperature, Rainfall and Humidity columns.")
            st.stop()

        data = data[required].copy()
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()
else:
    data = sample.copy()
    st.sidebar.info("Showing sample weather data.")

data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

for col in ["Temperature", "Rainfall", "Humidity"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()
data = data[
    (data["Rainfall"] >= 0) &
    (data["Humidity"].between(0, 100))
].sort_values("Date")

if data.empty:
    st.warning("No valid weather records available.")
    st.stop()

st.sidebar.subheader("Filter Data")

min_date = data["Date"].min().date()
max_date = data["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

parameter = st.sidebar.selectbox(
    "Choose chart parameter",
    ["Temperature", "Rainfall", "Humidity"]
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = data[
        data["Date"].dt.date.between(start_date, end_date)
    ]
else:
    filtered = data.copy()

if filtered.empty:
    st.warning("No records found for the selected date range.")
    st.stop()

st.caption(f"Records analyzed: {len(filtered)}")

temperature = filtered["Temperature"]
rainfall = filtered["Rainfall"]
humidity = filtered["Humidity"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Temperature", f"{temperature.mean():.2f} °C")
c2.metric("Total Rainfall", f"{rainfall.sum():.2f} mm")
c3.metric("Average Humidity", f"{humidity.mean():.2f}%")
c4.metric("Weather Records", len(filtered))

st.divider()
st.header("📊 Interactive Weather Charts")

left, right = st.columns(2)

with left:
    st.subheader(f"{parameter} Analysis")
    fig, ax = plt.subplots(figsize=(8, 4))

    if parameter == "Rainfall":
        ax.bar(filtered["Date"], filtered["Rainfall"], color="#0284c7")
        ax.set_ylabel("Rainfall (mm)")
    elif parameter == "Temperature":
        ax.plot(
            filtered["Date"], filtered["Temperature"],
            marker="o", color="#e76f51"
        )
        ax.set_ylabel("Temperature (°C)")
    else:
        ax.plot(
            filtered["Date"], filtered["Humidity"],
            marker="o", color="#7c3aed"
        )
        ax.set_ylabel("Humidity (%)")

    ax.set_xlabel("Date")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Rainfall Pattern")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(filtered["Date"], rainfall, color="#38bdf8")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_xlabel("Date")
    ax.grid(axis="y", alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

left, right = st.columns(2)

with left:
    st.subheader("Humidity Variation")
    st.line_chart(
        filtered.set_index("Date")[["Humidity"]],
        x_label="Date",
        y_label="Humidity (%)"
    )

with right:
    st.subheader("Temperature Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(temperature, bins=7, color="#fb923c", edgecolor="white")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Number of Days")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.header("📋 Statistical Report")

def statistics(series):
    return {
        "Average": series.mean(),
        "Minimum": series.min(),
        "Maximum": series.max(),
        "Standard Deviation": series.std(),
        "Total": series.sum()
    }

report = pd.DataFrame({
    "Temperature (°C)": statistics(temperature),
    "Rainfall (mm)": statistics(rainfall),
    "Humidity (%)": statistics(humidity)
}).round(2)

st.dataframe(report, use_container_width=True)

st.subheader("Historical Weather Records")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Weather Data",
    data=csv_data,
    file_name="weather_data.csv",
    mime="text/csv"
)

report_csv = report.to_csv().encode("utf-8")
st.download_button(
    "⬇️ Download Statistical Report",
    data=report_csv,
    file_name="weather_statistical_report.csv",
    mime="text/csv"
)

st.success("Weather analysis completed successfully.")

st.markdown("---")
st.caption("Weather Data Analysis System | Python Project — Phase 3")

