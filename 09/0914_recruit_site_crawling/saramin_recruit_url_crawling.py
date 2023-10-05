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
    with open(dir, 'wb') as f:
        pickle.dump(data, f)



_, excel_path, output_dir = sys.argv

root, file = os.path.split(excel_path)
filename, ext = os.path.splitext(file)
filename = filename.split('_')[1]

df = pd.read_excel(excel_path)
keyword_list = list(df['키워드'].values)

driver = webdriver.Chrome()
recruit_dict = {}
recruit_href_list = []
for keyword in keyword_list:
    page = 1
    while True:
        link = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&keydownAccess=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&searchword={keyword}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitPage={page}&recruitSort=relation&recruitPageCount=40&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting=&mainSearch=n"
        driver.get(link)

        recruit_url = driver.find_elements(By.XPATH, '//*[@id="recruit_info_list"]/div[1]/div/div[2]/h2/a')
        if len(recruit_url) < 1:
            break
        
        for url in recruit_url:
            href = url.get_attribute('href')
            if href:
                recruit_href_list.append(href)
   
        page += 1
    
        recruit_dict[keyword] = recruit_href_list

makePickle(recruit_dict, f"{output_dir}/saramin_{filename}.p")