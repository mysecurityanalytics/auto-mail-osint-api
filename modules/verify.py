import re
import dns.resolver
import smtplib
import socket


class Verify:
    def __init__(self, email):
        self.email = email

    async def check_regex(self):

        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(EMAIL_REGEX, self.email):
            return False
        else:
            return True

    async def check_mailbox(self):

        domain = self.email.split("@")[1]
        try:
            result = dns.resolver.resolve(domain, "MX")
            if (
                str(result[0].exchange) != ""
                and str(result[0].exchange) != "localhost."
            ):
                return True
            else:
                return False
        except Exception as e:
            return 0

    async def check_smtp(self, port):

        domain = self.email.split("@")[1]
        try:
            result = dns.resolver.resolve(domain, "MX")
            socket.setdefaulttimeout(2)
            if port == 465:
                with smtplib.SMTP_SSL(str(result[0].exchange), port) as server:
                    server.ehlo()
                    server.quit()
                return True
            else:
                with smtplib.SMTP(str(result[0].exchange), port) as server:
                    server.ehlo()
                    server.quit()
                return True
        except:
            with open("modules/domains.txt") as f:
                if domain in f.read():
                    return True
                else:
                    return False
