from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'

def metamaskSetup(recoveryPhrase, password):
    driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_xpath('//button[text()="Comece agora"]').click()
    driver.find_element_by_xpath('//button[text()="Importar carteira"]').click()
    driver.find_element_by_xpath('//button[text()="Não, agradeço"]').click()

    time.sleep(1)

    inputs = driver.find_elements_by_xpath('//input')
    inputs[0].send_keys(recoveryPhrase)
    inputs[1].send_keys(password)
    inputs[2].send_keys(password)
    driver.find_element_by_css_selector('.first-time-flow__terms').click()
    driver.find_element_by_xpath('//button[text()="Importar"]').click()

    time.sleep(2)

    driver.find_element_by_xpath('//button[text()="Tudo pronto"]').click()
    time.sleep(1)

    # closing the message popup after all done metamask screen
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    driver.find_element_by_xpath('//button[text()="Atividade"]').click()
    time.sleep(1)
    print("Wallet has been imported successfully")
    time.sleep(1)


def rentHorse():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    flag = True

    
    try:
        while flag is True: 
            driver.find_element_by_css_selector('.button-game-content').click()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            driver.find_element_by_xpath('//button[text()="Rent"]').click()
        else:
            driver.find_element_by_xpath('//button[text()="Compona"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//button[text()="Haz"]').click()
    except Exception as e:
            socket.send("::".join(['FATALERROR', e.__class__.__name__, e.message]))


def changeMetamaskNetwork():
    # opening network
    print("Changing network")
    driver.switch_to.window(driver.window_handles[0])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(1) 
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div').click()
    driver.find_element_by_xpath('//button[text()="Adicionar rede"]').click()
    time.sleep(2)
    print("opening network dropdown")
    inputs = driver.find_elements_by_xpath('//input')
    inputs[0].send_keys("Polygon")
    inputs[1].send_keys("https://polygon-rpc.com")
    inputs[2].send_keys("137")
    inputs[3].send_keys("MATIC")
    inputs[4].send_keys("https://polygonscan.com/")
    driver.find_element_by_xpath('//button[text()="Salvar"]').click()
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def loginGoogle():
    driver.execute_script('''window.open("https://accounts.google.com/servicelogin","_blank");''')
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)
    search_form = driver.find_element_by_id("identifierId")
    search_form.send_keys('email')
    driver.find_element_by_css_selector('.VfPpkd-vQzf8d').click()
    nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
    nextButton[0].click() 
    search_form.send_keys('senha')
    nextButton[0].click() 

if __name__ == "__main__":
    driver = webdriver.Chrome()
    executable_path = "./chromedriver"

    chrome_options = Options()
    chrome_options.add_extension('./metamask.crx')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])

    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.get("https://play.pegaxy.io/renting?tab=share-profit&bloodLine=Hoz")
    metamaskSetup("seed phrase", "senha")
    changeMetamaskNetwork()
    loginGoogle()
    # rentHorse()

    # logar()
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
