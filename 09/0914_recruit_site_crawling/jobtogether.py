from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import sys

_, output_dir = sys.argv

jobtogether_url = "http://www.jobtogether.net/job/jobYoung_list.do?menu=1&recFlag=1"

df2list = []
driver = webdriver.Chrome()
driver.get(jobtogether_url)
recruit_link = driver.find_elements(By.XPATH, '//*[@id="right_wrap"]/div[4]/ul/li')
wait = WebDriverWait(driver, 60)
for j in range(2, 7):
    if j > 2:
        page = driver.find_element(By.XPATH, f'//*[@id="paging"]/a[{j}]')
        driver.execute_script("arguments[0].click();", page)
        wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="right_wrap"]/div[4]/ul/li[{i}]/div[3]/p[1]/a')))
        time.sleep(1)
    회사명 = None
    기업정보 = None
    기업형태 = None
    전화번호 = None
    홈페이지 = None
    for i in range(1, len(recruit_link)+1):
        try:
            time.sleep(1)
            link = driver.find_element(By.XPATH, f'//*[@id="right_wrap"]/div[4]/ul/li[{i}]/div[3]/p[1]/a')
            driver.execute_script("arguments[0].click();", link)
            회사명 = driver.find_element(By.XPATH, '//dl[@class="first"]/dd').get_attribute('innerText')
            전화번호 = driver.find_element(By.XPATH, '//div[@class="in_sepa_two"]/dl[3]/dd').get_attribute('innerText')
            기업정보 = driver.find_element(By.XPATH, '//*[@id="tab_2"]')
            driver.execute_script("arguments[0].click();", 기업정보)
            기업형태 = driver.find_element(By.XPATH, '//*[@id="div_tab_2"]/div[2]/div[1]/dl/dd').get_attribute('innerText')
            홈페이지 = driver.find_element(By.XPATH, '//*[@id="right_wrap"]/div[3]/dl[3]/dd/a').get_attribute('innerText')
            df2list.append(['잡투게더', '무역', 회사명, 기업형태, None, None, 전화번호, 홈페이지, None])
            print(['잡투게더', '무역', 회사명, 기업형태, None, None, 전화번호, 홈페이지, None])
            driver.back()
        except:
            df2list.append(['잡투게더', '무역', 회사명, 기업형태, None, None, 전화번호, None, None])
            print(['잡투게더', '무역', 회사명, 기업형태, None, None, 전화번호, None, None])
            driver.back()
wait.until(EC.presence_of_element_located((By.XPATH, '//p[@class="tx01"]')))
        

df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '홈페이지', '업종'])
df.to_excel(f'{output_dir}/jobtogether_채용정보.xlsx', index=False)
