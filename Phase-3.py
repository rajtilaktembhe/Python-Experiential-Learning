import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌦️",
    layout="wide"
)

# Dark theme
st.markdown("""
<style>
.stApp {
    background: #0b1220;
    color: #e5eef8;
}
h1, h2, h3 {
    color: #22d3ee;
}
[data-testid="stMetric"] {
    background: #162338;
    border: 1px solid #2b3b50;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌦️ Weather Data Analysis System")
st.write("Search weather by selecting location and date.")

st.divider()

# Location input
city = st.text_input(
    "🔍 Enter City Name",
    placeholder="Example: Nagpur, Mumbai, Pune"
)

# Date selection
selected_date = st.date_input(
    "📅 Select Weather Date",
    value=date.today(),
    min_value=date(1940, 1, 1),
    max_value=date.today() + timedelta(days=16)
)

# Search button
if st.button("Search Weather", type="primary"):

    if not city.strip():
        st.warning("Please enter a location.")

    else:
        try:
            # Step 1: Search location
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"

            geo_params = {
                "name": city,
                "count": 10,
                "language": "en",
                "format": "json"
            }

            geo_response = requests.get(
                geo_url,
                params=geo_params,
                timeout=15
            )
            geo_response.raise_for_status()

            locations = geo_response.json().get("results", [])

            if not locations:
                st.error("Location not found.")
                st.stop()

            # Step 2: Select location
            location_options = {
                f"{loc['name']}, {loc.get('admin1', '')}, "
                f"{loc.get('country', '')}": loc
                for loc in locations
            }

            selected_location = st.selectbox(
                "📍 Select Exact Location",
                list(location_options.keys())
            )

            location = location_options[selected_location]

            # Step 3: Select API according to date
            if selected_date < date.today():
                weather_url = (
                    "https://archive-api.open-meteo.com/v1/archive"
                )
                source = "Historical Weather Data"

            elif selected_date == date.today():
                weather_url = (
                    "https://api.open-meteo.com/v1/forecast"
                )
                source = "Current Weather Data"

            else:
                weather_url = (
                    "https://api.open-meteo.com/v1/forecast"
                )
                source = "Weather Forecast"

            weather_params = {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "start_date": selected_date.isoformat(),
                "end_date": selected_date.isoformat(),
                "daily": [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "wind_speed_10m_max"
                ],
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "wind_speed_10m"
                ],
                "timezone": "auto"
            }

            response = requests.get(
                weather_url,
                params=weather_params,
                timeout=20
            )
            response.raise_for_status()

            weather = response.json()

            # Step 4: Display information
            st.success(f"Weather found: {selected_location}")
            st.subheader("🌤️ Weather Details")

            st.caption(
                f"Selected Date: {selected_date} | "
                f"Data Type: {source}"
            )

            daily = weather["daily"]
            hourly = weather["hourly"]

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Maximum Temperature",
                f"{daily['temperature_2m_max'][0]} °C"
            )

            c2.metric(
                "Minimum Temperature",
                f"{daily['temperature_2m_min'][0]} °C"
            )

            c3.metric(
                "Total Rainfall",
                f"{daily['precipitation_sum'][0]} mm"
            )

            c4.metric(
                "Maximum Wind Speed",
                f"{daily['wind_speed_10m_max'][0]} km/h"
            )

            # Step 5: Hourly data
            st.divider()
            st.subheader("⏰ Hourly Weather Report")

            hourly_df = pd.DataFrame({
                "Time": hourly["time"],
                "Temperature (°C)": hourly["temperature_2m"],
                "Humidity (%)": hourly["relative_humidity_2m"],
                "Rainfall (mm)": hourly["precipitation"],
                "Wind Speed (km/h)": hourly["wind_speed_10m"]
            })

            st.dataframe(
                hourly_df,
                use_container_width=True,
                hide_index=True
            )

            # Step 6: Temperature graph
            st.subheader("📊 Hourly Temperature Analysis")

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.plot(
                hourly_df["Time"],
                hourly_df["Temperature (°C)"],
                marker="o",
                color="#22d3ee"
            )

            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            ax.set_title("Temperature Variation")
            ax.grid(alpha=0.3)

            plt.xticks(rotation=45)
            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            # Step 7: Download report
            csv = hourly_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Weather Report",
                data=csv,
                file_name="weather_report.csv",
                mime="text/csv"
            )

            st.success("Weather analysis completed successfully.")

        except requests.RequestException as e:
            st.error(f"API connection error: {e}")

        except (KeyError, IndexError, ValueError) as e:
            st.error(f"Weather data processing error: {e}")

st.divider()
st.caption("Weather Data Analysis System | Python + Streamlit")
