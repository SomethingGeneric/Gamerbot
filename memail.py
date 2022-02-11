import smtplib, ssl, sys, os

from util_functions import *


class MEmail:
    def __init__(self):
        smtp_server = SMTP_SERVER_ADDR
        port = SMTP_SERVER_PORT
        self.sender_email = SMTP_EMAIL_ADDR
        if os.path.exists(SMTP_PASSWORD_FILE):
            password = open(SMTP_PASSWORD_FILE).read().strip()
        else:
            print(
                "Could not find " + SMTP_PASSWORD_FILE + ", as set in config. Failing."
            )
            sys.exit(1)
        context = ssl.create_default_context()
        print(
            "Trying to log in to "
            + smtp_server
            + " on port "
            + str(port)
            + " as user "
            + self.sender_email
        )
        try:
            self.server = smtplib.SMTP(smtp_server, port)
            self.server.ehlo()
            self.server.starttls(context=context)
            self.server.ehlo()
            self.server.login(self.sender_email, password)
        except Exception as e:
            print(str(e))
            print("Failing b/c of above error")
            sys.exit(1)

    def send(self, to, msg):
        try:
            self.server.sendmail(self.sender_email, to, msg)
            return "Sent."
        except Exception as e:
            return str(e)
