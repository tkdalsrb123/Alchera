from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



driver = webdriver.Chrome()
url = "http://www.jobtogether.net/job/jobYoung_list.do?menu=1&recFlag=1"

driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 30)

recruit_link = driver.find_elements(By.XPATH, '//*[@id="right_wrap"]/div[4]/ul/li')

for j in range(2, 7):
    if j > 2:
        page = driver.find_element(By.XPATH, f'//*[@id="paging"]/a[{j}]')
        driver.execute_script("arguments[0].click();", page)
        time.sleep(1)
    for i in range(1, len(recruit_link)+1):
        link = driver.find_element(By.XPATH, f'//*[@id="right_wrap"]/div[4]/ul/li[{i}]/div[3]/p[1]/a')
        driver.execute_script("arguments[0].click();", link)
        회사명 = driver.find_element(By.XPATH, '//dl[@class="first"]/dd')
        전화번호 = driver.find_element(By.XPATH, '//div[@class="in_sepa_two"]/dl[3]/dd')
        기업정보 = driver.find_element(By.XPATH, '//*[@id="tab_2"]')
        driver.execute_script("arguments[0].click();", 기업정보)
        기업형태 = driver.find_element(By.XPATH, '//*[@id="div_tab_2"]/div[2]/div[1]/dl/dd')
        print(회사명.text, 전화번호.text, 기업형태.text)
        driver.back()


wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="tx01"]')))