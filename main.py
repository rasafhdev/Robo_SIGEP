from scrappings import ScrappingGmail
from sigep import Sigep
import dotenv
import os


if __name__ == "__main__":
    dotenv.load_dotenv()
    
    email_account = ScrappingGmail(
        EMAIL=os.getenv("EMAIL", ''),
        EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD", ''),
        IMAP_SERVER=os.getenv("IMAP_SERVER", '')
    )

    if email_account.auth_email():
        email_account.list_messages(
            sender=os.getenv("SENDER", ''),
            subject=os.getenv("SUBJECT", ''),
            qty=1
        )
        email_account.logout()