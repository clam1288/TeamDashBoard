from sidebar import render_sidebar
import home
import dashboard
import stint_planner  # your other module

page = render_sidebar()

if page == "Home":
    home.run()
elif page == "Dashboard":
    dashboard.run()
elif page == "Driver Stint Planner":
    stint_planner.run()
else:
    st.error("Page not found.")
