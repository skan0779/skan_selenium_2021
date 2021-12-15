from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 기본
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

# selector 찾기
id_input=driver.find_element_by_xpath("")
pw_input=driver.find_element_by_xpath("")
login_button=driver.find_element_by_link_text("Log in")

# input 입력
id_input.semd_keys("skan0779")
pw_input.semd_keys(input("what is your password? : "))
login_button.click()




