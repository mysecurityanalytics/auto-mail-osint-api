class Verify:
    def __init__(self, email):
        self.email = email

    async def check_regex(self):
        import re

        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(EMAIL_REGEX, self.email):
            return False
        else:
            return True

    async def check_mailbox(self):
        import dns.resolver

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
        except:
            return False

    async def check_smtp(self):
        import dns.resolver
        import smtplib
        import socket

        domain = self.email.split("@")[1]
        try:
            result = dns.resolver.resolve(domain, "MX")
            socket.setdefaulttimeout(2)
            with smtplib.SMTP_SSL(str(result[0].exchange), 465) as server:
                server.ehlo()
                server.quit()
            return True
        except:
            with open('modules/domains.txt') as f:
                if domain in f.read():
                    return True
                else:
                    return False
