from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sys
from selenium.webdriver.common.keys import Keys

_, excel_dir = sys.argv

excel = pd.read_excel(excel_dir)

addresses = excel['주소'].tolist()

driver = webdriver.Chrome()

for text in addresses:
    url = f'https://map.kakao.com/?q={text}'
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    roadview = driver.find_element(By.XPATH, '//*[@id="view.map"]/div[4]/a')
    driver.execute_script("arguments[0].click();", roadview)
    time.sleep(5)
    point = driver.find_elements(By.XPATH, '//*[contains(@style, "position: absolute; z-index: 3;")]')
    actions = ActionChains(driver)
    actions.double_click(point[-1])
    actions.perform()
    time.sleep(10)
    button = driver.find_element(By.XPATH, '//*[@id="view"]/div[1]/div[1]/button')
    screenshot = driver.find_element(By.XPATH, '//*[@id="view"]/div[1]/div[1]/ul/li[1]/button')
    
    clickbutton = ActionChains(driver)\
        .click(button)
    clickbutton.perform()
    
    for i in range(30):
        time.sleep(1)
        clickscreenshot = ActionChains(driver)\
            .click(screenshot)
        clickscreenshot.perform()
        
        time.sleep(1)   
        # Keys.ARROW_RIGHT  오른쪽으로 이동
        # Keys.ARROW_LEFT  왼쪽으로 이동
        godirection = ActionChains(driver)\
            .send_keys(Keys.ARROW_LEFT)
        godirection.perform()

    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="view.roadview"]')))
driver.quit()
