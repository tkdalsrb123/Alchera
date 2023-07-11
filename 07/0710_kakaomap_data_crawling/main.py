from selenium import webdriver

text = '전북 장수군 장수읍 개실길'

driver = webdriver.Chrome()
url = 'https://search.map.kakao.com/mapsearch/map.daum?callback=jQuery18109267327558913874_1689065809524&q=+%EC%A0%84%EB%B6%81+%EC%9E%A5%EC%88%98%EA%B5%B0+%EC%9E%A5%EC%88%98%EC%9D%8D+%EA%B0%9C%EC%8B%A4%EA%B8%B8&msFlag=A&sort=0'
driver.get(url)

