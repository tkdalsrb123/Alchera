import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from tqdm import tqdm

def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def get_pdf_link():
    try:
        pdf_link_list = driver.find_element(By.XPATH, '//div[@class="board_list_01 mg_t8"]').find_elements(By.CLASS_NAME, 'bf_pdf')
        for link in pdf_link_list:
            pdf = link.get_attribute('href')
            pdf_list.append(pdf)
    except:
        print(link)

if __name__ == '__main__':
    _, = sys.argv
    link = "https://kostat.go.kr/board.es?mid=a10301010000&bid=a103010100&ref_bid=203,204,205,206,207,210,211,11109,11113,11814,213,215,214,11860,11695,216,218,219,220,10820,11815,11895,11816,208,245,222,223,225,226,227,228,229,230,11321,232,233,234,12029,10920,11469,11470,11817,236,237,11471,238,240,241,11865,243,244,11893,11898,12031,11825,246"

    driver = webdriver.Chrome()
    driver.get(link)

    pdf_list = []
    while True:
        page_len = len(driver.find_element(By.XPATH, '//div[@class="paging mg_t24"]').find_elements(By.TAG_NAME, 'a'))
        if page_len > 11:
            for i in range(2, 12):
                pagination = driver.find_element(By.XPATH, '//div[@class="paging mg_t24"]').find_elements(By.TAG_NAME, 'a')
                get_pdf_link()
                pagination[i].click()
                
        elif page_len == 11:
            for i in range(10):
                pagination = driver.find_element(By.XPATH, '//div[@class="paging mg_t24"]').find_elements(By.TAG_NAME, 'a')
                get_pdf_link()
                pagination[i].click()

        elif page_len < 11:
            break
    
    save_pickle(pdf_list, f"./kostat_pdf_list.p")
    
    for pdf in tqdm(pdf_list, desc='down pdf'):
        driver.get(pdf)