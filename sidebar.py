import streamlit as st

def render_sidebar():
    st.sidebar.title("ApexTurbo Motorsports")

    # Logo (optional: if you have a logo file in 'assets' folder)
    # st.sidebar.image("assets/logo.png", use_column_width=True)

    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Landing Page", "Dashboard", "Stint Planner"],
        index=1
    )

    # Mode toggle (specific to Stint Planner use case)
    if page == "Stint Planner":
        if "automated_mode" not in st.session_state:
            st.session_state.automated_mode = False

        automated_mode = st.sidebar.toggle("Enable Automated Mode", value=st.session_state.automated_mode)
        st.session_state.automated_mode = automated_mode

    return page
