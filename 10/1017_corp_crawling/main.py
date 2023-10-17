import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import pickle
import numpy as np
from tqdm import tqdm

def makePickle(data, dir):
    with open(dir, 'wb') as f:
        pickle.dump(data, f)
        
def readPickle(dir):
    with open(dir, 'rb') as f:
        data = pickle.load(f)
    return data

if __name__ == '__main__':
    _, csv_dir, output_dir = sys.argv

    df = pd.read_csv(csv_dir, encoding='euc-kr')

    search_list = []
    for i in range(df.shape[0]):
        if df.loc[i, '항목'] is not np.NaN:
            category = df.loc[i, '항목']
        no = df.loc[i, 'No.']
        keyword = df.loc[i, '키워드']
        search_list.append([category, no, keyword])
        
        
    driver = webdriver.Chrome()
    for search_info in tqdm(search_list[:2], desc='기업리스트 수집중'):
        category = search_info[0]
        no = search_info[1]
        keyword = search_info[2]
        i = 1
        corp_list = set([])
        while True:
            link = f'https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}&show_applied=&except_read=&ai_head_hunting=&recruitPage={i}&recruitSort=relation&recruitPageCount=40&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&quick_apply='
            
            driver.get(link)
            
            if len(driver.find_elements(By.CLASS_NAME, 'info_no_result')) > 0:
                break
            
            corp_name = driver.find_element(By.CLASS_NAME, 'content').find_elements(By.CLASS_NAME, 'corp_name')
            [corp_list.add(name.find_element(By.TAG_NAME, 'a').get_attribute('href')) for name in corp_name]
            
            if len(corp_list) > 2000:
                break

            i += 1
        
        output_info = [category, no, keyword, corp_list]
        pickle_folder = os.path.join(output_dir, 'pickle_folder')
        os.makedirs(pickle_folder, exist_ok=True)
        output_pickle = os.path.join(pickle_folder, f"{keyword}_data.p")
        makePickle(output_info, output_pickle)


    pickle_list = [os.path.join(pickle_folder, i) for i in os.listdir(pickle_folder)]
    list2df = []
    for pickle_path in tqdm(pickle_list, desc='기업정보 수집중', position=0):
        data = readPickle(pickle_path)
        
        category = data[0]
        no = data[1]
        keyowrd = data[2]
        for corp_link in tqdm(data[3], desc=f'{keyword}', position=1):
            driver.get(corp_link)
            try:
                h1 = driver.find_element(By.TAG_NAME, 'h1')
                corp_name = h1.find_element(By.CLASS_NAME, 'name').text
                summary = driver.find_element(By.CLASS_NAME, 'summary')
                li = summary.find_elements(By.TAG_NAME, 'li')
                info = driver.find_element(By.CLASS_NAME, 'info')
                info_text = info.text.split('\n')
                corp_type = None
                homepage = None
                for l in li:
                    if '기업형태' in l.text.split('\n'):
                        corp_type = l.text.split('\n')[0]
                for idx, i in enumerate(info_text):
                    if '홈페이지' == i:
                        homepage = info_text[idx+1]
            except:
                print(corp_link)
                
            list2df.append([category, no, keyword, corp_name, corp_type, homepage])

        os.remove(pickle_path)
        
    df = pd.DataFrame(list2df, columns=['항목', 'No.', '키워드', '기업명', '기업 형태', '홈페이지 주소'])
    df.to_excel(f'{output_dir}/corp_list.xlsx', index=False)
