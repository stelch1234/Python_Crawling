from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import requests
import konlpy
from konlpy.tag import Twitter
from urllib.request import urlopen
import re

driver = webdriver.Chrome('~~~')
driver.implicitly_wait(3)

#로그인 전용 화면
driver.get('https://m.nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/aside/')
#아이디와 비번 입력
driver.find_element_by_name('id').send_keys('NaverID')
driver.find_element_by_name('pw').send_keys('NaverPW')

#로그인 버튼 클릭
driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
