import streamlit as st

def render_sidebar(active="Dashboard"):
    st.sidebar.title("ApexTurbo Motorsports")

    page = st.sidebar.radio(
        "Navigation",
        ["Landing Page", "Dashboard", "Driver Stint Planner"],
        index=["Landing Page", "Dashboard", "Driver Stint Planner"].index(active)
    )

    # Show toggle only on Stint Planner
    if page == "Driver Stint Planner":
        if "automated_mode" not in st.session_state:
            st.session_state.automated_mode = False

        automated_mode = st.sidebar.toggle("Enable Automated Mode", value=st.session_state.automated_mode)
        st.session_state.automated_mode = automated_mode

    return page
