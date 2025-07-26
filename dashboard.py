import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

st.set_page_config(page_title="ApexTurbo Driver Planner", layout="wide")

# ======================
# Sidebar Navigation (non-multipage safe)
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
# Compact 1-Line Input Bar
# ======================
with st.container():
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.1, 1, 1, 1, 1, 1, 2])
    with c1:
        gmt_date = st.date_input("Date", value=datetime(2025, 1, 1).date(), label_visibility="collapsed")
    with c2:
        gmt_time = st.time_input("Time (GMT)", value=dt_time(13, 0), label_visibility="collapsed")
    with c3:
        practice = st.number_input("Prac", min_value=0, value=30, step=5, label_visibility="collapsed")
    with c4:
        quali = st.number_input("Qual", min_value=0, value=15, step=5, label_visibility="collapsed")
    with c5:
        grid = st.number_input("Grid", min_value=0, value=2, step=1, label_visibility="collapsed")
    with c6:
        tz_choice = st.selectbox(
            "TZ",
            ["EST", "CST", "MST", "PST", "UTC"],
            index=0,
            label_visibility="collapsed"
        )
    with c7:
        st.caption("📅 Start = GMT + Pre-race")

# ======================
# Time Block Calculation
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

st.markdown("---")

# ======================
# Driver Table
# ======================
st.markdown("### 📋 Stint Table")

drivers = st.multiselect("Drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])

roles = ["Drive", "Spot", "Rest"]
emoji_map = {
    "Drive": "🟣 Drive",
    "Spot": "🟢 Spot",
    "Rest": "🟡 Rest"
}
reverse_map = {v: k for k, v in emoji_map.items()}

# Build table
table_data = {t: [emoji_map["Rest"]] * len(drivers) for t in time_blocks}
rotated_df = pd.DataFrame(table_data, index=drivers)

# Editable grid
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
    key="editor"
)

# Clean for export
csv_df = edited.copy()
for col in csv_df.columns:
    csv_df[col] = csv_df[col].map(lambda x: reverse_map.get(x, x))

csv = csv_df.to_csv().encode("utf-8")
st.download_button("📥 Download CSV", csv, "driver_stint_plan.csv", "text/csv")
`
