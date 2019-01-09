from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DbMgr import DBHelper as Db
import time
from Tour import TourInfo

# 사전에 필요한 정보를 로드 => 디비혹스 쉘, 베치 파일에서 인자로 받아서 세팅
db = Db()
main_url = 'http://tour.interpark.com/'
keyword = '로마'
# 상품 정보를 담는 리스트 (TourInfo 리스트)
tour_list = []

# 드라이버 로드
driver = wd.Chrome(executable_path='chromedriver.exe')

# 사이트 접속 (get)
driver.get(main_url)
# 검색창을 찾아서 검색어 입력
# id : SearchGNBText
driver.find_element_by_id('SearchGNBText').send_keys(keyword)

# 검색 버튼 클릭
driver.find_element_by_css_selector('button.search-btn').click()

# 명시적 대기 => 특정 요소가 로케이트(발결된때까지) 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개 요소가 올라면 웨이트 종료
        EC.presence_of_element_located((By.CLASS_NAME, 'oTravelBox'))
    )
except Exception as e:
    print('오류 발생', e)

# 게시물에서 데이터 가져오기
# searchModule.SetCategoryList(1, '') 스크립트 실행
# 16은 임시값, 게시물을 넘어갔을때 현상을 확인차
for page in range(1, 2):  # 16):
    try:
        # 자바스크립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print("%s 페이지 이동" % page)
        # 상품명, 코멘트, 기간1, 기간2, 가격, 평점, 썸네일, 링크(상품상세정보)
        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        # 상품 하나 하나 접근
        for li in boxItems:
            # 이미지를 링크값을 사용할것인가?
            # 직접 다운로드 해서 우리 서버에 업로드(ftp) 할것인가?
            print('썸네임', li.find_element_by_css_selector('img').get_attribute('src'))
            print('링크', li.find_element_by_css_selector('a').get_attribute('onclick'))
            print('상품명', li.find_element_by_css_selector('h5.proTit').text)
            print('코멘트', li.find_element_by_css_selector('.proSub').text)
            print('가격', li.find_element_by_css_selector('.proPrice').text)
            area = ''
            for info in li.find_elements_by_css_selector('.info-row .proInfo'):
                print(info.text)
            print('=' * 100)
            # 데이터 모음
            # li.find_elements_by_css_selector('.info-row .proInfo')[1].text
            # 데이터가 부족하거나 없을수도 있으므로 직접 인덱스로 표현은 위험성이 있음
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text,
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src')
            )
            tour_list.append(obj)
    except Exception as e1:
        print('오류', e1)

print(tour_list, len(tour_list))

# 수집한 정보 개수를 루프 => 페이지 방문 => 콘텐츠 획득(상품상세정보) => 디비
for tour in tour_list:
    print(type(tour))
    arr = tour.link.split(',')
    if arr:
        # 대체
        link = arr[0].replace('searchModule.OnClickDetail(', '')
        # 슬라이싱 => 앞에 ', 뒤에 ' 제거
        detail_url = link[1:-1]
        # 상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http~)
        driver.get(detail_url)
        time.sleep(2)
        # pip install bs4
        # 혖재 페이지를 beautifulsoup의 DOM으로 구성
        soup = bs(driver.page_source, 'html.parser')
        # 현제 상세 정보 페이지에서 스케줄 정보 획득
        data = soup.select('.tip-cover')
        # print( type(data), len(data), type(data[0].contents)  )
        # 디비 입력 => pip install pymysql
        # 데이터 sum
        content_final = ''
        for c in data[0].contents:
            content_final += str(c)

        # html 콘첸츠 데이터 전처리 (디비에 입력 가능토록)
        import re

        content_final = re.sub("'", '"', content_final)
        content_final = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)

        print(content_final)
        # 콘텐츠 내용에 따라 전처리 => data[0].contents
        db.db_insertCrawlingData(
            tour.title,
            tour.price[:-1],
            tour.area.replace('출발 가능 기간 : ', ''),
            content_final,
            keyword
        )

# 종료
driver.close()

import sys
sys.exit()