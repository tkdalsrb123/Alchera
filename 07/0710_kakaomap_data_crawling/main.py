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

# text = '전북 장수군 장수읍 개실길'

driver = webdriver.Chrome()
url = 'http://localhost:8080/07/0710_kakaomap_data_crawling/test_roadview/test.html'
driver.get(url)
try:
    wait = WebDriverWait(driver, 30)
    for i in range(10):
        time.sleep(2)
        driver.save_screenshot(f'./image{i}.png')
        driver.find_element(By.XPATH, '//div[contains(@id,"_ar_10_")]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@id,"_ar_10_")]')))
finally:
    driver.quit()