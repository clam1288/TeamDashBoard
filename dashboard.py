import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")

st.title("🕒 ApexTurbo Driver Stint Planner")

# ======================
# SECTION 1: GMT to US Time Zone Converter
# ======================
st.header("🕒 GMT to US Time Zone Converter")

gmt_input = st.text_input("Enter race start in GMT (MM/DD/YYYY HH:MM, 24h format)", value="01/01/2025 13:00")

try:
    # Convert MM/DD/YYYY HH:MM to datetime object
    gmt_time = datetime.strptime(gmt_input, "%m/%d/%Y %H:%M")
    gmt_time = pytz.utc.localize(gmt_time)

    timezones = {
        "Eastern (US/Eastern)": gmt_time.astimezone(pytz.timezone("US/Eastern")),
        "Central (US/Central)": gmt_time.astimezone(pytz.timezone("US/Central")),
        "Mountain (US/Mountain)": gmt_time.astimezone(pytz.timezone("US/Mountain")),
        "Pacific (US/Pacific)": gmt_time.astimezone(pytz.timezone("US/Pacific")),
    }

    st.success("📅 Race Start Time in US Time Zones:")
    for zone, t in timezones.items():
        st.write(f"**{zone}** → {t.strftime('%Y-%m-%d %I:%M %p')}")

except ValueError:
    st.error("Please enter the time in the format MM/DD/YYYY HH:MM (24-hour)")

st.markdown("---")

# ======================
# SECTION 2: Driver Stint Planner
# ======================
st.header("📋 24-Hour Driver Schedule")

timezone_options = {
    "EST (UTC-5)": "US/Eastern",
    "CST (UTC-6)": "US/Central",
    "MST (UTC-7)": "US/Mountain",
    "PST (UTC-8)": "US/Pacific",
    "UTC": "UTC"
}

selected_label = st.selectbox("Select Timezone", list(timezone_options.keys()), index=0)
selected_tz = pytz.timezone(timezone_options[selected_label])

# Base start time: 8:00 AM EST on Jan 1, 2025
base_start_est = pytz.timezone("US/Eastern").localize(datetime(2025, 1, 1, 8, 0))
base_start_local = base_start_est.astimezone(selected_tz)

# Build 24-hour time blocks in local timezone
local_times = [(base_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]

# Initialize planner
if "planner" not in st.session_state or st.session_state.get("last_tz") != selected_tz:
    planner = pd.DataFrame({"Time": local_times})
    for d in drivers:
        planner[d] = ["Resting"] * 24
    st.session_state.planner = planner
    st.session_state.last_tz = selected_tz

# Show editable planner
edited = st.data_editor(
    st.session_state.planner,
    use_container_width=True,
    num_rows="dynamic",
    key="planner_editor"
)

# Save planner edits
st.session_state.planner = edited

# Download option
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
