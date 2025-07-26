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
    with
