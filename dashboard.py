import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")
st.title("🕒 ApexTurbo Driver Stint Planner")

# ======================
# SECTION 1: Race Time Input
# ======================
st.header("🗓 Race Start Setup")

col1, col2, col3 = st.columns(3)

with col1:
    gmt_date = st.date_input("Race Start Date (GMT)", value=datetime(2025, 1, 1).date())
with col2:
    gmt_time = st.time_input("Race Start Time (GMT)", value=dt_time(13, 0))
with col3:
    timezone_options = {
        "EST (UTC-5)": "US/Eastern",
        "CST (UTC-6)": "US/Central",
        "MST (UTC-7)": "US/Mountain",
        "PST (UTC-8)": "US/Pacific",
        "UTC": "UTC"
    }
    selected_label = st.selectbox("Display Timezone", list(timezone_options.keys()), index=0)
    selected_tz = pytz.timezone(timezone_options[selected_label])

# Calculate time slots
gmt_dt = datetime.combine(gmt_date, gmt_time)
race_start_utc = pytz.utc.localize(gmt_dt)
race_start_local = race_start_utc.astimezone(selected_tz)
local_times = [(race_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

st.markdown("---")

# ======================
# SECTION 2: Driver Planner
# ======================
st.header("📋 24-Hour Driver Schedule")

drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]

# Initialize DataFrame with emoji labels
emoji_map = {
    "Driving": "🟣 Driving",
    "Spotting": "🟢 Spotting",
    "Resting": "🟡 Resting"
}
reverse_map = {v: k for k, v in emoji_map.items()}

# Create starting planner with emoji role labels
planner_data = {"Time": local_times}
for d in drivers:
    planner_data[d] = [emoji_map["Resting"]] * 24
planner = pd.DataFrame(planner_data)

# Editor with emojis (color-coded in text)
edited = st.data_editor(
    planner,
    column_config={
        d: st.column_config.SelectboxColumn(
            label=d,
            options=list(emoji_map.values()),
            required=True
        ) for d in drivers
    },
    use_container_width=True,
    num_rows="dynamic",
    key="planner_editor"
)

# Reverse map for export
cleaned_df = edited.copy()
for d in drivers:
    cleaned_df[d] = cleaned_df[d].map(lambda x: reverse_map.get(x, x))

# ======================
# SECTION 3: CSV Download
# ======================
csv = cleaned_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
