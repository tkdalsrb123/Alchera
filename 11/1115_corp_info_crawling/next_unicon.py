import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login(driver, id, pw):
    input_id = driver.find_element(By.XPATH, '//input[@name="email"]')
    input_pw = driver.find_element(By.XPATH, '//input[@name="password"]')
    input_id.send_keys(id)
    input_pw.send_keys(pw)
    input_pw.send_keys(Keys.RETURN)


def crawling_data():
    LINK = 'https://www.nextunicorn.kr/login'
    USERID = 'joohyunghan1104@gmail.com'
    USERPW = 'qhrtlf123'

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    driver.get(LINK)

    login(driver, USERID, USERPW)

    link = "https://www.nextunicorn.kr/finder"
    time.sleep(1)
    driver.get(link)
    
    category = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="sc-1gaf0b5-1 iHmnaz"]')))
    category = category.find_element(By.XPATH, '//li[@data-category-name="biz"]')
    category.click()
    
    subjects = driver.find_elements(By.XPATH, '//div[@class="sc-ob0hua-1 bsmhgS"]')
    list2df = []
    for idx, sub in enumerate(subjects):
        if idx in [0, 1, 2, 6, 8, 16]:
            sub.click()

            while True:
                button = driver.find_elements(By.XPATH, '//button[@data-event="finder/:tabName/seeMore"]')

                if len(button) > 0:
                    button[0].click()
                    time.sleep(1)

                else:
                    break
            
            name_list = driver.find_element(By.XPATH, '//div[@class="sc-1xk12lb-0 dbdPec"]').find_elements(By.TAG_NAME, 'a')
            print(f"{sub.text}: {len(name_list)}개 수집!!")
            
            [list2df.append([sub.text, name.text.split('\n')[0]]) for name in name_list]

            time.sleep(3)
            sub.click()
        
    df = pd.DataFrame(list2df, columns=['분야', '회사명'])
    df.index += 1
    df.to_csv('./company_names.csv')

if __name__ == '__main__':
    _ = sys.argv
    print('---------collecting company names--------')
    crawling_data()
    print('----------------Done!--------------------')
    