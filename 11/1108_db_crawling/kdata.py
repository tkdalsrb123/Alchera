import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from tqdm import tqdm


def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    _, = sys.argv
    

    driver = webdriver.Chrome()
    
    pdf_link_list = []
    i = 1
    while True:
        link = f"https://www.kdata.or.kr/kr/board/info_01/boardList.do?pageIndex={i}&bbsIdx=&searchCondition=all&searchKeyword="
        driver.get(link)
        
        url_list = driver.find_element(By.XPATH, '//ul[@class="bbs_list"]').find_elements(By.TAG_NAME, 'a')
        if len(url_list) == 0:
            break
        for url in url_list:
            url.click()
            try:
                pdf_path = driver.find_element(By.XPATH, '//div[@class="down_box"]').find_element(By.TAG_NAME, 'a')
                pdf_link = pdf_path.get_attribute('href')
                pdf_link_list.append(pdf_link)
            except:
                print(link)
            driver.back()
            
        i += 1
        
    save_pickle(pdf_link_list, f"./kdata_pdf_list.p")
    
    for pdf in tqdm(pdf_link_list, desc='down pdf'):
        driver.get(pdf)