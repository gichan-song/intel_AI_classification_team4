from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Finance', 'Securities', 'Industry', 'Venture_company', 'Real_estate', 'Global_economy', 'Living_economy', 'General_economy']
sections = [259, 258, 261, 771, 260, 262, 310, 263]
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣]')
for i, section in enumerate(sections):
    url = 'https://news.naver.com/breakingnews/section/101/{}'.format(section)
    titles = []
    driver.get(url)
    time.sleep(0.5)
    for n in range(30):
        try:
            driver.find_element('xpath', '//*[@id="newsct"]/div[2]/div/div[2]/a').click()
            time.sleep(0.2)
        except:
            print('driver.get', category[i], n)
    title_tags = driver.find_elements(By.CLASS_NAME, 'sa_text_strong')
    for title_tag in title_tags:
        try:
            title = re_title.sub(' ', title_tag.text)
            titles.append(title)
        except:
            print('re compile miss')
    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[i]
    df_section_title.to_csv('./crawling_data/data_{}.csv'.format(category[i]), index=False)
    df_titles = pd.concat([df_titles, df_section_title], axis=0, ignore_index=True)

df_titles.to_csv('./crawling_data/naver_news_economy_data.csv', index=False)
print(df_titles.head())
print(df_titles["category"].value_counts())
print(df_titles.info())

driver.close()
