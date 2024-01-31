from bs4 import BeautifulSoup   #pip install bs4
import requests
import re
import pandas as pd
import datetime

category = ['Real_estate','Finance', 'Securities', 'Industry']
sections = ['realestate', 'financial-market', 'finance', 'industry']
df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for i, section in enumerate(sections):
    url = 'https://www.hankyung.com/{}'.format(section)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.news-tit')
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
df_titles.to_csv('./crawling_data/korea_economy_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')
), index=False)