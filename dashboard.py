import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")
st.title("🕒 ApexTurbo Driver Stint Planner")

# ======================
# SECTION 1: Race Start Setup
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

# Convert to local race start
gmt_dt = datetime.combine(gmt_date, gmt_time)
race_start_utc = pytz.utc.localize(gmt_dt)
race_start_local = race_start_utc.astimezone(selected_tz)
time_blocks = [(race_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

st.markdown("---")

# ======================
# SECTION 2: Rotated Driver Table
# ======================
st.header("📋 Rotated Driver Schedule")

drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]
emoji_map = {
    "Driving": "🟣 Driving",
    "Spotting": "🟢 Spotting",
    "Resting": "🟡 Resting"
}
reverse_map = {v: k for k, v in emoji_map.items()}

# Create empty table with drivers as rows, time blocks as columns
rotated_data = {time_label: [emoji_map["Resting"]] * len(drivers) for time_label in time_blocks}
rotated_df = pd.DataFrame(rotated_data, index=drivers)

# Streamlit data editor
edited = st.data_editor(
    rotated_df,
    column_config={
        col: st.column_config.SelectboxColumn(
            label=col,
            options=list(emoji_map.values()),
            required=True
        ) for col in rotated_df.columns
    },
    use_container_width=True,
    num_rows="fixed",
    key="rotated_editor"
)

# Convert emoji labels back to raw role text
csv_ready_df = edited.copy()
for col in csv_ready_df.columns:
    csv_ready_df[col] = csv_ready_df[col].map(lambda x: reverse_map.get(x, x))

# ======================
# SECTION 3: CSV Export
# ======================
csv = csv_ready_df.to_csv().encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
