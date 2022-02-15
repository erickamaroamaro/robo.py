from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def metamaskSetup(recoveryPhrase, password):
    driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_xpath('//button[text()="Comece agora"]').click()
    driver.find_element_by_xpath('//button[text()="Importar carteira"]').click()
    driver.find_element_by_xpath('//button[text()="Não, agradeço"]').click()

    time.sleep(5)

    inputs = driver.find_elements_by_xpath('//input')
    inputs[0].send_keys(recoveryPhrase)
    inputs[1].send_keys(password)
    inputs[2].send_keys(password)
    driver.find_element_by_css_selector('.first-time-flow__terms').click()
    driver.find_element_by_xpath('//button[text()="Importar"]').click()

    time.sleep(5)

    driver.find_element_by_xpath('//button[text()="Tudo pronto"]').click()
    time.sleep(2)

    # closing the message popup after all done metamask screen
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    time.sleep(2)
    print("Wallet has been imported successfully")
    time.sleep(10)


if __name__ == "__main__":
    driver = webdriver.Chrome()

    executable_path = "./chromedriver"

    chrome_options = Options()
    chrome_options.add_extension('./metamask.crx')

    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.get("https://www.google.com.br/")
    metamaskSetup()
    # logar()
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
