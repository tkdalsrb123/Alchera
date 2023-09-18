import sys, os
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

_, csv_path, output_dir = sys.argv

df = pd.read_csv(csv_path, encoding='cp949')
keyword_list = list(df['키워드'].values)

df2list = []
driver = webdriver.Chrome()
for keyword in keyword_list:
    link = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n"

    driver.get(link)
    time.sleep(3)
    recruit_button = driver.find_element(By.XPATH, '//a[@target="recruit"]') 
    recruit_button.click()
    time.sleep(1)
    pagination_button = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')

    for i in range(len(pagination_button)+1):
        if i > 0:
            pagination = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')
            page_num = pagination[i].get_attribute('page')

            p = driver.find_element(By.XPATH, f'//a[@page="{page_num}"]')
            p.click()
            
        recruit_links = driver.find_elements(By.XPATH, '//*[@id="recruit_info_list"]/div[1]/div/div[2]/h2/a')
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
                연락처 = None
                for jv in jv_cont[:1]:
                    guide = jv.find('dl', attrs={'class':'guide'})
                    dt = guide.find_all('dt')
                    if '담당자' in [d.get_text() for d in dt]:
                        manager = guide.find('dd', attrs={'class':'manager'})
                        담당자 = manager.get_text()
                    elif '연락처' in [d.get_text() for d in dt]:
                        number = guide.find('dd', attrs={'class':'info'})
                        연락처 = number.get_text()

                jv_company = soup.find_all('div', attrs={'class':'jv_cont jv_company'})
                기업형태 = None
                업종 = None
                매출액 = None
                홈페이지 = None
                for jv in jv_company[:1]:
                    기업명 = jv.find('span').get_text()
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
                
                df2list.append(['사람인', 업종, 기업명, 기업형태, 매출액, 담당자, 연락처])
                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                print("에러")
                driver.close()
                driver.switch_to.window(driver.window_handles[0]) 


link = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_kewd=689%2C690%2C691%2C696%2C693%2C694%2C763%2C770&panel_type=&search_optional_item=n&search_done=y&panel_count=y&preview=y"

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
                연락처 = None
                for jv in jv_cont[:1]:
                    guide = jv.find('dl', attrs={'class':'guide'})
                    dt = guide.find_all('dt')
                    if '담당자' in [d.get_text() for d in dt]:
                        manager = guide.find('dd', attrs={'class':'manager'})
                        담당자 = manager.get_text()
                    elif '연락처' in [d.get_text() for d in dt]:
                        number = guide.find('dd', attrs={'class':'info'})
                        연락처 = number.get_text()

                jv_company = soup.find_all('div', attrs={'class':'jv_cont jv_company'})
                기업형태 = None
                업종 = None
                매출액 = None
                홈페이지 = None
                for jv in jv_company[:1]:
                    기업명 = jv.find('span').get_text()
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

                df2list.append(['사람인', 업종, 기업명, 기업형태, 매출액, 담당자, 연락처])
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

jobtogether_url = "http://www.jobtogether.net/job/jobYoung_list.do?menu=1&recFlag=1"

driver.get(jobtogether_url)
recruit_link = driver.find_elements(By.XPATH, '//*[@id="right_wrap"]/div[4]/ul/li')

for j in range(2, 7):
    if j > 2:
        page = driver.find_element(By.XPATH, f'//*[@id="paging"]/a[{j}]')
        driver.execute_script("arguments[0].click();", page)
        time.sleep(1)
    회사명 = None
    기업정보 = None
    기업형태 = None
    전화번호 = None
    for i in range(1, len(recruit_link)+1):
        link = driver.find_element(By.XPATH, f'//*[@id="right_wrap"]/div[4]/ul/li[{i}]/div[3]/p[1]/a')
        driver.execute_script("arguments[0].click();", link)
        회사명 = driver.find_element(By.XPATH, '//dl[@class="first"]/dd')
        전화번호 = driver.find_element(By.XPATH, '//div[@class="in_sepa_two"]/dl[3]/dd')
        기업정보 = driver.find_element(By.XPATH, '//*[@id="tab_2"]')
        driver.execute_script("arguments[0].click();", 기업정보)
        기업형태 = driver.find_element(By.XPATH, '//*[@id="div_tab_2"]/div[2]/div[1]/dl/dd')
        df2list.append(['잡투게더', None, 회사명, 기업형태, None, None, 전화번호])
        driver.back()

df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '이메일주소'])
df.to_excel(f'{output_dir}/채용정보.xlsx', index=False)