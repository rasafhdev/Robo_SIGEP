import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dataclasses import dataclass
from scrappings import ScrappingGmail  # Importando a classe ScrappingGmail para capturar o código MFA
import dotenv
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Sigep:
    USERNAME_SIGEP: str
    PASSWORD_SIGEP: str
    URL_SIGEP: str
    EMAIL: str
    EMAIL_PASSWORD: str
    IMAP_SERVER: str

    def setup_driver(self):
        """Configura o WebDriver do Chromium para rodar sem interface gráfica."""
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"  # Caminho para o Chromium
        #chrome_options.add_argument("--headless")  # Rodar sem interface gráfica
        chrome_options.add_argument("--disable-gpu")
        
        # Configurações de cookies
        chrome_options.add_argument("--enable-features=CookiesWithoutSameSiteMustBeSecure")
        chrome_options.add_argument("--enable-cookies")
        chrome_options.add_argument("--enable-extensions")  # Desabilita extensões
        chrome_options.add_argument("--disable-popup-blocking")  # Desabilita bloqueios de popups
        # chrome_options.add_argument("--incognito")  # Usar o modo de navegação anônima (sem histórico)
        chrome_options.add_argument("--enable-notifications")  # Desativa notificações do Chrome

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        """Realiza o login no sistema Sigep e verifica se o MFA é solicitado."""
        self.setup_driver()
        self.driver.get(self.URL_SIGEP)
        print(input('Pause, clique para continuar'))

        # Espera o site carregar
        time.sleep(3)

        # Insere as credenciais
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        username_field.send_keys(self.USERNAME_SIGEP)
        password_field.send_keys(self.PASSWORD_SIGEP)
        password_field.submit()

        # Aguarda o carregamento da página de MFA (caso necessário)
        time.sleep(3)

        # Verifica se o campo de MFA aparece
        try:
            # Verifica se o campo de MFA existe
            mfa_field = self.driver.find_element(By.ID, "code")  # Substitua pelo ID correto do campo MFA
            print("MFA is required!")
            
            # Captura o código MFA via ScrappingGmail
            email_account = ScrappingGmail(
                EMAIL=self.EMAIL,
                EMAIL_PASSWORD=self.EMAIL_PASSWORD,
                IMAP_SERVER=self.IMAP_SERVER
            )

            if email_account.auth_email():
                # Aguardamos um pouco para garantir que o e-mail com o código MFA tenha chegado
                time.sleep(5)
                email_account.list_messages(
                    sender=os.getenv("SENDER", ''),  # Substitua pelo remetente do e-mail MFA
                    subject=os.getenv("SUBJECT", ''),  # Substitua pelo assunto do e-mail MFA
                    qty=1
                )
                email_account.logout()

            mfa_code = email_account.MFA_CODE  # Captura o código MFA do e-mail

            # Insere o código MFA no campo e submete o formulário
            mfa_field.send_keys(mfa_code)
            mfa_field.submit()
            print(f"MFA Code '{mfa_code}' submitted.")
            page_content = self.driver.page_source  # Captura o conteúdo da página
            print("Page Content: ", page_content)
            
        except:
            print("No MFA required, login successful.")  # Se não precisar de MFA
            

    def close(self):
        """Fecha o navegador após a execução."""
        if hasattr(self, 'driver'):
            self.driver.quit()


if __name__ == "__main__":
    # Carrega as variáveis de ambiente
    dotenv.load_dotenv()

    # Exemplo de uso da classe Sigep
    sigep = Sigep(
        USERNAME_SIGEP=os.getenv("USERNAME_SIGEP", ""),
        PASSWORD_SIGEP=os.getenv("PASSWORD_SIGEP", ""),
        URL_SIGEP=os.getenv("URL_SIGEP", ""),
        EMAIL=os.getenv("EMAIL", ""),
        EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD", ""),
        IMAP_SERVER=os.getenv("IMAP_SERVER", "")
    )

    # Realiza o login e captura o código MFA, se necessário
    sigep.login()

    # Fecha o navegador
    sigep.close()