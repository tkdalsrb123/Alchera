import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

_, bucket_name = sys.argv

LOGIN_URL = 'https://s3.console.aws.amazon.com/s3/buckets/alchera-label-socket?region=ap-northeast-2&tab=objects'
USERID =  'baithings'
USERNAME = 's3_worker'
PASSWORD =  '78ryL8#q'
BUCKET = bucket_name

driver = webdriver.Chrome()
driver.get(LOGIN_URL)

IAM_button = driver.find_element(By.XPATH, "//input[@id='iam_user_radio_button']")
IAM_button.click()

# login s3
id = driver.find_element(By.XPATH, "//input[@id='resolving_input']")
next_button = driver.find_element(By.XPATH, "//button[@id='next_button']")
id.send_keys(USERID)
next_button.click()
name = driver.find_element(By.XPATH, "//input[@id='username']")
pw = driver.find_element(By.XPATH, "//input[@id='password']")
name.send_keys(USERNAME)
pw.send_keys(PASSWORD)
pw.send_keys(Keys.RETURN)

# get bucket link
time.sleep(3)
bucket_input = driver.find_element(By.XPATH, '//input[@id="polaris-table-formfield-filter"]')
bucket_input.send_keys(BUCKET)
bucket_input.send_keys(Keys.RETURN)
time.sleep(1)
object_links_list = []
while True:
    page_next_button = driver.find_element(By.XPATH, '//button[@aria-label="다음 페이지"]') 
    object_links = driver.find_element(By.XPATH, '//span[@class="object-link"]').find_elements(By.XPATH, '//span[@class="name folder latest object-name"]')
    [object_links_list.append(obj_link.text) for obj_link in object_links]
    
    if page_next_button.is_enabled() == True:
        page_next_button.click()
    elif page_next_button.is_enabled() == False:
        break

df = pd.DataFrame(object_links_list, columns=['S3 버킷'])
df.to_excel('./s3_file_list.xlsx', index=False)