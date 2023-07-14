from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# text = '전북 장수군 장수읍 개실길'

# chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument('--headless')

# chrome_options.add_argument('--no-sandbox')

# chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome()
url = 'http://localhost:8080/07/0710_kakaomap_data_crawling/test_roadview/test.html'
driver.get(url)
driver.implicitly_wait(time_to_wait=5)  # 웹페이지 load 최대시간 설정

# # q_element = driver.find_element(By.NAME, 'q')     # 검색창 element 찾기
# # q_element.send_keys(text, Keys.ENTER)   # 검색창에 text 넣기
clickable = driver.find_element(By.ID, '_ar_14_512')
ActionChains(driver)\
    .context_click(clickable)\
    .perform()
# # clickable = driver.find_element(By.ID, 'roadview')
# # ActionChains(driver)\
# #     .context_click(clickable)\
# #     .perform()
# # clickable = driver.find_element(By.ID, 'roadview')
driver.save_screenshot('./image.png')
driver.quit()

# from seleniumwire import webdriver  # Import from seleniumwire

# # Create a new instance of the Chrome driver
# driver = webdriver.Chrome()

# # Go to the Google home page
# driver.get('http://localhost:8080/07/0710_kakaomap_data_crawling/test_roadview/test.html')

# # Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.response:
#         print(
#             request.url,'url',
#             request.response.status_code,'status_cod',
#             request.response.headers['Content-Type'], 'contenttype'
#         )
# driver.save_screenshot('./image.png')
# driver.quit()