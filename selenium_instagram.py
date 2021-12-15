from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import csv


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

data={}
max_data=10

def wait_for(locator):
    # locator = (By.TAG_NAME,"header") 
    # 특정 element가 나올때까지 기다리는 기능
    return WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

def get_data(url):
    driver.get(url)
    # wait_for((By.TAG_NAME,"header"))
    # header = driver.find_element_by_tag_name("header")
    wait_for((By.CLASS_NAME,"AC7dP"))
    hashtags = driver.find_elements_by_class_name("AC7dP")

    for hashtag in hashtags:
        hashtag_name=hashtag.text
        if not data[hashtag_name]:
            # 각 hashtag 눌러서 새로운 창 열기
            ActionChains(driver).key_down(Keys.COMMAND).click(hashtag).perform()
 
    for window in driver.window_handles:
        # 각 hashtag 창으로 이동
        driver.switch_to_window(window)
        time.sleep(1)
        wait_for((By.TAG_NAME,"h1"))
        tag_name=driver.find_element_by_tag_name("h1").text[1:]
        wait_for((By.CLASS_NAME,"g47SY"))
        tag_number=driver.find_element_by_class_name("g47SY").text.replace(",","")
        if tag_name and tag_number:
            if data.get(tag_name)==None:
                data[tag_name]=tag_number
            else: 
                pass
    
    if len(data)<max_data:
        for window in driver.window_handles[0:-1]:
            # 마지막 창 빼고 전부 닫기
            driver.switch_to_window(window)
            # 현재 창 닫고 다음 창으로 이동
            driver.close()
        # 반복
        driver.switch_to_window(driver.window_handles[0])
        get_data(driver.current_url)

target = "dog"
get_data("https://www.instagram.com/explore/tags/{}".format(target))


f=open("{}-repor.csv".format(target),"w")
w=csv.writer(f)
w.writerow(["Hashtag name","Hashtag number"])
for item in data.items():
    w.writerow(item)

driver.quit()
