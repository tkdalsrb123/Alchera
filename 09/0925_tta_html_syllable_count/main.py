import pandas as pd
import os, sys
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

def readfiles(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.html':
                file_path = os.path.join(root, file)

                file_list.append(file_path)
            
    return file_list

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

html_list = readfiles(input_dir)

list2df = []
for html in tqdm(html_list):
    root, file = os.path.split(html)
    logger.info(html)
    page = open(html, 'rt', encoding='utf-8').read()

    soup = bs(page, 'html.parser')

    td_list = soup.find_all('td')

    td_count = 0
    for td in td_list:
        td_text = td.get_text().replace(' ', '')
        td_count += len(td_text)


    list2df.append([file, td_count])

df = pd.DataFrame(list2df, columns=['파일명', 'count'])
df.to_excel(f'{output_dir}/html_count.xlsx', index=False)
