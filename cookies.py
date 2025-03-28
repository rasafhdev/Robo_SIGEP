from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configura o driver do Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acessa o site
    driver.get("https://keycloak.trt1.jus.br/auth/realms/trt1_acip/protocol/openid-connect/auth?scope=openid&state=7hkoSKoJgr6U40CP-7Dhsgg48-HxPwyHbBar_o-D2Ms.o8Z-ZlZCTsg.sigep-autoatendimento-consultainformacoesfuncionais&response_type=code&client_id=trt1&redirect_uri=https%3A%2F%2Fkeycloak.trt1.jus.br%2Fauth%2Frealms%2Ftrt1%2Fbroker%2Fkeycloak-oidc%2Fendpoint&nonce=cjQ-5_YUW1JTNGixYTXhkQ")
    time.sleep(3)  # Espera o site carregar

    # Obtém todos os cookies
    cookies = driver.get_cookies()
    print("Cookies antes de adicionar novo cookie:")
    for cookie in cookies:
        print(cookie)

finally:
    # Fecha o navegador
    driver.quit()