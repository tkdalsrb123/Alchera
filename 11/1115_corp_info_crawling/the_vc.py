import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_company_names(path):
    company_names = []
    df = pd.read_csv(path, encoding='utf-8')
    df.apply(lambda x: company_names.append((x['분야'], x['회사명'])), axis=1)

    return company_names

def login(driver, id, pw):
    time.sleep(1)
    input_id = driver.find_element(By.XPATH, '//input[@id="email"]')
    input_pw = driver.find_element(By.XPATH, '//input[@id="password"]')
    input_id.send_keys(id)
    input_pw.send_keys(pw)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    
def crawling_data():
    LINK = "https://thevc.kr/auth/login"
    USERID = 'joohyunghan1104@gmail.com'
    USERPW = 'qhrtlf123'


    keyword_list = get_company_names('./company_names.csv')
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    driver.get(LINK)

    login(driver, USERID, USERPW)
    
    info_list = []
    for keyword in keyword_list:
        subject = keyword[0]
        keyword = keyword[1].replace('(주)','').replace('주식회사', '')
        keyword = keyword.strip()
        try:
            link = f"https://thevc.kr/search/overview?keyword={keyword}"
            driver.get(link)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="grid fill-300 gap-16"]')))
            corp_site = driver.find_elements(By.XPATH, '//div[@class="grid fill-300 gap-16"]')
            if len(corp_site) > 0:
                corp = corp_site[0].find_elements(By.XPATH, '//div[@class="flex gap-8 align-center"]')
                time.sleep(3)
                if len(corp) > 0:
                    corp[0].click()
                    time.sleep(3)

                    info = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__nuxt"]/div[1]/div/div/aside/div/div[1]/div[2]/dl')))
                    info_split = info.text.split('\n')
                    email = info_split[1]
                    number = info_split[3]
                    url = info_split[5]
                    
                    info_list.append([subject, keyword, email, number, url])
        except:
            pass     
    
    df = pd.DataFrame(info_list, columns=['분야', '회사명', '이메일', '전화번호', '홈페이지'])
    df.index += 1
    df.to_excel('./company_info.xlsx')
            
if __name__ == '__main__':
    _ = sys.argv
    print('---------collecting company info--------')
    crawling_data()
    print('----------------Done!--------------------')
    
    