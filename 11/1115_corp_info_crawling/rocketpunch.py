import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time

def login(driver, id, pw):
    input_id = driver.find_element(By.XPATH, '//input[@name="email"]')
    input_pw = driver.find_element(By.XPATH, '//input[@name="password"]')
    input_id.send_keys(id)
    input_pw.send_keys(pw)
    input_pw.send_keys(Keys.RETURN)

def get_company_names(path):
    company_names = []
    df = pd.read_csv(path, encoding='euc-kr')
    df.apply(lambda x: company_names.append((x['분야'], x['회사명'])), axis=1)

    return company_names

def crawling(key_path, output_path):
    LINK = "https://www.rocketpunch.com/login"
    USERID = 'joohyunghan1104@gmail.com'
    USERPW = 'qhrtlf123'
    
    keyword_list = get_company_names(key_path)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 3)
    driver.get(LINK)
    
    login(driver, USERID, USERPW)
    time.sleep(5)
    
    info_list = []
    for keyword in tqdm(keyword_list):
        keyword = keyword[1].replace('(주)','').replace('주식회사', '')
        keyword = keyword.strip()
        try:
            COMPANY_LINK = f"https://www.rocketpunch.com/companies?keywords={keyword}"
            driver.get(COMPANY_LINK)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="company item"]')))
            company_item = driver.find_elements(By.XPATH, '//div[@class="company item"]')
            if company_item:
                company = company_item[0]
                company.click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ui company info items"]')))
                company_info = driver.find_element(By.XPATH, '//div[@class="ui company info items"]')
                item = company_info.find_elements(By.CLASS_NAME, 'item')
                info_dict = {'기업명':keyword}
                for i in item:
                    try:
                        a = i.find_element(By.CLASS_NAME, 'title').text
                        b = i.find_element(By.CLASS_NAME, 'content').text
                        info_dict[a] = b
                    except:
                        pass
                
                info_list.append(info_dict)
            
            else:
                pass
        except:
            print(COMPANY_LINK)
    
    df = pd.DataFrame.from_dict(info_list)
    df.to_excel(f"{output_path}/rocket_file.xlsx", index=False)

if __name__ == "__main__":
    _, csv_path, output_dir = sys.argv
    print('---------collecting company info--------')
    crawling(csv_path, output_dir)
    print('----------------Done!--------------------')