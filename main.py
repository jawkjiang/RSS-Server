from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from feedgen.feed import FeedGenerator
import datetime
import pytz


def scrape(key_words, language, num, tbm, time_filter):

    page_num = 0

    url = f"https://www.google.com/search?" \
          f"q={key_words}&hl={language}&num={num}&start={page_num}&tbm={tbm}&tbs=qdr:{time_filter}"

    '''
    params = {
        'q': key_words,
        'hl': language,
        'num': num,
        'start': 0,     # start refers to the page number. Use an iterator till turning back nothing.
        'tbm': tbm,     # tbm indicates the type of search results
        'tbs': f"qdr:{time_filter}"
    }
    '''

    chrome_driver_path = "D:/chromedriver-win64/chromedriver.exe"
    chrome_options = ChromeOptions()
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'main')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    feed = FeedGenerator()
    feed.title('Web3 Startup Raise News in Last 24 Hours')
    feed.link(href=url, rel='alternate')
    feed.description('None')
    feed.language('en')
    feed.generator('FeedGen')

    while soup.find_all(class_="WlydOe"):

        elements = soup.find_all(class_="WlydOe")

        for element in elements:
            entry = feed.add_entry()
            title = element.find(class_="n0jPhd ynAwRc MBeuO nDgy9d")
            entry.title(title.text)
            link = element["href"]
            entry.link(href=link)
            description = element.find(class_="GI74Re nDgy9d")
            entry.description(description.text)
            entry.guid(link)
            entry.pubDate(datetime.datetime.now(tz=pytz.timezone('America/New_York')))

        page_num += 1
        url = f"https://www.google.com/search?" \
              f"q={key_words}&hl={language}&num={num}&start={page_num}&tbm={tbm}&tbs=qdr:{time_filter}"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    rss_feed = feed.rss_str(pretty=True)
    with open("D:/feed.xml", "wb") as file:
        file.write(rss_feed)


def main():

    scrape("web3+startup+raise", "en", 10, "nws", "d")


if __name__ == "__main__":
    main()
