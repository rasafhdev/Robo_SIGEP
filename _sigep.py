from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuração do driver para rodar em modo headless (sem interface gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Usando o webdriver_manager para gerenciar o chromedriver
service = Service(ChromeDriverManager().install())

# Substitua o caminho do chromedriver ou utilize o webdriver_manager para garantir que o driver esteja correto
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acesse a página de login
url = "https://keycloak.trt1.jus.br/auth/realms/trt1_acip/protocol/openid-connect/auth?scope=openid&state=7hkoSKoJgr6U40CP-7Dhsgg48-HxPwyHbBar_o-D2Ms.o8Z-ZlZCTsg.sigep-autoatendimento-consultainformacoesfuncionais&response_type=code&client_id=trt1&redirect_uri=https%3A%2F%2Fkeycloak.trt1.jus.br%2Fauth%2Frealms%2Ftrt1%2Fbroker%2Fkeycloak-oidc%2Fendpoint&nonce=cjQ-5_YUW1JTNGixYTXhkQ"

driver.get(url)

# Espera o site carregar (ajuste conforme necessário)
time.sleep(3)

# Insira o login e senha
username = driver.find_element(By.ID, "username")  # Altere conforme o ID do campo de login v
password = driver.find_element(By.ID, "password")  # Altere conforme o ID do campo de senha


username.send_keys("")  # Substitua pelo seu usuário
password.send_keys("")  # Substitua pela sua senha

# Submete o formulário
password.submit()

# Aguarda a página de MFA carregar (ajuste conforme necessário)
time.sleep(3)

# Verifique se a página de MFA apareceu (por exemplo, verificando a presença de um campo de código)
try:
    # Verifica se o campo de MFA (por exemplo, 'otp' ou um campo similar) existe
    mfa_field = driver.find_element(By.ID, "otp")  # Substitua pelo ID correto
    print("MFA is required!")
except:
    print("No MFA required, login successful.")
    # Caso o MFA não seja necessário, lista o conteúdo da página
    page_content = driver.page_source
    print("Page Content: ", page_content)

# Fecha o navegador
driver.quit()
