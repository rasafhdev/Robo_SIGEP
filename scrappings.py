# modulo

from dataclasses import dataclass
import imaplib
import email
from email.header import decode_header
import dotenv
import os

dotenv.load_dotenv()

@dataclass
class ScrappingGmail:
    EMAIL: str
    EMAIL_PASSWORD: str
    IMAP_SERVER: str
    MFA_CODE: str | None = None

    def auth_email(self):
        """Authenticate in Gmail and return the connection."""
        try:
            self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            self.mail.login(self.EMAIL, self.EMAIL_PASSWORD)
            self.mail.select("inbox")
            return self.mail
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

    def get_body(self, msg):
        """Get the body of the email."""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        return part.get_payload(decode=True).decode(errors="ignore")
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        return part.get_payload(decode=True).decode(errors="ignore")
            else:
                return msg.get_payload(decode=True).decode(errors="ignore")
        except Exception as e:
            print(f"Error extracting email body: {e}")
            return None

    def list_messages(self, sender, subject, qty=3):
        """List emails from a specific sender and with a specific subject."""
        try:
            status, messages = self.mail.search(None, f'(FROM "{sender}" SUBJECT "{subject}")')

            if status != "OK" or not messages[0]:
                print("No messages found.")
                return

            email_ids = messages[0].split()[-qty:]

            for num in reversed(email_ids):
                status, msg_data = self.mail.fetch(num, "(RFC822)")

                if status != "OK" or not msg_data or not msg_data[0]:
                    print("Failed to fetch email.")
                    continue

                raw_email = msg_data[0][1] if isinstance(msg_data[0], tuple) else None

                if not raw_email or not isinstance(raw_email, bytes):
                    print(f"Unexpected email format: {type(raw_email)}")
                    continue

                msg = email.message_from_bytes(raw_email)

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                print(f'Subject: {subject}')
                print(f'Sender: {msg["From"]}')

                # Get the body of the email
                body = self.get_body(msg)
                if body:
                    print(f'Body: {body}\n')

                    # Check and capture the MFA code
                    self.MFA_CODE = self.extract_mfa_code(body)
                    if self.MFA_CODE:
                        print(f'MFA Code found: {self.MFA_CODE}')
                        # Now we can delete the email
                        self.delete_email(num)
        except Exception as e:
            print(f"Error listing messages: {e}")

    def extract_mfa_code(self, body):
        """Extract the first 6 characters from the email body as the MFA code."""
        if body:
            return body[:6]  # Capture only the first 6 characters
        return None

    def delete_email(self, num):
        """Delete an email from the server."""
        try:
            self.mail.store(num, '+FLAGS', '\\Deleted')
            self.mail.expunge()
            print(f"Email deleted.")
        except Exception as e:
            print(f"Error deleting email: {e}")

    def logout(self):
        """End the login session."""
        try:
            self.mail.logout()
            print("Logged out successfully.")
        except Exception as e:
            print(f"Error logging out: {e}")


if __name__ == "__main__":

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
