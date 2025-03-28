from scrappings import ScrappingGmail 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dataclasses import dataclass
import dotenv
import os

dotenv.load_dotenv()

@dataclass
class Sigep:
    USERNAME_SIGEP: str
    PASSWORD_SIGEP: str
    URL_SIGEP: str
    EMAIL: str
    EMAIL_PASSWORD: str
    IMAP_SERVER: str

    def setup_driver(self):
        """Configura o WebDriver do Chrome para rodar sem interface gráfica."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument(
            "--enable-features=CookiesWithoutSameSiteMustBeSecure"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        """Abre a página inicial do Sigep."""
        self.setup_driver()
        self.driver.get(self.URL_SIGEP)
        
    def selecionar_orgao(self, orgao_nome):
        """Seleciona o órgão desejado e clica no botão OK."""
        wait = WebDriverWait(self.driver, 10)

        # Clicar no formulario de seleção do órgão para abrir as opções
        selecionar_elemento = wait.until(
            EC.element_to_be_clickable((By.ID, "formTribunal_nome"))
        )
        selecionar_elemento.click()
        time.sleep(1)

        # Selecionar a opção desejada pelo texto visível
        opcao_desejada = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,f"//span[contains(text(), '{orgao_nome}')]")
            )
        )
        opcao_desejada.click()
        time.sleep(1)

        # Aguardar ativação e clicar no botão "OK"
        btn_ok = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-ok"))
        )
        btn_ok.click()

        # Clicar no botão de acesso
        btn_especial = wait.until(
            EC.element_to_be_clickable((By.ID, "social-keycloak-oidc"))
        )
        btn_especial.click()

        # Preencher credenciais
        username_sigep = self.driver.find_element(By.ID, "username")
        password_sigep = self.driver.find_element(By.ID, "password")
        username_sigep.send_keys(self.USERNAME_SIGEP)
        password_sigep.send_keys(self.PASSWORD_SIGEP)
        password_sigep.submit()

        # Verifica se o campo de MFA aparece
        try:
            mfa_field = self.driver.find_element(By.ID, "code")
            print("MFA is required!")

            # Captura o código MFA via ScrappingGmail
            email_account = ScrappingGmail(
                EMAIL=self.EMAIL,
                EMAIL_PASSWORD=self.EMAIL_PASSWORD,
                IMAP_SERVER=self.IMAP_SERVER
            )

            if email_account.auth_email():
                time.sleep(5)
                email_account.list_messages(
                    sender=os.getenv("SENDER", ''),
                    subject=os.getenv("SUBJECT", ''),
                    qty=1
                )
                email_account.logout()

            mfa_code = email_account.MFA_CODE
            mfa_field.send_keys(mfa_code)
            mfa_field.submit()
            print(f"MFA Code '{mfa_code}' submitted.")

        except:
            print("No MFA required, login successful.")

    def selecionar_sistema(self, sistema_nome):
        """Seleciona o sistema desejado pelo nome na página."""
        wait = WebDriverWait(self.driver, 10)
        
        sistema_element = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//img[@alt='{sistema_nome}']"
        )))
        
        sistema_element.find_element(By.XPATH, "./ancestor::app-painel-item").click()

    def selecionar_autoatendimento(self):
        """Seleciona o módulo Autoatendimento."""
        wait = WebDriverWait(self.driver, 10)
        
        autoatendimento_element = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//h1[contains(text(), 'Autoatendimento')]"))
        )
        
        autoatendimento_element.find_element(By.XPATH, "./ancestor::app-painel-item").click()
        print("Autoatendimento selecionado!")
        

    def selecionar_consulta_informacoes_funcionais(self):
        """Seleciona a opção 'Consulta de Informações Funcionais' no Autoatendimento."""
        wait = WebDriverWait(self.driver, 10)

        consulta_element = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//h1[contains(text(), 'Consulta de Informações Funcionais')]"
        )))

        consulta_element.find_element(By.XPATH, "./ancestor::app-painel-item").click()
        print("Consulta de Informações Funcionais selecionada!")
        
        


if __name__ == "__main__":
    sigep = Sigep(
        USERNAME_SIGEP=os.getenv("USERNAME_SIGEP", ""),
        PASSWORD_SIGEP=os.getenv("PASSWORD_SIGEP", ""),
        URL_SIGEP=os.getenv("URL_SIGEP", ""),
        EMAIL=os.getenv("EMAIL", ""),
        EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD_APP", ""),
        IMAP_SERVER=os.getenv("IMAP_SERVER", "")
    )

    sigep.login()
    time.sleep(1)
    sigep.selecionar_orgao(os.getenv('ORGAO'))
    time.sleep(1)
    sigep.selecionar_sistema("Sistema Integrado de Gestão de Pessoas da Justiça do Trabalho")
    time.sleep(1)
    input('')