from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def logar():
    user = driver.find_element_by_id("ctl00_body_tbCpfCnpj")
    user.send_keys("32.778.935/0001-90")
    senha = driver.find_element_by_id("ctl00_body_tbSenha")
    senha.send_keys("")
    button = driver.find_element_by_id("ctl00_body_btEntrar")
    button.click()
    #tratar o captcha da imagem

    # elem.clear()


if __name__ == "__main__":
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://nfe.prefeitura.sp.gov.br/login.aspx")
    logar()
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()