from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

class ResponsiveTester:
    def __init__(self,url,folder):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.driver.maximize_window()
        self.folder=folder 
        if "https://" not in url:
            url="https://"+url
        self.url=url    
        self.widths=[480,960,1920]
        self.height = self.driver.get_window_size()['height']
        self.height2 = self.driver.execute_script(
            """ 
        height2 = window.innerHeight
        return height2 
            """
        )
        
    def start(self):   
        self.driver.get(self.url)
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        else:
            pass
        for width in self.widths:
            self.driver.set_window_size(width,self.height)
            self.driver.execute_script("window.scrollTo(0,0)")
            time.sleep(0.5)
            scroll_height = self.driver.execute_script(
                """ 
            scroll_height = document.body.scrollHeight
            return scroll_height 
                """
            )
            scroll_numbers = scroll_height//self.height2
            for scroll_number in range(scroll_numbers+1):
                self.driver.execute_script(
                    """
                window.scrollTo(0,{}*{})
                    """.format(scroll_number,self.height2)
                )
                self.driver.save_screenshot("{}/{}x{}.png".format(self.folder,width,scroll_number))
                time.sleep(0.5)

test=ResponsiveTester("nomadcoders.co","nomad")
test.start()