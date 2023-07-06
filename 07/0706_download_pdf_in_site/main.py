import requests
import pandas as pd
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def download_pdf(url, file_name, headers):
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
    else:
        print(response.status_code)
    

# def url():
#     시황정보_리포트 = "https://finance.naver.com/research/market_info_list.naver"
#     투자정보_리포트 = "https://finance.naver.com/research/invest_list.naver"
#     종목분석_리포트 = "https://finance.naver.com/research/company_list.naver"
#     산업분석_리포트 = "https://finance.naver.com/research/industry_list.naver"
#     경제분석_리포트 = "https://finance.naver.com/research/economy_list.naver"
#     채권분석_리포트 = "https://finance.naver.com/research/debenture_list.naver"
    
# _, excel_dir, save_dir = sys.argv

url = "https://finance.naver.com/research/debenture_list.naver"


response = urlopen(url)

soup = BeautifulSoup(response, 'html.parser')
# for i in soup.find_all('td', {'class':'date'}):
#     print(i)

# value =  soup.find('td', {'class':'date'})

# print(value)