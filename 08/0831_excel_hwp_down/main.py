import sys
import pandas as pd
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm, tqdm_pandas

def down_file(x):
    x = x.dropna()
    link_list = list(x.values)
    if len(link_list) > 0:
        for link in link_list:
            if ',' in link:
                link_list2 = link.split(',')
                for link in link_list2:
                    logger.info(link)
                    driver.get(link)
            else:
                logger.info(link)
                driver.get(link)

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


_, excel_dir = sys.argv

logger = make_logger('log.log')
tqdm.pandas()

LOGIN_URL = 'https://tta-kr.monday.com/auth/login_monday/email_password'
USERNAME =  'hw.chung@alcherainc.com'
PASSWORD =  'dkfcpfk123'

driver = webdriver.Chrome()
driver.get(LOGIN_URL)
time.sleep(1)
id = driver.find_element(By.XPATH, '//input[@id="user_email"]')
pw = driver.find_element(By.XPATH, '//input[@id="user_password"]')
login_button = driver.find_element(By.XPATH, '//button[@class="next-button submit_button button_cf589593a2 sizeMedium_ba8f045efd kindPrimary_2021268b9c colorPrimary_37d8c4d67a hasStyleSize_e76c5d96a2"]')

id.send_keys(USERNAME)
pw.send_keys(PASSWORD)
time.sleep(1)
login_button.click()
time.sleep(5)

df = pd.read_excel(excel_dir, header=None)
df.columns = df.loc[2]
df = df.loc[3:]
df = df.reset_index()
df = df[['품질지표기준서', '항목별 측정조건', '용역 검사기준서', '구축 및 품질관리 계획서']]
df.progress_apply(down_file, axis=1)
time.sleep(5)