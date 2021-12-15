from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
folder="screenshots"

driver.get("https://nomadcoders.co")
driver.maximize_window()
height=driver.get_window_size()['height']
height2 = driver.execute_script(
    """ 
height2 = window.innerHeight
return height2 
    """
)
widths=[480,960,1920]


for width in widths:
    driver.set_window_size(width,height)
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(1)
    scroll_height = driver.execute_script(
        """ 
    scroll_height = document.body.scrollHeight
    return scroll_height 
        """
    )
    scroll_numbers = scroll_height//height2
    # scrollTo(0,0)인 header부분도 찍으려면 + 1 = 0 ~ n
    for scroll_number in range(scroll_numbers+1):
        driver.execute_script(
            """
        window.scrollTo(0,{}*{})
            """.format(scroll_number,height2)
        )
        driver.save_screenshot("{}/{}x{}.png".format(folder,width,scroll_number))
        time.sleep(1)