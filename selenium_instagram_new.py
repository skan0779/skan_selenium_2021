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

class Instagramming:

    def __init__(self, target,max_data):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_arguement("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.target=target
        self.max_data=max_data
        self.data={}

    def wait_for(self,locator):
        # locator = (By.TAG_NAME,"header") 
        return WebDriverWait(self.driver,10).until(EC.presence_of_element_located(locator))

    def start(self):
        self.get_data("https://www.instagram.com/explore/tags/{}".format(self.target))

    def save_to_csv(self):
        f=open("{}-report.csv".format(self.target),"w")
        w=csv.writer(f)
        w.writerow(["Hashtag name","Hashtag number"])
        for item in self.data.items():
            w.writerow(item)

    def get_data(self,url):
        self.driver.get(url)
        self.wait_for((By.CLASS_NAME,"AC7dP"))
        hashtags = self.driver.find_elements_by_class_name("AC7dP")

        for hashtag in hashtags:
            hashtag_name=hashtag.text
            if not self.data[hashtag_name]:
                ActionChains(self.driver).key_down(Keys.COMMAND).click(hashtag).perform()
    
        for window in self.driver.window_handles:
            self.driver.switch_to_window(window)
            time.sleep(1)
            self.wait_for((By.TAG_NAME,"h1"))
            tag_name=self.driver.find_element_by_tag_name("h1").text[1:]
            self.wait_for((By.CLASS_NAME,"g47SY"))
            tag_number=self.driver.find_element_by_class_name("g47SY").text.replace(",","")
            if tag_name and tag_number:
                if self.data.get(tag_name)==None:
                    self.data[tag_name]=tag_number
                else: 
                    pass
        
        if len(self.data)<self.max_data:
            for window in self.driver.window_handles[0:-1]:
                self.driver.switch_to_window(window)
                self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
            self.get_data(self.driver.current_url)
        else:
            self.driver.quit()
            self.save_to_csv()


Instagramming("dog",10).start()
