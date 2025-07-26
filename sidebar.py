import streamlit as st

def render_sidebar():
    st.sidebar.title("ApexTurbo Motorsports")

    pages = {
        "Home": "Home",
        "Dashboard": "Dashboard",
        "Driver Stint Planner": "Driver Stint Planner"
    }

    st.sidebar.markdown("### Navigation")
    for label, target in pages.items():
        st.sidebar.markdown(f"- [{label}](?page={target})")

    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["Home"])[0]

    return current_page
