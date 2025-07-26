import streamlit as st
import pandas as pd

st.set_page_config(page_title="ApexTurbo - Driver Stint Planner", layout="wide")

st.title("🕒 Driver Stint Planner")
st.markdown("Plan out your team’s 24-hour endurance schedule below.")

# Define hours of the race (0 to 23)
hours = [f"{h}:00" for h in range(24)]

# Define team members
drivers = st.multiselect("Select drivers", options=["Tom", "Chad", "Kyle"], default=["Tom", "Chad", "Kyle"])

# Define available roles
roles = ["Driving", "Spotting", "Resting"]

# Initialize planner if not already in session state
if "planner" not in st.session_state:
    st.session_state.planner = pd.DataFrame({
        "Hour": hours,
    })
    for d in drivers:
        st.session_state.planner[d] = ["Resting"] * 24

# Display editable planner
edited = st.data_editor(
    st.session_state.planner,
    use_container_width=True,
    num_rows="dynamic",
    key="planner_editor"
)

# Save updated planner
st.session_state.planner = edited

# Option to download
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Plan as CSV",
    csv,
    "driver_stint_plan.csv",
    "text/csv",
    key="download-csv"
)

