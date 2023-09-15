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
    

keyword = '데이터분석가' 
link = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n"

driver = webdriver.Chrome()
driver.get(link)
driver.maximize_window()
time.sleep(3)
recruit_button = driver.find_element(By.XPATH, '//a[@target="recruit"]') 
recruit_button.click()
time.sleep(1)
pagination_button = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')

list2df = []
for i in range(len(pagination_button)):
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
            print(기업형태, 업종, 매출액, 홈페이지)



            # print(홈페이지.strip())
            # content = driver.find_element(By.TAG_NAME, 'iframe')
            # driver.switch_to.frame(content)
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            print("에러")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # time.sleep(3)
    # pagination = driver.find_elements(By.XPATH, '//a[@class=" page page_move track_event"]')
    # page_num = pagination[i].get_attribute('page')

    # p = driver.find_element(By.XPATH, f'//a[@page="{page_num}"]')
    # p.click()

    # html = driver.page_source

    # # beautiful soup
    # soup = bs4(html, 'html.parser')

    # result = soup.find_all('div', attrs={'class':'item_recruit'})

    # for res in result:
    #     main = res.find('div', attrs={'class':'area_job'})
    #     title = main.find('span').text

    #     company = res.find('strong', attrs={'class':'corp_name'})
    #     company_name = company.text
    #     company_name = company_name.replace('\n','').strip()

    #     list2df.append([title, company_name])

# df = pd.DataFrame(list2df, columns=['채용제목', '회사'])
# df.to_excel('./채용정보.xlsx', index=False)