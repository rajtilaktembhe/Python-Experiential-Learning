import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import date, timedelta

st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌦️",
    layout="wide"
)

BG = "#0b1220"
PANEL = "#162338"
TEXT = "#e5eef8"
ACCENT = "#22d3ee"

st.markdown(f"""
<style>
.stApp {{
    background: {BG};
    color: {TEXT};
}}
h1, h2, h3 {{
    color: {ACCENT};
}}
[data-testid="stMetric"] {{
    background: {PANEL};
    border: 1px solid #2b3b50;
    padding: 15px;
    border-radius: 12px;
}}
</style>
""", unsafe_allow_html=True)

st.title("🌦️ Weather Data Analysis System")
st.write("Analyze weather data using CSV upload or location-based weather search.")

st.divider()

today = date.today()


def fetch_weather(city, start_date, end_date):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 5,
            "language": "en",
            "format": "json"
        },
        timeout=20
    )

    geo_response.raise_for_status()

    locations = geo_response.json().get("results", [])

    if not locations:
        raise ValueError("Location not found. Enter a valid city.")

    location = locations[0]

    cutoff = today - timedelta(days=92)
    segments = []

    if start_date < cutoff:
        old_end = min(end_date, cutoff - timedelta(days=1))
        segments.append((start_date, old_end, "archive"))

    recent_start = max(start_date, cutoff)

    if recent_start <= end_date:
        segments.append((recent_start, end_date, "forecast"))

    all_data = []

    for seg_start, seg_end, api_type in segments:

        if api_type == "archive":
            weather_url = "https://archive-api.open-meteo.com/v1/archive"
        else:
            weather_url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "start_date": seg_start.isoformat(),
            "end_date": seg_end.isoformat(),
            "daily": [
                "temperature_2m_mean",
                "precipitation_sum",
                "relative_humidity_2m_mean",
                "wind_speed_10m_max"
            ],
            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if "daily" not in result:
            raise ValueError("Weather data is unavailable for these dates.")

        daily = pd.DataFrame({
            "Date": result["daily"]["time"],
            "Temperature": result["daily"]["temperature_2m_mean"],
            "Rainfall": result["daily"]["precipitation_sum"],
            "Humidity": result["daily"]["relative_humidity_2m_mean"],
            "Wind Speed": result["daily"]["wind_speed_10m_max"]
        })

        all_data.append(daily)

    if not all_data:
        raise ValueError("No weather records available.")

    weather_data = pd.concat(all_data, ignore_index=True)

    weather_data["Date"] = pd.to_datetime(
        weather_data["Date"],
        errors="coerce"
    )

    weather_data = weather_data.dropna(subset=["Date"])
    weather_data = weather_data.sort_values("Date")

    return weather_data, location


def analyze_weather(data, location_name):
    data = data.copy()

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    for column in ["Temperature", "Rainfall", "Humidity", "Wind Speed"]:
        if column not in data.columns:
            data[column] = np.nan

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(
        subset=["Date", "Temperature", "Rainfall", "Humidity"]
    )

    data = data[data["Rainfall"] >= 0]
    data = data[data["Humidity"].between(0, 100)]
    data = data.sort_values("Date")

    if data.empty:
        st.warning("No valid weather records found.")
        return

    st.success(f"Weather analysis completed for {location_name}")

    st.subheader("🌤️ Weather Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Temperature",
        f"{data['Temperature'].mean():.1f} °C"
    )

    c2.metric(
        "Total Rainfall",
        f"{data['Rainfall'].sum():.1f} mm"
    )

    c3.metric(
        "Average Humidity",
        f"{data['Humidity'].mean():.1f}%"
    )

    if data["Wind Speed"].notna().any():
        c4.metric(
            "Average Wind Speed",
            f"{data['Wind Speed'].mean():.1f} km/h"
        )
    else:
        c4.metric("Average Wind Speed", "N/A")

    st.divider()

    st.subheader("📋 Weather Records")

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🌡️ Temperature Analysis")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        data["Date"],
        data["Temperature"],
        marker="o",
        label="Temperature"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.xticks(rotation=30)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("🌧️ Rainfall Analysis")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        data["Date"],
        data["Rainfall"]
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Rainfall (mm)")
    ax.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=30)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("💧 Humidity Analysis")

    st.line_chart(
        data.set_index("Date")[["Humidity"]]
    )

    if data["Wind Speed"].notna().any():
        st.subheader("💨 Wind Speed Analysis")

        st.line_chart(
            data.set_index("Date")[["Wind Speed"]]
        )

    st.divider()

    st.subheader("📊 Statistical Report")

    report = data[
        ["Temperature", "Rainfall", "Humidity", "Wind Speed"]
    ].agg(["mean", "min", "max", "std", "sum"])

    st.dataframe(
        report.round(2),
        use_container_width=True
    )

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Weather Data",
        data=csv,
        file_name="weather_analysis_report.csv",
        mime="text/csv"
    )

    report_csv = report.to_csv().encode("utf-8")

    st.download_button(
        "⬇️ Download Statistical Report",
        data=report_csv,
        file_name="weather_statistical_report.csv",
        mime="text/csv"
    )


source = st.radio(
    "Select Data Source",
    ["Search by Location", "Upload CSV"],
    horizontal=True
)

if source == "Search by Location":

    st.subheader("📍 Location-Based Weather Search")

    with st.form("weather_search_form"):

        city = st.text_input(
            "Enter City or Location",
            placeholder="Example: Nagpur, Mumbai, Pune, Delhi"
        )

        mode = st.radio(
            "Select Date Option",
            ["Single Date", "Date Range"],
            horizontal=True
        )

        if mode == "Single Date":

            start_date = st.date_input(
                "Select Weather Date",
                value=today,
                min_value=date(1940, 1, 1),
                max_value=today + timedelta(days=16)
            )

            end_date = start_date

        else:

            selected_dates = st.date_input(
                "Select Start Date and End Date",
                value=(today - timedelta(days=6), today),
                min_value=date(1940, 1, 1),
                max_value=today + timedelta(days=16)
            )

            if len(selected_dates) == 2:
                start_date, end_date = selected_dates
            else:
                start_date = selected_dates[0]
                end_date = selected_dates[0]

        search = st.form_submit_button(
            "🔍 Search Weather",
            type="primary"
        )

    if search:

        st.session_state.pop("weather_data", None)

        if not city.strip():
            st.warning("Please enter a location.")

        elif start_date > end_date:
            st.error("Start date cannot be after end date.")

        else:
            try:
                with st.spinner("Fetching weather information..."):

                    weather_data, location = fetch_weather(
                        city,
                        start_date,
                        end_date
                    )

                st.session_state["weather_data"] = weather_data

                st.session_state["location_name"] = (
                    f"{location['name']}, "
                    f"{location.get('admin1', '')}, "
                    f"{location.get('country', '')}"
                )

                st.session_state["active_source"] = "Search by Location"

            except requests.RequestException as e:
                st.error(f"API connection error: {e}")

            except (ValueError, KeyError, TypeError) as e:
                st.error(f"Error: {e}")

    if (
        "weather_data" in st.session_state
        and st.session_state.get("active_source") == "Search by Location"
    ):
        st.caption(
            f"Location: {st.session_state['location_name']}"
        )

        analyze_weather(
            st.session_state["weather_data"],
            st.session_state["location_name"]
        )

else:

    st.subheader("📂 Upload Weather CSV")

    uploaded_file = st.file_uploader(
        "Upload your weather CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            data = pd.read_csv(uploaded_file)

            required_columns = [
                "Date",
                "Temperature",
                "Rainfall",
                "Humidity"
            ]

            if not all(
                col in data.columns for col in required_columns
            ):
                st.error(
                    "CSV must contain Date, Temperature, Rainfall and Humidity columns."
                )

            else:

                data["Date"] = pd.to_datetime(
                    data["Date"],
                    errors="coerce"
                )

                valid_dates = data["Date"].dropna()

                if valid_dates.empty:
                    st.error("No valid dates found in CSV.")

                else:
                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()

                    st.subheader("📅 Select Date Range")

                    col1, col2 = st.columns(2)

                    with col1:
                        start_date = st.date_input(
                            "Start Date",
                            value=min_date
                        )

                    with col2:
                        end_date = st.date_input(
                            "End Date",
                            value=max_date
                        )

                    if start_date <= end_date:

                        filtered_data = data[
                            (data["Date"].dt.date >= start_date) &
                            (data["Date"].dt.date <= end_date)
                        ]

                        analyze_weather(
                            filtered_data,
                            "Uploaded CSV Data"
                        )

                    else:
                        st.error("Start date cannot be after end date.")

        except Exception as e:
            st.error(f"Unable to read CSV file: {e}")

st.divider()

st.caption(
    "Weather Data Analysis System | Python Project - Phase 3"
)
