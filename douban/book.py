import requests
from lxml import etree
from bs4 import BeautifulSoup
import re


tags = []
with open('tags.txt', 'r', encoding='utf-8') as file:
    tags = [line.strip() for line in file]


def douban_tag_ranks(tag):
    url = 'https://book.douban.com/tag/' + tag + '?type=S'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    a_tags = soup.select('#subject_list > ul > li > div.info > h2 > a')

    for i, a in enumerate(a_tags):
        href = a.get('href')
        title = re.sub('\s+', '', a.text)

wenhua = douban_tag_ranks('文化')
