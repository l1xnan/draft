# coding: utf-8
import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
from pprint import pprint
import chardet


{
    'User-Agent':      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer':         'https://book.douban.com/tag/%E6%80%9D%E6%83%B3',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'
}


def get_book_info(url):
    """
    args:
    url: 为书籍的链接，例如：'https://book.douban.com/subject/5989373/'

    returns:
    一个字典，包括书籍的元信息。
    """
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')
    # 获取书籍评分、评论人数
    rate = soup.select_one(
        '#interest_sectl  div.rating_self.clearfix > strong').text
    rate_num = soup.select_one(
        '#interest_sectl  div.rating_self.clearfix  div.rating_sum  a > span').text

    # 获取书籍信息
    children = list(soup.select('#info')[0].children)
    br = BeautifulSoup('<br/>', 'lxml').select('br')[0]

    # 找到 <br/> 的位置
    indexs = [i for i, child in enumerate(children) if child == br]

    childs = [children[:indexs[0]]]
    count = len(indexs)
    for i in range(count - 1):
        childs.append(children[indexs[i]:indexs[i + 1]])
    childs.append(children[indexs[-1]:])

    child_n = [['评分', rate], ['评论人数', rate_num]]
    for child in childs:
        string = ''.join([ch if ch.name == None else ch.text for ch in child])
        row = re.sub('\s+', '', string).split(':', 1)
        if len(row) == 2:
            child_n.append(row)

    return child_n


child_n = get_book_info(url)
print('-' * 50)
for child in child_n:
    temp = '| {0}\t| {1:30}\t|'.format(*child)
    print(temp)
    print('-' * 50)
