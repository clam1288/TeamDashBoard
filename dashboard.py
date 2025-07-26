import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")

st.title("🕒 Driver Stint Planner")
st.markdown("Plan your 24-hour race schedule below. Includes real-world time slots adjusted to your timezone.")

# --- Timezone Setup ---
timezone_options = {
    "EST (UTC-5)": "US/Eastern",
    "CST (UTC-6)": "US/Central",
    "MST (UTC-7)": "US/Mountain",
    "PST (UTC-8)": "US/Pacific",
    "UTC": "UTC"
}

selected_label = st.selectbox("Select Timezone", list(timezone_options.keys()), index=0)
selected_tz = pytz.timezone(timezone_options[selected_label])

# Base race start: 8:00 AM EST (Eastern Time)
race_start_est = pytz.timezone("US/Eastern").localize(datetime(2025, 1, 1, 8, 0))
race_start_local = race_start_est.astimezone(selected_tz)

# Generate 24 real-world time slots from local race start
times = [(race_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

# --- Drivers & Roles ---
drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]

# --- Planner Initialization ---
if "planner" not in st.session_state or st.session_state.get("last_tz") != selected_tz:
    planner = pd.DataFrame({"Time": times})
    for d in drivers:
        planner[d] = ["Resting"] * 24
    st.session_state.planner = planner
    st.session_state.last_tz = selected_tz

# --- Data Editor ---
edited = st.data_editor(
    st.session_state.planner,
    use_container_width=True,
    num_rows="dynamic",
    key="planner_editor"
)

# Save to session state
st.session_state.planner = edited

# --- Download Button ---
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
