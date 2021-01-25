# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import chrome
#
#
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options)
#
#
#
# driver.get("https://google.com")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Firefox(options=chrome_options)
driver.get("http://www.linkedin.com/uas/login")
username = ""
password = ""
elementID = driver.find_element_by_id("username")
elementID.send_keys(username)
elementID = driver.find_element_by_id("password")
elementID.send_keys(password)
elementID.submit()

visitingProfileId = "/in/ruslan-skira/"
fullink = "https://www.linkedin.com" + visitingProfileId
driver.get(fullink)
# driver.close()
