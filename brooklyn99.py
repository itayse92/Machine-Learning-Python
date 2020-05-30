from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def is_contain(text, string):
    if text.find(string) >= 0:
            return True
    return False


driver = webdriver.Firefox()
base_url = "https://transcripts.foreverdreaming.org"
url_addition = "/viewforum.php?f=429"

# lists to columns in output excel
chapters = []
urls = []
transcripts = []

index_topic = 1  # row
for page in range(1, 5):  # pages to navigate (add on more)
    driver.get(base_url + url_addition)
    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    topics = soup.find_all("td", {"class": "topic-titles row2"})
    episodes = False

    for topic in topics:
        if not episodes and index_topic > 2:
            episodes = True
            index_topic = index_topic - 2

        if episodes and is_contain(str(topic), "h3"):
            print(f'topic #{index_topic}:')
            chapter = topic.text
            chapters.append(chapter)
            print(f'chapter: {chapter}')

            chapter_URL = topic.find("a", {"class": "topictitle"}).attrs['href']
            chapter_URL = chapter_URL[1:]
            urls.append(chapter_URL)
            print(f'URL: {chapter_URL}')

            driver.get(base_url + chapter_URL)
            time.sleep(2)
            content_sp = driver.page_source
            soup_inner = BeautifulSoup(content_sp, 'lxml')
            transcript = soup_inner.find("div", {"class": "postbody"}).text
            transcripts.append(transcript)

        # move to next row
        print("\n")
        index_topic = index_topic + 1

    # move to next page
    page_buttons = soup.find("b", {"class": "pagination"})
    pages_links = page_buttons.find_all("a")
    for p in pages_links:
        if p.text == "»":
            url_addition = p.attrs['href']
            url_addition = url_addition[1:]


# store in excel
store_in_excel = pd.DataFrame({'Chapter': chapters, 'URL': urls, 'Transcript': transcripts})
store_in_excel.to_csv('Brooklyn.csv', index=False, encoding='utf-8')
