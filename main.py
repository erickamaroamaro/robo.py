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

    time.sleep(4)

    driver.find_element_by_xpath('//button[text()="Tudo pronto"]').click()
    time.sleep(1)

    # closing the message popup after all done metamask screen
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    driver.find_element_by_xpath('//button[text()="Atividade"]').click()
    time.sleep(1)
    print("Wallet has been imported successfully")
    time.sleep(1)


def connectDanki():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/header/div/div[3]/div/a').click()
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[3]/div[2]/button[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    time.sleep(3)
    print('Site connected to metamask')
    print(driver.window_handles)


def getDanki():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    driver.refresh()
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/header/div/div[2]/a').click()
    time.sleep(4)
    alert = driver.switch_to.alert
    text = alert.text
    print(text)
    alert.accept()
    time.sleep(2)
    while True:
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[2]/header/div/div[2]/a').click()
        time.sleep(4)
        alert = driver.switch_to.alert
        text = alert.text
        print(text)
        time.sleep(2)
        if(text == "⭐ Confirme a Transação na Metamask para sacar seus Danki Tokens!"):
            alert.accept()
            time.sleep(3)
            driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[3]/div[2]/button[2]').click()
            time.sleep(8)
            break
        else: 
            alert.accept()

    # Sucesso
    # ⭐ Confirme a Transação na Metamask para sacar seus Danki Tokens!

    # Sucesso
    # Saque efetuado com Sucesso! Danki Tokens adicionados em sua Metamask!




def connectToWebsite():
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    time.sleep(3)
    print('Site connected to metamask')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)



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
    inputs[0].send_keys("Smart Chain")
    inputs[1].send_keys("https://bsc-dataseed.binance.org/")
    inputs[2].send_keys("56")
    inputs[3].send_keys("BNB")
    inputs[4].send_keys("https://bscscan.com")
    driver.find_element_by_xpath('//button[text()="Salvar"]').click()
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    executable_path = "./chromedriver"
# C:\Program Files\Google\Chrome\Application\chrome.exe
    chrome_options = Options()
    chrome_options.add_extension('./metamask.crx')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])

    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.get("https://app.dankicastle.io/")
    metamaskSetup("", "")
    changeMetamaskNetwork()
    connectDanki()
    getDanki()

    assert "No results found." not in driver.page_source
