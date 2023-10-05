import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup as bs4
import pickle

def 전처리(text):
    if type(text) == str:
        text = text.replace(' ', '').replace('\n', '')
        
    return text

def makePickle(data, dir):
    with open(dir, 'w') as f:
        pickle.dump(data, f)



_, csv_path, output_dir = sys.argv

root, file = os.path.split(csv_path)
filename, ext = os.path.split(file)

df = pd.read_excel(csv_path)
keyword_list = list(df['키워드'].values)

df2list = []
driver = webdriver.Chrome()
for keyword in keyword_list:
    # link = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n"
    link = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&keydownAccess=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&searchword={keyword}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitPage=1&recruitSort=relation&recruitPageCount=40&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting="
    driver.get(link)
    # time.sleep(1)
    # recruit_button = driver.find_element(By.XPATH, '//a[@target="recruit"]') 
    # recruit_button.click()
    # time.sleep(1)
    pagination_button = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')

    try:
        for i in range(len(pagination_button)+1):
            if i > 0:
                pagination = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')
                p = pagination[i-1]
                driver.execute_script("arguments[0].click();", p)
                time.sleep(1)

            recruit_links = driver.find_elements(By.XPATH, '//*[@id="recruit_info_list"]/div[1]/div/div[2]/h2/a')

            for link in recruit_links:
                try:
                    href = link.get_attribute('href')
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(href)
                    time.sleep(1)
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
                    
                    df2list.append(['사람인', keyword, 기업명, 기업형태, 매출액, 담당자, 연락처, 홈페이지, 업종])
                    # print(['사람인', keyword, 기업명, 기업형태, 매출액, 담당자, 연락처, 홈페이지, 업종])

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except:
                    df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '홈페이지', '업종'])
                    df.to_excel(f'{output_dir}/saramin_{filename}_채용정보.xlsx', index=False)
                    # makePickle(df2list, f"{output_dir}/saramin_{filename}_채용정보.p")
    except:
        df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '홈페이지', '업종'])
        df.to_excel(f'{output_dir}/saramin_{filename}_채용정보.xlsx', index=False)
        # makePickle(df2list, f"{output_dir}/saramin_{filename}_채용정보.p")

# makePickle(df2list, f"{output_dir}/saramin_{filename}_채용정보.p")
df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '홈페이지', '업종'])
df.to_excel(f'{output_dir}/saramin_{filename}_채용정보.xlsx', index=False)

