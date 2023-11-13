import sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib
import pickle
from tqdm import tqdm


def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    _, output_dir = sys.argv
    
    link = "https://www.kordi.or.kr/content.do?page=1&sf_category=N107_1&cmsId=173"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": output_dir, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    driver = webdriver.Chrome(options=options)

    num = 1
    docs = []
    while True:
        link = f"https://www.kordi.or.kr/content.do?page={num}&sf_category=N107_1&cmsId=173"
        driver.get(link)
        doc_list = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'a')
        if len(doc_list) == 0:
            break
        
        [docs.append(doc.get_attribute('href')) for doc in doc_list]
        
        num += 1
    
    save_pickle(docs, f"./oldman_doc_list.p")    
    
    pdf_list = []
    for doc_link in tqdm(docs, desc='collect pdf link'):
        try:
            driver.get(doc_link)
            pdf = driver.find_element(By.XPATH, '//*[@id="sub_contents"]/article/table/tbody/tr[4]/td').find_elements(By.TAG_NAME, 'a')
            
            [pdf_list.append(i.get_attribute('href')) for i in pdf]
        except:
            print('error doc !!!')
            print(doc_link)
    save_pickle(pdf_list, f"./oldman_href_list.p")    

    [driver.get(pdf) for pdf in tqdm(pdf_list, desc='download pdf')]
        
    os.remove(f"./oldman_doc_list.p")
    os.remove(f"./oldman_href_list.p")