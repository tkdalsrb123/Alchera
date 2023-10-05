import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup as bs4
import pickle
from tqdm import tqdm

def readPickle(dir):
    with open(dir, 'rb') as f:
        data = pickle.load(f)
    
    return data

def readfiles(dir):
    file_dict = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.p':
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path

    return file_dict

def makePickle(data, dir):
    with open(dir, 'wb') as f:
        pickle.dump(data, f)
        
def preprocessing(text):
    if type(text) == str:
        text = text.replace(' ', '').replace('\n', '')
        
    return text

def makeinfo(link, keyword):
    driver.get(link)
    html = driver.page_source
    soup = bs4(html, 'html.parser')
    jv_cont = soup.find_all('div', attrs={'class':'jv_cont jv_howto'})
    담당자 = None
    연락처 = None
    try:
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
            
            기업형태 = preprocessing(기업형태)
            업종 = preprocessing(업종)
            매출액 = preprocessing(매출액)
            홈페이지 = preprocessing(홈페이지)
            
            df2list.append(['사람인', keyword, 기업명, 기업형태, 매출액, 담당자, 연락처, 홈페이지, 업종])
    except:
        error_list.append(link)
    
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv

    pickle_dict = readfiles(input_dir)

    driver = webdriver.Chrome()
    df2list = []
    error_list = []

    for filename, pickle_path in tqdm(pickle_dict.items(), desc='pickle', position=0):
        pickle_file = readPickle(pickle_path)

        for keword, link_list in tqdm(pickle_file.items(), desc='recruit', position=1):
            [makeinfo(link, keword) for link in link_list]

    df = pd.DataFrame(df2list, columns=['인입경로', '키워드', '기업명', '기업형태', '매출액', '담당자', '전화', '홈페이지', '업종'])
    df.to_excel(f'{output_dir}/saramin_채용정보.xlsx', index=False)

    error_df = pd.DataFrame(error_list, columns=['error_link'])
    error_df.to_excel('./error_list.xlsx', index=False)

