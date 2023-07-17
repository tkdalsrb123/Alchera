from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup

url_title = {'시황정보 리포트':'company_list.naver', '투자정보 리포트':'invest_list.naver', '종목분석 리포트':'company_list.naver', '산업분석 리포트':'industry_list.naver', '경제분석 리포트':'economy_list.naver', '채권분석 리포트':'debenture_list.naver'}

excel = pd.read_excel(r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0706_사이트 내 PDF 파일 다운로드\save_pdf.xlsx")
# excel['날짜'] = excel['날짜'].str.replace('.', '/')
excel['날짜'] = pd.to_datetime(excel['날짜'], format='%y.%m.%d')
data = excel.values
print(data)
# driver = webdriver.Chrome()
# pdf_list = []
# date_list = []

# for val in data[:3]:
#     title = url_title[val[0]]
#     date = val[1]
#     url = f'https://finance.naver.com/research/{title}'
#     driver.get(url)
    
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     table = soup.find('table')
    
#     # 작성일 추출
#     for date in table.find_all('td', {'style':'padding-left:5px'}):
#         date_list.append(date.text)
        
#     # pdf 링크 추출
#     for pdf_link in table.find_all('td', {'class':'file'}):
#         if pdf_link.find('a') != None:
#             pdf_list.append(pdf_link.find('a').get('href'))
#             # print(pdf_link.find('a').get('href'))
    
#     date_pdf = list(zip(date_list, pdf_list))
            

    
    # next = driver.find_element(By.XPATH, '//*[@id="contentarea_left"]/div[3]/table[2]/tbody/tr/td[11]/a')
    # next.click()
    
    