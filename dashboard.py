import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="ApexTurbo Driver Planner", layout="wide")

# ======================
# Sidebar Navigation
# ======================
with st.sidebar:
    st.title("🏁 ApexTurbo")
    st.markdown("### Navigation")
    st.markdown("- 🕒 Driver Stint Planner")
    st.markdown("- ⛽ Fuel Strategy (Coming Soon)")
    st.markdown("- 🗒 Track Notes (Coming Soon)")
    st.divider()
    st.caption("We don’t hotlap. We finish together.")

# ======================
# Title
# ======================
st.markdown("## 🕒 Driver Stint Planner")

# ======================
# Input Section
# ======================
with st.container():
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.1, 1, 1, 1, 1, 1, 2])

    with c1:
        st.caption("📅 GMT Start Date")
        gmt_date = st.date_input("Race Date", value=datetime(2025, 6, 11).date(), label_visibility="collapsed")
    with c2:
        st.caption("⏱ GMT Start Time")
        gmt_time = st.time_input("Race Time", value=dt_time(12, 0), label_visibility="collapsed")
    with c3:
        st.caption("🏁 Practice (min)")
        practice = st.number_input("Practice", min_value=0, value=30, step=5, label_visibility="collapsed")
    with c4:
        st.caption("🚦 Quali (min)")
        quali = st.number_input("Quali", min_value=0, value=15, step=5, label_visibility="collapsed")
    with c5:
        st.caption("🧍 Grid Time (min)")
        grid = st.number_input("Grid", min_value=0, value=2, step=1, label_visibility="collapsed")
    with c6:
        st.caption("🌐 Timezone")
        tz_choice = st.selectbox("Timezone", ["EST", "CST", "MST", "PST", "UTC"], index=0, label_visibility="collapsed")
    with c7:
        st.caption("🧮 Start = GMT + Pre-race")

# ======================
# Time Calculations
# ======================
tz_map = {
    "EST": "US/Eastern",
    "CST": "US/Central",
    "MST": "US/Mountain",
    "PST": "US/Pacific",
    "UTC": "UTC"
}
selected_tz = pytz.timezone(tz_map[tz_choice])
gmt_dt = datetime.combine(gmt_date, gmt_time)
race_start_utc = pytz.utc.localize(gmt_dt) + timedelta(minutes=practice + quali + grid)
race_start_local = race_start_utc.astimezone(selected_tz)
time_blocks = [(race_start_local + timedelta(hours=i)).strftime("%-I:%M%p") for i in range(24)]

# ======================
# Driver Roles
# ======================
st.markdown("---")
st.markdown("### 📋 Stint Table")
drivers = st.multiselect("Drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])

roles = ["Drive", "Spot", "Rest"]
emoji_map = {
    "Drive": "🟣 Drive",
    "Spot": "🟢 Spot",
    "Rest": "🟡 Rest"
}
reverse_map = {v: k for k, v in emoji_map.items()}

# ======================
# Automated Mode Toggle
# ======================
auto_mode = st.toggle("🔁 Enable Automated Mode")

# ======================
# Initialize Table
# ======================
full_data = {t: [emoji_map["Rest"]] * len(drivers) for t in time_blocks}
df = pd.DataFrame(full_data, index=drivers)

if auto_mode:
    st.markdown("#### ⚙️ Auto-fill Starting Role for Driver 1")
    starting_role = st.selectbox("Select Starting Role", options=roles, index=0)

    # Define the rotation pattern starting from selected role
    role_cycle = {
        "Drive": ["Drive", "Spot", "Rest", "Rest", "Spot", "Drive", "Drive", "Spot"],
        "Spot": ["Spot", "Rest", "Rest", "Spot", "Drive", "Drive", "Spot", "Drive"],
        "Rest": ["Rest", "Rest", "Spot", "Drive", "Drive", "Spot", "Rest", "Rest"]
    }

    base_pattern = role_cycle[starting_role]

    # Fill for each driver with their offset
    for i, driver in enumerate(drivers):
        pattern = base_pattern[i:] + base_pattern[:i]
        for t in range(24):
            role = pattern[t % len(pattern)]
            df.iloc[i, t] = emoji_map[role]

# ======================
# Split Table and Show
# ======================
first_half_cols = time_blocks[:12]
second_half_cols = time_blocks[12:]

st.markdown("#### ⏱ Hours 0–11")
first_half = st.data_editor(
    df[first_half_cols],
    column_config={
        col: st.column_config.SelectboxColumn(label=col, options=list(emoji_map.values()), required=True)
        for col in first_half_cols
    },
    use_container_width=True,
    num_rows="fixed",
    key="first_half"
)

st.markdown("#### ⏱ Hours 12–23")
second_half = st.data_editor(
    df[second_half_cols],
    column_config={
        col: st.column_config.SelectboxColumn(label=col, options=list(emoji_map.values()), required=True)
        for col in second_half_cols
    },
    use_container_width=True,
    num_rows="fixed",
    key="second_half"
)

# ======================
# Export CSV
# ======================
merged_df = pd.concat([first_half, second_half], axis=1)
csv_df = merged_df.copy()
for col in csv_df.columns:
    csv_df[col] = csv_df[col].map(lambda x: reverse_map.get(x, x))

csv = csv_df.to_csv().encode("utf-8")
st.download_button("📥 Download CSV", csv, "driver_stint_plan.csv", "text/csv")
