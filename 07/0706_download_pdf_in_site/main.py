import requests
import pandas as pd
import sys, os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def select_url(report):
    if report == '시황정보 리포트':
        url = "https://finance.naver.com/research/market_info_list.naver?"
    elif report == '투자정보 리포트':
        url = "https://finance.naver.com/research/invest_list.naver?"
    elif report == '종목분석 리포트':
        url = "https://finance.naver.com/research/company_list.naver?"
    elif report == '산업분석 리포트':
        url = "https://finance.naver.com/research/industry_list.naver?"
    elif report == '경제분석 리포트':
        url = "https://finance.naver.com/research/economy_list.naver?"
    elif report == '채권분석 리포트':
        url = "https://finance.naver.com/research/debenture_list.naver?"

    return url
    
_, excel_dir, save_dir, page = sys.argv

excel = pd.read_excel(excel_dir)

for i in range(excel.shape[0]):
    category = excel.iloc[i]['분야']
    excel_date = excel.iloc[i]['날짜']

    folder = os.path.join(save_dir, category)
    os.makedirs(folder, exist_ok=True)
    
    pdf_list = []
    date_list = []
    url = select_url(category)

    concat_df = pd.DataFrame(columns=['pdf_link', 'date'])
    for j in range(1, int(page)+1):
        url = f'{url}&page={j}'
        print(category, 'pdf 수집!!', url)
        response = urlopen(url)

        soup = BeautifulSoup(response, 'html.parser')

        table = soup.find('table')
        
        # pdf 링크 추출
        for pdf_link in table.find_all('td', {'class':'file'}):
            pdf_list.append(pdf_link.find('a').get('href'))
        # 작성일 추출
        for date in table.find_all('td', {'style':'padding-left:5px'}):
            date_list.append(date.text)

        table_list = [pdf_list, date_list]
        # 페이지 수만큼 데이터프레임 만들어서 concat
        table_df = pd.DataFrame(table_list).transpose()
        table_df.columns = ['pdf_link', 'date']
        concat_df = pd.concat([concat_df, table_df])

    # excel에 날짜별 데이터프레임 추출
    df = concat_df[concat_df['date'] == excel_date]

    # pdf down
    for idx in range(df.shape[0]):
        pdf = df.iloc[idx]['pdf_link']
        pdf_name = pdf.split('/')[-1]
    
        response = requests.get(pdf)
        
        down_path = os.path.join(folder, pdf_name)
        pdf_file = open(down_path, 'wb')
        pdf_file.write(response.content)
        pdf_file.close()
        print(down_path, 'downloaded')
