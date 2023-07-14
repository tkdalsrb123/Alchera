from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# driver = webdriver.Chrome()
# url = 'http://localhost:8080/07/0710_kakaomap_data_crawling/test_roadview/test.html'
# driver.get(url)
# try:
#     wait = WebDriverWait(driver, 30)
#     for i in range(10):
#         time.sleep(2)
#         driver.save_screenshot(f'./image{i}.png')
#         driver.find_element(By.XPATH, '//div[contains(@id,"_ar_10_")]').click()
#     wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@id,"_ar_10_")]')))
# finally:
#     driver.quit()
text = '전라북도 장수군 장수읍 개정농원길'

driver = webdriver.Chrome()
url = f'https://map.kakao.com/?q={text}'
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 30)
roadview = driver.find_element(By.XPATH, '//*[@id="view.map"]/div[4]/a')
driver.execute_script("arguments[0].click();", roadview)
time.sleep(5)
point = driver.find_elements(By.XPATH, '//*[contains(@style, "position: absolute; z-index: 3;")]')
actions = ActionChains(driver)
actions.double_click(point[-1])
actions.perform()
time.sleep(5)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="view.mapContainer"]/div[2]/div/div[6]/*')))
driver.quit()
# //*[@id="view.mapContainer"]/div[2]/div/div[6]/div[9]
# //*[@id="view.mapContainer"]/div[2]/div/div[6]/div[6]
