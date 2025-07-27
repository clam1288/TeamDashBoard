# scraperdash.py
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from io import StringIO

# ---------------------------
# Scraping Function
# ---------------------------
def get_subsession_ids(url: str):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        time.sleep(5)  # Allow JS to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        card = soup.find("div", class_="card-header", string="Race Splits")
        if not card:
            driver.quit()
            return []

        card_block = card.find_parent("div", class_="card").find("div", class_="card-block")
        rows = card_block.find_all("div", class_="row")

        subsession_ids = []
        for row in rows:
            links = row.find_all("a", href=True)
            for link in links:
                if "subsessionid=" in link['href']:
                    sid = link['href'].split("subsessionid=")[-1]
                    subsession_ids.append(sid)

        driver.quit()
        return list(set(subsession_ids))  # remove duplicates
    except Exception as e:
        return f"ERROR: {e}"

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="iRacing Subsession Extractor", layout="centered")
st.title("🔍 iRacing Race Split Subsession Scraper")

st.markdown("Paste an iRacing event page URL below (like a results overview), and this tool will extract all subsession IDs.")

url = st.text_input("iRacing Race Results URL")

if url:
    if st.button("Fetch Subsession IDs"):
        with st.spinner("Scraping race splits..."):
            result = get_subsession_ids(url)

        if isinstance(result, list):
            if result:
                st.success(f"✅ Found {len(result)} subsession IDs")
                df = pd.DataFrame(result, columns=["Subsession ID"])
                st.dataframe(df)

                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button("⬇️ Download as CSV", data=csv_buffer.getvalue(), file_name="subsession_ids.csv", mime="text/csv")
            else:
                st.warning("No subsession IDs found on the page.")
        else:
            st.error(result)
