from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os, sys

def down_pdf(driver):
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', {'class':'box_type_m'})
    board = table.find('table', {'class':'type_1'})
    td = table.find_all('td')
    navi = table.find('table', {'class':'Nnavi'})
    
    if category == 'company_list.naver' or category == 'industry_list.naver':
        for tr in board.find_all('tr'):
            if len(tr.find_all('td')) > 1:
                for info in tr.find_all('td'):
                    if not info.attrs.values():
                        if info.find('a') != None:
                            title = info.text
                        else:
                            company = info.text
                    elif ['file'] in info.attrs.values():   # pdf 파일 다운
                        if info.find('a') != None:
                            pdf = info.find('a').get('href')
                            pdf_name = pdf.split('/')[-1]
                            response_pdf = requests.get(pdf)
                            down_path = os.path.join(folder, pdf_name)
                            pdf_file = open(down_path, 'wb')
                            pdf_file.write(response_pdf.content)
                            pdf_file.close()
                            print(down_path, 'downloaded')
                            
                        elif info.find('a') == None:    # pdf 파일이 없을 경우
                            pdf_name = 'No'
                
                all_list.append([val[0], title, company, pdf_name, date])
    else:
        for tr in table.find_all('tr'):
            if len(tr.find_all('td')) > 1:
                for info in tr.find_all('td'):
                    if 'padding-left:10px' in info.attrs.values() or 'padding-left:10' in info.attrs.values():
                        title = info.text
                    
                    elif not info.attrs.values():
                        company = info.text
                        
                    elif ['file'] in info.attrs.values():   # pdf 파일 다운
                        if info.find('a') != None:
                            pdf = info.find('a').get('href')
                            pdf_name = pdf.split('/')[-1]
                            response_pdf = requests.get(pdf)
                            down_path = os.path.join(folder, pdf_name)
                            pdf_file = open(down_path, 'wb')
                            pdf_file.write(response_pdf.content)
                            pdf_file.close()
                            print(down_path, 'downloaded')
                            
                        elif info.find('a') == None:    # pdf 파일이 없을 경우
                            pdf_name = 'No'
                
                all_list.append([val[0], title, company, pdf_name, date])

    # 다음 페이지가 있을 경우
    for i in td:
        if i.has_attr('class'):
            if 'pgRR' in i['class']:
                all_page = navi.find_all('a')
                for page in all_page[1:-1]:
                    next = page.get('href')
                    url = f'https://finance.naver.com/{next}'
                    
                    driver.get(url)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('div', {'class':'box_type_m'})
                    board = table.find('table', {'class':'type_1'})
                    td = table.find_all('td')
                    navi = table.find('table', {'class':'Nnavi'})
                    
                    if category == 'company_list.naver' or category == 'industry_list.naver':
                        for tr in board.find_all('tr'):
                            if len(tr.find_all('td')) > 1:
                                for info in tr.find_all('td'):
                                    if not info.attrs.values():
                                        if info.find('a') != None:
                                            title = info.text
                                        else:
                                            company = info.text
                                    elif ['file'] in info.attrs.values():   # pdf 파일 다운
                                        if info.find('a') != None:
                                            pdf = info.find('a').get('href')
                                            pdf_name = pdf.split('/')[-1]
                                            response_pdf = requests.get(pdf)
                                            down_path = os.path.join(folder, pdf_name)
                                            pdf_file = open(down_path, 'wb')
                                            pdf_file.write(response_pdf.content)
                                            pdf_file.close()
                                            print(down_path, 'downloaded')
                                            
                                        elif info.find('a') == None:    # pdf 파일이 없을 경우
                                            pdf_name = 'No'
                                
                                all_list.append([val[0], title, company, pdf_name, date])
                    else:
                        for tr in table.find_all('tr'):
                            if len(tr.find_all('td')) > 1:
                                for info in tr.find_all('td'):
                                    if 'padding-left:10px' in info.attrs.values() or 'padding-left:10' in info.attrs.values():
                                        title = info.text
                                    
                                    elif not info.attrs.values():
                                        company = info.text
                                        
                                    elif ['file'] in info.attrs.values():   # pdf 파일 다운
                                        if info.find('a') != None:
                                            pdf = info.find('a').get('href')
                                            pdf_name = pdf.split('/')[-1]
                                            response_pdf = requests.get(pdf)
                                            down_path = os.path.join(folder, pdf_name)
                                            pdf_file = open(down_path, 'wb')
                                            pdf_file.write(response_pdf.content)
                                            pdf_file.close()
                                            print(down_path, 'downloaded')
                                            
                                        elif info.find('a') == None:    # pdf 파일이 없을 경우
                                            pdf_name = 'No'
                                
                                all_list.append([val[0], title, company, pdf_name, date])
                    
_, excel_dir, save_dir = sys.argv

url_category = {'시황정보 리포트':'market_info_list.naver', '투자정보 리포트':'invest_list.naver', '종목분석 리포트':'company_list.naver', '산업분석 리포트':'industry_list.naver', '경제분석 리포트':'economy_list.naver', '채권분석 리포트':'debenture_list.naver'}

excel = pd.read_excel(excel_dir)
excel['날짜'] = excel['날짜'].apply(lambda x: pd.to_datetime(x, format='%y.%m.%d').date())   # format 형식 -> 기존 데이터의 형태에 맞게 만들어야한다.
data = excel.values

driver = webdriver.Chrome()

all_list = []
for val in data:
    category = url_category[val[0]]
    date = str(val[1])
    folder = os.path.join(save_dir, val[0])
    os.makedirs(folder, exist_ok=True)
    url = f'https://finance.naver.com/research/{category}?keyword=&brokerCode=&searchType=writeDate&writeFromDate={date}&writeToDate={date}'
    driver.get(url)
    
    down_pdf(driver)

df = pd.DataFrame(all_list, columns=['리서치', '리포트제목', '증권사', 'pdf 파일명', '작성일'])
df.to_excel('./report.xlsx')
    
    


    