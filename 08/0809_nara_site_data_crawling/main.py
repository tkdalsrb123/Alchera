import pandas as pd
import time
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

def request_url(cat):
    '''returns url for a  category'''
    d = datetime.date.today()
    fromtd = d - timedelta(days=14)
    start_date = str(fromtd.strftime("%Y/%m/%d"))
    end_date = str(d.strftime("%Y/%m/%d"))
    fromBidDt = requests.utils.quote(start_date, safe='')
    toBidDt = requests.utils.quote(end_date, safe='')
    bidNm = requests.utils.quote(cat.encode('euc-kr'))
    url = f"https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?searchType=1&bidSearchType=1&taskClCds=&bidNm=&searchDtType=1&fromBidDt={fromBidDt}&toBidDt={toBidDt}&setMonth1=3&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&instSearchRangeType=&refNo=&area=&areaNm=&strArea=&orgArea=&industry=&industryCd=&upBudget=&downBudget=&budgetCompare=&detailPrdnmNo=&detailPrdnm=&procmntReqNo=&intbidYn=&regYn=Y&recordCountPerPage=30"

    return url

# def scrape_cat(cat):
#     '''searches for each category'''
#     cat_url = request_url(cat)
#     df = pd.read_html(cat_url)[0]
#     df['search_term']=cat
    
    return df
# df = pd.read_csv(r"C:\Users\Alchera115\wj.alchera\Alchera_data\08\0809_nara_site_data_crawling\keyword.csv", encoding='cp949')
# print(df)
url = request_url('인공지능')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
tbody = soup.find('tbody')
tr = tbody.find_all('tr')
div = tr[0].find_all('td' > 'div')
for i in div:
    # if ['class'] not in i.attrs.values():
    if 'class':
        print(i.text)
    if i.name == 'a':
        print(i.get('href'))
    
# df = pd.read_html(url)[0]
# print(df['공고명'])

# response = urlopen(url)
# soup = BeautifulSoup.get(response, 'html.parser')

# print(soup)