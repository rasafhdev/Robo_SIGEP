from sigep import Sigep
import os
import dotenv
from time import sleep

dotenv.load_dotenv()

if __name__ == '__main__':
    app = Sigep()

    """
    Atributos:
        Todos os valores podem ser capturados dinamicamente, ou, se None, são
        capturados pelo arquivo .env.
    ----------

    USERNAME_SIGEP : str | None
        Código do usuário. Apesar de numérico, deve ser tratado como string.

    PASSWORD_SIGEP : str | None
        Senha real do usuário. Infelizmente ou felizmente, é isso.

    URL_SIGEP : str | None
        URL principal do sistema.

    EMAIL : str | None
        Email cadastrado que recebe o código MFA.

    EMAIL_PASSWORD_APP : str | None
        Senha de aplicativo! É a senha de API configurada no email do usuário,
        que recebe o código MFA. Essa senha não é a senha do email.

    IMAP_SERVER : str | None
        Configuração do servidor do provedor de email (ex.: Gmail, Outlook, UOL).
    """

    app._setup_driver() # Faz a configuração do navegador
    app.acessar_orgao_desejado(nome_do_orgao=os.getenv('ORGAO')) # Loga conforme órgão
    app.logar_no_sistema() # faz login no sistema
    app.consultar_informacoes_financeiras()
    app.imprimir_e_salvar_arquivo()

