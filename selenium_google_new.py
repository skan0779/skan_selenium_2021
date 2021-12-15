from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class GoogleScreenshoter:

    def __init__(self,keyword,folder):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver=webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.keyword=keyword
        self.folder=folder

    def start(self):
        self.driver.get("https://google.com")   
        search_bar=self.driver.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        try:
            remove_element=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"ULSxyf"))
            )
            self.driver.execute_script(
                """
            const remove=arguements[0];
            remove.parentElement.removeChild(remove);
            """,remove_element,
            )
        except:
            pass

        results=self.driver.find_elements_by_class_name("g")
        for index,result in enumerate(results):
            result.screenshot("{}/{}x{}.png".format(self.folder,self.keyword,index))

    def close(self):
        self.driver.quit()

target=GoogleScreenshoter("python job","screenshots")
target.start()
target.close()

