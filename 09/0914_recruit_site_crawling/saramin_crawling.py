from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
import time
from bs4 import BeautifulSoup as bs4


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
    recruit_links = driver.find_elements(By.XPATH, '//a[@target="_blank"]')
    for link in recruit_links:
        href = link.get_attribute('href')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href)

        접수방법 = driver.find_element(By.XPATH, '//button[@class="spr_jview jv_howto ready]')
        접수방법.click()
        

        

    
    
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

df = pd.DataFrame(list2df, columns=['채용제목', '회사'])
df.to_excel('./채용정보.xlsx', index=False)