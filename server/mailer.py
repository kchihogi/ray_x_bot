import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, recipient_email, subject, message):
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add message body
        msg.attach(MIMEText(message, 'plain'))

        # Create SMTP session
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

if __name__ == "__main__":
    mailer = Mailer(os.environ['EMAIL_FROM'], os.environ['EMAIL_PASSWORD'], os.environ['EMAIL_SERVER'], os.environ['EMAIL_PORT'])
    mailer.send_email(os.environ['EMAIL_TO'], os.environ['EMAIL_SUBJECT'], os.environ['EMAIL_BODY'])
