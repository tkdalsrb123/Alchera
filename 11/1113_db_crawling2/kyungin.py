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

def get_src_link():
    try:
        img_list = driver.find_element(By.XPATH, '//div[@class="gallery_list_01 mg_t8 info_gallery"]').find_elements(By.XPATH, '//div[@class="gl_thumb"]')
        for img in img_list:
            i = img.find_element(By.TAG_NAME, 'img')
            src_list.append(i.get_attribute('src'))
    except:
        print(link)

if __name__ == '__main__':
    _, output_dir = sys.argv
    link = "https://kostat.go.kr/gallery.es?mid=a30306000000&bid=11945&ref_bid="
    driver = webdriver.Chrome()
    driver.get(link)

    src_list = []
    
    
    pagination = driver.find_element(By.XPATH, '//div[@class="paging mg_t24"]').find_elements(By.TAG_NAME, 'a')
    get_src_link()
    pagination[0].click()
    get_src_link()

    save_pickle(src_list, f"./kyungin_src_list.p")
    
    i = 1
    for src_alt in tqdm(src_list, desc='down img'):
        output_img_path = os.path.join(output_dir, f"{i}.jpg")
        urllib.request.urlretrieve(src_alt, output_img_path)
        i += 1

    driver.close()
    
    os.remove(f"./kostat_src_list.p")