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
# Compact Inputs
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

roles = ["Drive", "Spot", "Rest"]
emoji_map = {
    "Drive": "🟣 Drive",
    "Spot": "🟢 Spot",
    "Rest": "🟡 Rest"
}
reverse_map = {v: k for k, v in emoji_map.items()}

drivers = st.multiselect("Drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])

# ======================
# State Init
# ======================
if "stint_df" not in st.session_state:
    data = {t: [emoji_map["Rest"]] * len(drivers) for t in time_blocks}
    st.session_state.stint_df = pd.DataFrame(data, index=drivers)

if "auto_mode" not in st.session_state:
    st.session_state.auto_mode = False

if "pending_auto" not in st.session_state:
    st.session_state.pending_auto = False

# ======================
# Toggle With Confirmation
# ======================
toggle = st.checkbox("🔁 Enable Automated Mode", value=st.session_state.auto_mode)

if toggle and not st.session_state.auto_mode and not st.session_state.pending_auto:
    st.session_state.pending_auto = True
    st.stop()

if st.session_state.pending_auto:
    st.warning("⚠️ This will erase any changes made in manual mode.")

    with st.form("confirm_auto_mode"):
        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
