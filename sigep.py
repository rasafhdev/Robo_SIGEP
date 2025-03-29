# Instalados
from scrapper import ScrappingGmail 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui as pg
import dotenv
import shutil

# Built-ins
from dataclasses import dataclass
import os
from time import sleep
from datetime import datetime


# Carrega info env
dotenv.load_dotenv()

@dataclass
class Sigep:
    USERNAME_SIGEP: str | None = os.getenv('USERNAME_SIGEP')
    PASSWORD_SIGEP: str | None = os.getenv('PASSWORD_SIGEP')
    URL_SIGEP: str      | None = os.getenv('URL_SIGEP')
    EMAIL: str          | None = os.getenv('EMAIL')
    EMAIL_PASSWORD_APP: str | None = os.getenv('EMAIL_PASSWORD_APP')
    IMAP_SERVER: str    | None = os.getenv('IMAP_SERVER')

    def _setup_driver(self):
        """Configura o WebDriver do Chrome para rodar sem interface gráfica."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument(
            "--enable-features=CookiesWithoutSameSiteMustBeSecure"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)


    def acessar_orgao_desejado(self, nome_do_orgao):
        # Abrir pagina principal
        if not self.URL_SIGEP:
            raise ValueError("Necessário inserir a URL do Sistema")
        self.driver.get(self.URL_SIGEP)


        # Inicio Seção de interação com o formulário inicial
        seleciona_orgao_desejado = self.wait.until(
            EC.element_to_be_clickable((By.ID, "formTribunal_nome"))
        )
        seleciona_orgao_desejado.click()

        orgao_desejado = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,f"//span[contains(text(), '{nome_do_orgao}')]")
            )
        )
        orgao_desejado.click()

        btn_ok = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-ok"))
        )
        btn_ok.click()
        # Fim da seção de interação com o formulário inicial


    def logar_no_sistema(self):
        sleep(3)
        # Verificação de credenciais
        if not all([self.USERNAME_SIGEP, self.PASSWORD_SIGEP]):
            raise ValueError('Credenciais de login não fornecidas')

        # Inicio da interação com o formulário de login
        btn_especial = self.wait.until(
            EC.element_to_be_clickable((By.ID, "social-keycloak-oidc"))
        )
        btn_especial.click()

        # Preencher credenciais
        username_sigep = self.driver.find_element(By.ID, "username")
        password_sigep = self.driver.find_element(By.ID, "password")
        username_sigep.send_keys(self.USERNAME_SIGEP or "")
        password_sigep.send_keys(self.PASSWORD_SIGEP or "")
        password_sigep.submit()

        # Verifica se o campo de MFA aparece
        try:
            mfa_field = self.driver.find_element(By.ID, "code")
            print("MFA is required!")

            # Captura o código MFA via ScrappingGmail
            _email_account = ScrappingGmail(
                EMAIL=self.EMAIL,
                EMAIL_PASSWORD=self.EMAIL_PASSWORD_APP,
                IMAP_SERVER=self.IMAP_SERVER
            )

            if _email_account.auth_email():
                sleep(5)
                _email_account.list_messages(
                    sender=os.getenv("SENDER", ''),
                    subject=os.getenv("SUBJECT", ''),
                    qty=1
                )
                _email_account.logout()

            mfa_code = _email_account.MFA_CODE
            mfa_field.send_keys(mfa_code)
            mfa_field.submit()
            print(f"MFA Code '{mfa_code}' submitted.")

        except:
            print("No MFA required, login successful.")

    
    def consultar_informacoes_financeiras(self):
        sleep(6)
        # Recebe a URL de consulta
        self.driver.get(os.getenv('URL_CONSULTA'))

        # Baixar o arquivo
        btn_imprimir = self.wait.until(
            EC.element_to_be_clickable((By.ID, "botaoSalvarImprimir"))
        )
        btn_imprimir.click()

        

    def imprimir_e_salvar_arquivo(self, ):
        usuario = os.getlogin()
        mes = datetime.now().month
        ano = datetime.now().year
        arquivo  = f'contracheque_{ano}-0{mes}_Folha Normal.pdf'
        
        sleep(2)
        # pg.hotkey('ctrl', 'p') # para imprimir
        # sleep(0.30)
        # pg.press('enter')
        # pg.hotkey('alt', 'f4')
        # pg.hotkey('alt', 'f4')
        
        if os.name == 'nt':
            origem = f'c:\\Users\\{usuario}\\Downloads\\{arquivo}'
            destino = f'c:\\Users\\{usuario}\\Desktop\\CONTRACHEQUES\\'
        else:
            origem = f'home/{usuario}/Downloads'
            destino = f'home/{usuario}/Desktop/{arquivo}'

        shutil.move(origem, destino)

        #input('Pressione Enter para finalizar...')
        
