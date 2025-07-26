# dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="Driver Stint Planner", layout="wide")

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
        st.caption("🢍 Grid Time (min)")
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
            yes = st.form_submit_button("Yes")
        with confirm_col2:
            no = st.form_submit_button("No")

    if yes:
        st.session_state.auto_mode = True
        st.session_state.pending_auto = False
    elif no:
        st.session_state.auto_mode = False
        st.session_state.pending_auto = False
    st.stop()

# ======================
# Apply Automated Mode
# ======================
if st.session_state.auto_mode:
    st.markdown("#### ⚙️ Auto-generate Stint Schedule")
    starting_role = st.selectbox("Select Starting Role for Driver 1", options=roles, index=0)

    pattern_1 = ["Drive", "Spot", "Rest", "Rest", "Spot", "Drive", "Drive", "Spot"]
    pattern_2 = ["Spot", "Drive", "Drive", "Spot", "Rest", "Rest", "Spot", "Drive", "Drive", "Spot"]
    pattern_3 = ["Rest", "Rest", "Spot", "Drive", "Drive", "Spot", "Rest", "Rest"]

    patterns = [pattern_1, pattern_2, pattern_3]

    auto_df = st.session_state.stint_df.copy()
    for i, driver in enumerate(drivers):
        pat = patterns[i % len(patterns)]
        for t in range(24):
            role = pat[t % len(pat)]
            auto_df.loc[driver, time_blocks[t]] = emoji_map[role]
    st.session_state.stint_df = auto_df

# ======================
# Table Display
# ======================
df = st.session_state.stint_df
first_half_cols = time_blocks[:12]
second_half_cols = time_blocks[12:]

st.markdown("#### ⏱ Hours 0–11")
first_half = st.data_editor(
    df[first_half_cols],
    column_config={col: st.column_config.SelectboxColumn(label=col, options=list(emoji_map.values()), required=True) for col in first_half_cols},
    use_container_width=True,
    num_rows="fixed",
    key="first_half"
)

st.markdown("#### ⏱ Hours 12–23")
second_half = st.data_editor(
    df[second_half_cols],
    column_config={col: st.column_config.SelectboxColumn(label=col, options=list(emoji_map.values()), required=True) for col in second_half_cols},
    use_container_width=True,
    num_rows="fixed",
    key="second_half"
)

# ======================
# Export to CSV
# ======================
merged_df = pd.concat([first_half, second_half], axis=1)
csv_df = merged_df.copy()
for col in csv_df.columns:
    csv_df[col] = csv_df[col].map(lambda x: reverse_map.get(x, x))

csv = csv_df.to_csv().encode("utf-8")
st.download_button("📥 Download CSV", csv, "driver_stint_plan.csv", "text/csv")
