from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def logar():
    user = driver.find_element_by_id("email")
    user.send_keys("")
    senha = driver.find_element_by_id("pass")
    senha.send_keys("")
    button = driver.find_element_by_id("u_0_2")
    button.click()
    # elem.clear()


if __name__ == "__main__":
    driver = webdriver.Chrome("./chromedriver")
    driver.get("http://www.fb.com/")
    logar()
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()