import streamlit as st

st.set_page_config(page_title="ApexTurbo Home", layout="centered")

st.title("🏁 Welcome to ApexTurbo Motorsports")
st.markdown("### We don’t hotlap. We finish together.")

st.write("""
ApexTurbo is a toolkit built for endurance racing teams. Whether you're running the 24H of Daytona or a local team league,
we help your squad prepare, plan, and perform.

**What you’ll find here:**
- ✅ Driver stint planner
- ⛽ Fuel & tire strategy (coming soon)
- 🗒 Team track guides (coming soon)
- 📊 Study & consistency tools

Built by racers — for racers.
""")

st.markdown("### 🔗 Start Planning")
st.page_link("pages/Driver Planner.py", label="🕒 Open Driver Stint Planner")
