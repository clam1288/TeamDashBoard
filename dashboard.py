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

timezone_options = {
    "EST (UTC-5)": "US/Eastern",
    "CST (UTC-6)": "US/Central",
    "MST (UTC-7)": "US/Mountain",
    "PST (UTC-8)": "US/Pacific",
    "UTC": "UTC"
}

selected_label = st.selectbox("Select Target Timezone for Schedule", list(timezone_options.keys()), index=0)
selected_tz = pytz.timezone(timezone_options[selected_label])

try:
    gmt_time = datetime.strptime(gmt_input, "%m/%d/%Y %H:%M")
    gmt_time = pytz.utc.localize(gmt_time)
    race_start_local = gmt_time.astimezone(selected_tz)

    st.success("📅 Converted Start Time:")
    st.write(f"**{selected_label}** → {race_start_local.strftime('%Y-%m-%d %I:%M %p')}")

    local_times = [(race_start_local + timedelta(hours=i)).strftime("%I:%M %p") for i in range(24)]

except ValueError:
    st.error("Please enter the time in format MM/DD/YYYY HH:MM")
    local_times = [f"{i}:00" for i in range(24)]

st.markdown("---")

# ======================
# SECTION 2: Driver Stint Planner
# ======================
st.header("📋 24-Hour Driver Schedule")

drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])
roles = ["Driving", "Spotting", "Resting"]

planner_data = {"Time": local_times}
for d in drivers:
    planner_data[d] = ["Resting"] * 24
planner = pd.DataFrame(planner_data)

# Editable table with dropdowns
edited = st.data_editor(
    planner,
    column_config={
        d: st.column_config.SelectboxColumn(
            label=d,
            options=roles,
            required=True
        ) for d in drivers
    },
    use_container_width=True,
    num_rows="dynamic",
    key="planner_editor"
)

# ======================
# SECTION 3: Display with Role-Based Cell Coloring
# ======================

st.markdown("### 🎨 Visualized Schedule")

def highlight_roles(val):
    color_map = {
        "Driving": "#9400D3",   # F1 Purple Sector
        "Spotting": "#00FF00",  # F1 Green (Driver PB)
        "Resting": "#FFFF00"    # F1 Yellow (Not PB)
    }
    color = color_map.get(val, "white")
    return f"background-color: {color}; color: black;"

styled_df = edited.style.applymap(highlight_roles, subset=drivers)
st.dataframe(styled_df, use_container_width=True)

# ======================
# SECTION 4: Download Button
# ======================
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)
