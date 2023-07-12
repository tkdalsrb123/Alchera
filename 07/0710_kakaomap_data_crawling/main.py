from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton

text = '전북 장수군 장수읍 개실길\n'

driver = webdriver.Chrome()
url = 'https://map.kakao.com/'
driver.get(url)
driver.implicitly_wait(time_to_wait=3)  # 웹페이지 load 최대시간 설정

q_element = driver.find_element(By.NAME, 'q')     # 검색창 element 찾기
q_element.send_keys(text, Keys.ENTER)   # 검색창에 text 넣기
clickable = driver.find_element(By.ID, 'search.keyword.submit')
ActionChains(driver)\
    .context_click(clickable)\
    .perform()
driver.save_screenshot('./image.png')
driver.quit()

