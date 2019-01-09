import requests
import pandas as pd
import time
import os
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#chrome driver 불어오기
driver = webdriver.Chrome('/~path')

#기본 설정
#맥주: hoegaarden
base_url = 'https://www.ratebeer.com/beer/hoegaarden/399/'
driver.get(base_url)
#페이지 로드를 위한 2초
time.sleep(2)

#리뷰를 보는 방식은 스크롤을 하단으로 내려 'seeall' 버튼을 내려야 함
body = driver.find_element_by_tag_name('body')
body.send_keys(Keys.DOWN)
driver.find_element_by_css_selector('#seeAll').click()

#seeall버튼을 누른 다음에 리뷰 페이지로 넘어가지만 스크롤을 계속 내려야 모든 리뷰를 볼 수 있음
#스크롤을 계속 믿으로 내려 보내는 작업
for page_down in range(1,500):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

#댓글 태그가 2종류로 되어 있어 2종류 모두 불러옴
review_list = []
soup = bs(driver.page_source, 'html.parser')
reviews1 = soup.select('div.LinesEllipsis  ')
reviews2 =  soup.select('div.LinesEllipsis LinesEllipsis--clamped ')
for review1 in reviews1:
    review1 = review1.get_text()
    #태그 지우기
    review1  = re.sub('<.+?>', '', review1, 0).strip()
    review_list.append({'reviews' : review1})
for review2 in reviews2:
    review2 = review2.get_text()
    review2 = re.sub('<.+?>', '', review2, 0).strip()
    review_list.append({'reviews' : review2})

#csv파일로 저장
beer_df = pd.DataFrame(review_list)
beer_df.to_csv('beer_호가든.csv', index=False)