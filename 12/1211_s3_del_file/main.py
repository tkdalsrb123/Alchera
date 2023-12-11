import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def login(login_url, ID, NAME, PW):
    driver.get(login_url)
    IAM_button = driver.find_element(By.XPATH, "//input[@id='iam_user_radio_button']")
    IAM_button.click()
    id = driver.find_element(By.XPATH, "//input[@id='resolving_input']")
    next_button = driver.find_element(By.XPATH, "//button[@id='next_button']")
    id.send_keys(ID)
    next_button.click()
    name = driver.find_element(By.XPATH, "//input[@id='username']")
    pw = driver.find_element(By.XPATH, "//input[@id='password']")
    name.send_keys(NAME)
    pw.send_keys(PW)
    pw.send_keys(Keys.RETURN)

if __name__ == "__main__":
    _, excel_dir = sys.argv

    LOGIN_URL = 'https://s3.console.aws.amazon.com/s3/buckets/alchera-label-socket?region=ap-northeast-2&tab=objects'
    URL = 'https://s3.console.aws.amazon.com/s3/buckets/alchera-label-socket?region=ap-northeast-2&tab=objects'
    USERID =  'baithings'
    USERNAME = 's3_worker'
    PASSWORD =  '78ryL8#q'
    
    df = pd.read_excel(excel_dir)
    del_list = df['del_list'].values
    
    driver = webdriver.Chrome()
    
    # login s3
    login(LOGIN_URL, USERID, USERNAME, PASSWORD)

    output_list = []
    for del_name in del_list:
        # get bucket link
        time.sleep(3)
        bucket_input = driver.find_element(By.XPATH, '//input[@id="polaris-table-formfield-filter"]')
        bucket_input.send_keys(del_name)
        bucket_input.send_keys(Keys.RETURN)
        time.sleep(1)
        check = driver.find_element(By.XPATH, '//span[@class="awsui_control_1wepg_12w0t_151 awsui_checkbox-control_k2y2q_10kux_107"]')
        del_button = driver.find_element(By.XPATH, '//button[@data-testid="delete-objects-button"]')
        check.click()
        if del_button.is_enabled():
            del_button.click()
            time.sleep(1)
            del_input = driver.find_element(By.XPATH, '//input[@class="awsui_input_2rhyz_7lwtk_97"]')
            del_input.send_keys('삭제')
            real_del_button = driver.find_element(By.XPATH, '//awsui-button[@class="delete-objects__actions-submit"]')
            real_del_button.click()
            time.sleep(1)
        else:
            output_list.append(del_name)
        driver.get(URL)
            
       
    df = pd.DataFrame(output_list, columns=['bucket'])
    df.to_csv('./output.csv', index=False)