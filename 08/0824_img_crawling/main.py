from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os, sys

text = '자동차'

driver = webdriver.Chrome()
url = f"https://unsplash.com/ko/s/사진/{text}"

driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 30)
time.sleep(3)
load = driver.find_element(By.XPATH, "//button[@class='CwMIr DQBsa p1cWU jpBZ0 AYOsT Olora I0aPD dEcXu WMIal']")
load.click()
time.sleep(3)
images = driver.find_elements(By.XPATH, "//a[@itemprop='contentUrl']")

for img in images:
    href = img.get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(href)

    try:
        down_button = driver.find_element(By.XPATH, "//button[@class='slPFO DQBsa p1cWU jpBZ0 EzsBC KHq0c zhYdL I0aPD dEcXu cMuzD jpBZ0']")
        down_button.click()
        time.sleep(1)
        down_size_button = driver.find_elements(By.XPATH, "//a[@class='KR60y VVTRX WP6Ak eziW_ svE7J IquXd pZEJ4']")
        L_size_button = down_size_button[2]
        L_size_button.click()
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

wait.until(EC.presence_of_element_located((By.XPATH, "//button[@Class='fdrIK jpBZ0 cIVI_']")))
