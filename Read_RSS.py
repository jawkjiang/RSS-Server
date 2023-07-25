import feedparser
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def main():

    chrome_driver_path = "D:/chromedriver-win64/chromedriver.exe"
    chrome_options = ChromeOptions()
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    rss_url = 'D:/feed.xml'
    feed = feedparser.parse(rss_url)

    root = ET.Element("file")
    for entry in feed.entries:

        driver.get(entry.link)

        wait = WebDriverWait(driver, 15)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'p')))
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            paragraphs = soup.find_all("p")
            txt = ""
            for para in paragraphs:
                txt += para.text

        except TimeoutException or WebDriverException:
            continue

        print(txt)

        item = ET.SubElement(root, "entry")
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "content").text = txt

    tree = ET.ElementTree(root)
    with open("D:/ChatGPT_file.xml", "wb") as xml_file:
        tree.write(xml_file)


if __name__ == '__main__':
    main()
