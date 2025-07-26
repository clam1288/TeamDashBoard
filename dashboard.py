import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")
st.title("🕒 ApexTurbo Driver Stint Planner")

# ======================
# SECTION 1: Compact Race Setup
# ======================
st.markdown("#### 🗓 Race Start & Timezone")

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

    with col1:
        gmt_date = st.date_input("Date (GMT)", value=datetime(2025, 1, 1).date(), label_visibility="collapsed")
        st.caption("📅 Date")
    with col2:
        gmt_time = st.time_input("Time (GMT)", value=dt_time(13, 0), label_visibility="collapsed")
        st.caption("⏱ Time")
    with col3:
        practice_minutes = st.number_input("Practice", min_value=0, value=30, step=5, label_visibility="collapsed")
        st.caption("🏁 Practice (min)")
    with col4:
        quali_minutes = st.number_input("Quali", min_value=0, value=15, step=5, label_visibility="collapsed")
        st.caption("🚦 Quali (min)")
    with col5:
        grid_minutes = st.number_input("Grid", min_value=0, value=2, step=1, label_visibility="collapsed")
        st.caption("🧍 Grid (min)")

st.markdown("")

# Timezone row
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.caption("🌐 Timezone")
    with col2:
        timezone_options = {
            "EST": "US/Eastern",
            "CST": "US/Central",
            "MST": "US/Mountain",
            "PST": "US/Pacific",
            "UTC": "UTC"
        }
        selected_label = st.selectbox("", list(timezone_options.keys()), index=0, label_visibility="collapsed")
        selected_tz = pytz.timezone(timezone_options[selected_label])

# Compute adjusted race start
total_offset = timedelta(minutes=practice_minutes + quali_minutes + grid_minutes)
gmt_dt = datetime.combine(gmt_date, gmt_time)
race_start_utc = pytz.utc.localize(gmt_dt) + total_offset
race_start_local = race_start_utc.astimezone(selected_tz)
time_blocks = [(race_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

st.markdown(
    f"""🟠 **Race stints start at {race_start_local.strftime('%I:%M %p %Z')}**  
    (Practice: {practice_minutes}m, Quali: {quali_minutes}m, Grid: {grid_minutes}m — Total: {practice_minutes + quali_minutes + grid_minutes}m)
    """
)

st.divider()

# ======================
# SECTION 2: Rotated Driver Schedule Table
# ======================
st.markdown("#### 📋 24-Hour Driver Schedule")

drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]
emoji_map = {
    "Driving": "🟣 Driving",
    "Spotting": "🟢 Spotting",
    "Resting": "🟡 Resting"
}
reverse_map = {v: k for k, v in emoji_map.items()}

rotated_data = {time_label: [emoji_map["Resting"]] * len(drivers) for time_label in time_blocks}
rotated_df = pd.DataFrame(rotated_data, index=drivers)

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

# Clean for export
csv_ready_df = edited.copy()
for col in csv_ready_df.columns:
    csv_ready_df[col] = csv_ready_df[col].map(lambda x: reverse_map.get(x, x))

csv = csv_ready_df.to_csv().encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
