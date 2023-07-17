from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os, sys

def down_pdf(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', {'class':'box_type_m'})
    td = table.find_all('td')

    # pdf 링크 추출
    for pdf_link in table.find_all('td', {'class':'file'}):
        if pdf_link.find('a') != None:
            pdf = pdf_link.find('a').get('href')
            pdf_name = pdf.split('/')[-1]
            response_pdf = requests.get(pdf)
            down_path = os.path.join(folder, pdf_name)
            pdf_file = open(down_path, 'wb')
            pdf_file.write(response_pdf.content)
            pdf_file.close()
            print(down_path, 'downloaded')
            
    # 다음 페이지가 있을 경우
    for i in td:
        if i.has_attr('class'):
            if 'pgRR' in i['class']:
                next = driver.find_element(By.XPATH, '//*[@id="contentarea_left"]/div[3]/table[2]/tbody/tr/td[3]')
                next.click()
                down_pdf(driver)
    
    
_, excel_dir, save_dir = sys.argv

url_title = {'시황정보 리포트':'company_list.naver', '투자정보 리포트':'invest_list.naver', '종목분석 리포트':'company_list.naver', '산업분석 리포트':'industry_list.naver', '경제분석 리포트':'economy_list.naver', '채권분석 리포트':'debenture_list.naver'}

excel = pd.read_excel(excel_dir)
excel['날짜'] = excel['날짜'].apply(lambda x: pd.to_datetime(x, format='%y.%m.%d').date())   # format 형식 -> 기존 데이터의 형태에 맞게 만들어야한다.
data = excel.values

driver = webdriver.Chrome()
pdf_list = []
date_list = []

for val in data:
    title = url_title[val[0]]
    date = str(val[1])
    folder = os.path.join(save_dir, val[0])
    os.makedirs(folder, exist_ok=True)
    url = f'https://finance.naver.com/research/{title}'
    driver.get(url)

    # 찾고자 하는 기간 입력
    start_date = driver.find_element(By.XPATH, '//*[@type="text"][@title="시작 기간 입력"]')
    start_date.click()
    start_date.send_keys(Keys.CONTROL + 'a')
    start_date.send_keys(date)
    end_date = driver.find_element(By.XPATH, '//*[@type="text"][@title="끝나는 기간 입력"]')
    end_date.click()
    end_date.send_keys(Keys.CONTROL + 'a')
    end_date.send_keys(date)
    
    driver.find_element(By.XPATH, '//*[@type="image"][@alt="검색"]').click()
    
    down_pdf(driver)


    
    


    