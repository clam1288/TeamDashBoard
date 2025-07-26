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
