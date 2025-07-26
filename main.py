import streamlit as st
from sidebar import render_sidebar
import home
import dashboard
import stint_planner

st.set_page_config(page_title="ApexTurbo Motorsports", layout="wide")

# Render sidebar and get selected page
page = render_sidebar()

# Page router
if page == "Home":
    home.run()
elif page == "Dashboard":
    dashboard.run()
elif page == "Driver Stint Planner":
    stint_planner.run()
else:
    st.error("Page not found.")
