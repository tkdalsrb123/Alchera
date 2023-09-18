from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
import time
from bs4 import BeautifulSoup as bs4

def 전처리(text):
    if type(text) == str:
        text = text.replace(' ', '')
        
    return text


link = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=689%2C690%2C691%2C696%2C693%2C694%2C763%2C770&panel_type=&search_optional_item=n&search_done=y&panel_count=y&preview=y"

driver = webdriver.Chrome()
driver.get(link)
time.sleep(3)

page_list = driver.find_elements(By.XPATH, '//button[@class="BtnType SizeS"]')

while page_list:
    page_list = driver.find_elements(By.XPATH, '//button[@class="BtnType SizeS"]')
    for page in range(len(page_list)+1):
        if page > 0:
            page_num = driver.find_elements(By.XPATH, '//button[@class="BtnType SizeS"]')
            page_num[page-1].click()
        recruit_links = driver.find_elements(By.XPATH, '//a[@class="str_tit "]')
        for link in recruit_links:
            href = link.get_attribute('href')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(href)
            time.sleep(4)
            try:
                html = driver.page_source
                soup = bs4(html, 'html.parser')
                jv_cont = soup.find_all('div', attrs={'class':'jv_cont jv_howto'})
                담당자 = None
                for jv in jv_cont[:1]:
                    guide = jv.find('dl', attrs={'class':'guide'})
                    dt = guide.find_all('dt')
                    if '담당자' in [d.get_text() for d in dt]:
                        manager = guide.find('dd', attrs={'class':'manager'})
                        담당자 = manager.get_text()

                jv_company = soup.find_all('div', attrs={'class':'jv_cont jv_company'})
                기업형태 = None
                업종 = None
                매출액 = None
                홈페이지 = None
                for jv in jv_company[:1]:
                    info = jv.find_all('dl')
                    for i in info:   
                        if '기업형태' in i.find('dt').get_text():
                            기업형태 = i.find('dd').get_text()
                        elif '업종' in i.find('dt').get_text():
                            업종 = i.find('dd').get_text()
                        elif '매출액' in i.find('dt').get_text():
                            매출액 = i.find('dd').get_text()
                        elif '홈페이지' in i.find('dt').get_text():
                            홈페이지 = i.find('dd').get_text()
                
                기업형태 = 전처리(기업형태)
                업종 = 전처리(업종)
                매출액 = 전처리(매출액)
                홈페이지 = 전처리(홈페이지)

                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                print("에러")
                driver.close()
                driver.switch_to.window(driver.window_handles[0]) 
            
    try:
        next_page = driver.find_element(By.XPATH, '//button[@class="BtnType SizeS BtnNext"]')
        next_page.click()
    except:
        print('마지막 페이지입니다')
        break



