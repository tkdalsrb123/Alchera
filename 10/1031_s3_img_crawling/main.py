import sys
import time
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
object_link = driver.find_element(By.XPATH, '//span[@class="object-link"]').find_element(By.TAG_NAME, 'a')
link = object_link.get_attribute('href')
driver.get(link)

# get images download links
time.sleep(1)
object_list = driver.find_elements(By.XPATH, '//span[@class="object-link"]')
img_list = [object.find_element(By.TAG_NAME, 'a') for object in object_list]
img_links = [link.get_attribute('href') for link in img_list]

# download images
for img_link in img_links:
    driver.get(img_link)
    time.sleep(1)
    down_button = driver.find_element(By.XPATH, '//awsui-button[@id="object-detail-download-object-button"]')
    down_button.click()
    time.sleep(1)