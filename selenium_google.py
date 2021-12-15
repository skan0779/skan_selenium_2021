from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 1. 기본방법
# browser=webdriver.Chrome(ChromeDriverManager().install())
# browser.get("https://google.com")

# 1. 창 자동닫힘 해결버전
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

# 2. 구글 검색
KEYWORD="buy domain"
browser.get("https://google.com")
search_bar=browser.find_element_by_class_name("gLFyf")
search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)

# 3. JavaScript element load 대기
remove_element=WebDriverWait(browser,10).until(EC,EC.presence_of_element_located((By.CLASS_NAME,"ULSxyf")))

# 4. JavaScript console 제거할 인자 보내기
browser.execute_script(
    """
const remove=arguements[0];
remove.parentElement.removeChild(remove);
""",remove_element,
)

# 5. Screenshot 
results=browser.find_elements_by_class_name("g")
for index,result in enumerate(results):
    result.screenshot("screenshots/{}x{}.png".format(KEYWORD,index))

browser.quit()

