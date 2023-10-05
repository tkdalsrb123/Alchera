import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup as bs4
import pickle
from tqdm import tqdm

def save_df(data, path):
    df = pd.DataFrame(data, columns=['No.', '기업명', '대표 전화번호', '전자우편(E-mail)'])
    df.to_excel(f"{path}/cor_data.xlsx", index=False)

_, csv_dir, output_dir = sys.argv

df = pd.read_csv(csv_dir, encoding='cp949',header=1)
cor_list = list(df['기업명'])

link = "https://www.ftc.go.kr/www/biz/bizCommList.do?key=5375"

driver = webdriver.Chrome()

df2list = []
i = 1
for cor in tqdm(cor_list[:30], desc='수집중'):
    try:
        driver.get(link)
        category = driver.find_element(By.XPATH, '//*[@id="searchCnd"]')
        name = driver.find_element(By.XPATH, '//*[@id="searchCnd"]/option[3]')
        input_box = driver.find_element(By.XPATH, '//*[@id="boardsearch"]')
        category.click()
        name.click()
        input_box.clear()
        input_box.send_keys(cor)
        
        input_box.send_keys(Keys.ENTER)
        
        cor_url_list = driver.find_elements(By.CLASS_NAME, 'tr-hover')
        time.sleep(1)
        if len(cor_url_list) > 0:
            for url in cor_url_list:
                driver.execute_script("arguments[0].click();", url)

                number = driver.find_element(By.XPATH, '//*[@id="contents"]/table/tbody/tr[4]/td[2]')
                mail = driver.find_element(By.XPATH, '//*[@id="contents"]/table/tbody/tr[6]/td[1]')

                df2list.append([i, cor, number.text, mail.text])
                
                driver.back()
                i += 1
    except:
        save_df(df2list, './')

save_df(df2list, output_dir)





    

    