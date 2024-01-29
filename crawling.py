from bs4 import BeautifulSoup   #pip install bs4
import requests
import re
import pandas as pd
import datetime

category = ['Finance', 'Securities', 'Industry', 'Venture_company', 'Real_estate', 'Global_economy', 'Living_economy', 'General_economy']
sections = [259, 258, 261, 771, 260, 262, 310, 263]
df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for i, section in enumerate(sections):
    url = 'https://news.naver.com/breakingnews/section/101/{}'.format(section)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sa_text_strong')
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                          ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')
), index=False)