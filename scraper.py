# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_subsession_ids(url: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    card = soup.find("div", class_="card-header", string="Race Splits")
    if not card:
        driver.quit()
        return []

    card_block = card.find_parent("div", class_="card").find("div", class_="card-block")
    rows = card_block.find_all("div", class_="row")

    subsession_ids = []
    for row in rows:
        if "subsessionid=" in row.text:
            links = row.find_all("a", href=True)
            for link in links:
                if "subsessionid=" in link['href']:
                    sid = link['href'].split("subsessionid=")[-1]
                    subsession_ids.append(sid)

    driver.quit()
    return subsession_ids
