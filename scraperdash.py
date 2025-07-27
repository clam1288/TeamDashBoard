# inside dashboard.py or new streamlit page
import streamlit as st
from scraper import get_subsession_ids

st.title("🔍 Subsession Extractor")

url = st.text_input("Enter iRacing Results Page URL")

if url:
    if st.button("Fetch Subsession IDs"):
        with st.spinner("Scraping..."):
            subsession_ids = get_subsession_ids(url)
        
        if subsession_ids:
            st.success(f"Found {len(subsession_ids)} subsession IDs:")
            st.code("\n".join(subsession_ids))
            st.download_button("Download as CSV", data="\n".join(subsession_ids), file_name="subsessions.csv")
        else:
            st.error("No subsession IDs found or invalid page.")
