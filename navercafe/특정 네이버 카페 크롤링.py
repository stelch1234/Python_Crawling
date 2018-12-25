from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import re
import requests

list_url = 'https://m.cafe.naver.com/ArticleAllListAjax.nhn'

#인자들을 params로 받는다
params = {
    'search.clubid' : '10186119',   #카페 고유 id
    'search.query' : '치안',  # 찾고자 하는 키워드
    'search.boardtype' : 'L',
    'search.questionTab' : 'A',
    'search.totalCount': '201',
    'search.page' : 1,
}

html = requests.get(list_url, params = params).text
soup = bs(html, 'html.parser')
print(soup)