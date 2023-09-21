import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import pickle
from tqdm import tqdm


_, output_dir = sys.argv

keyword_list = ['설계', '디자인', '금속', '플라스틱', '3D 프린터', '도금', '증착', 'Dicing', '공정', '인쇄', '기계', '사출', '포장재', 'CNC', '도장', '코팅', '단조', '압연', '용접']

driver = webdriver.Chrome()

for keyword in tqdm(keyword_list, desc='전체진행률'):
    page = 1
    count = 0
    corp_dict = {}
    while True:
        link = f"https://www.saramin.co.kr/zf_user/search/company?searchword={keyword}&page={page}&searchType=search&pageCount=30&mainSearch=n"
        driver.get(link)
        company_list = driver.find_elements(By.XPATH, '//a[@class="company_popup"]')
        for corp in company_list:
            corp_href = corp.get_attribute('href')
            corp_name = corp.text
            corp_dict[corp_name] = corp_href
            count += 1
        if count >= 5000 or len(company_list) == 0 :
            break
        page += 1
        
    df_list = []
    n = 1
    for corp_name, corp_href in tqdm(corp_dict.items(), desc=f'{keyword} 기업 수집중'):
        try:
            link = corp_href
            driver.get(link)
            info = driver.find_element(By.XPATH, '//dl[@class="info"]')
            info_text = info.text.split('\n')
            세부분류 = None
            지역 = None
            주소 = None
            홈페이지 = None
            for idx, t in enumerate(info_text):
                if '업종' == t:
                    세부분류 = info_text[idx+1]
                elif '홈페이지' == t:
                    홈페이지 = info_text[idx+1]
                elif '기업주소' == t:
                    주소 = info_text[idx+1]
                    지역 = 주소.split(' ')[0]

            df_list.append([n, keyword, corp_name, 세부분류, 지역, 주소, 홈페이지])
            n += 1
        except:
            pass

        df = pd.DataFrame(df_list, columns=['번호', '대분류', '회사명', '세부분류', '지역', '주소', '홈페이지'])
        df.to_excel(f'{output_dir}/corp_{keyword}_list.xlsx', index=False)

output_list = os.listdir(output_dir)

new_df = pd.DataFrame()
for file in output_list:
    file_path = os.path.join(output_dir, file)
    df = pd.read_excel(file_path)
    new_df = pd.concat([new_df, df])
    os.remove(file_path)
new_df.to_excel(f'{output_dir}/corp_merge_list.xlsx', index=False)