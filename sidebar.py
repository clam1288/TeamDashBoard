import streamlit as st

def render_sidebar(active="Dashboard"):
    st.sidebar.title("ApexTurbo Motorsports")

    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Dashboard", "Driver Stint Planner"],
        index=["Home", "Dashboard", "Driver Stint Planner"].index(active)
    )

    return page
