class Verify:
    def __init__(self, email):
        self.email = email

    async def format_check(self):
        import re

        try:
            EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(EMAIL_REGEX, self.email):
                return "BAD"
            else:
                return "OK"
        except:
            return "ERROR"

    async def mailbox_check(self):
        import dns.resolver

        domain = self.email.split("@")[1]
        try:
            result = dns.resolver.resolve(domain, "MX")
            if (
                str(result[0].exchange) != ""
                and str(result[0].exchange) != "localhost."
            ):
                return "EXIST"
            else:
                return "NOT EXIST"
        except:
            return "ERROR"

    async def smtp_check(self):
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
            return "OK"
        except:
            domains = [
                "aol.com",
                "att.net",
                "comcast.net",
                "facebook.com",
                "gmail.com",
                "gmx.com",
                "googlemail.com",
                "google.com",
                "hotmail.com",
                "hotmail.co.uk",
                "mac.com",
                "me.com",
                "mail.com",
                "msn.com",
                "live.com",
                "sbcglobal.net",
                "verizon.net",
                "yahoo.com",
                "yahoo.co.uk",
                "email.com",
                "fastmail.fm",
                "games.com",
                "gmx.net",
                "hush.com",
                "hushmail.com",
                "icloud.com",
                "iname.com",
                "inbox.com",
                "lavabit.com",
                "love.com",
                "outlook.com",
                "pobox.com",
                "protonmail.ch",
                "protonmail.com",
                "tutanota.de",
                "tutanota.com",
                "tutamail.com",
                "tuta.io",
                "keemail.me",
                "rocketmail.com",
                "safe-mail.net",
                "wow.com",
                "ygm.com",
                "ymail.com",
                "zoho.com",
                "yandex.com",
                "bellsouth.net",
                "charter.net",
                "cox.net",
                "earthlink.net",
                "juno.com",
                "btinternet.com",
                "virginmedia.com",
                "blueyonder.co.uk",
                "live.co.uk",
                "ntlworld.com",
                "orange.net",
                "sky.com",
                "talktalk.co.uk",
                "tiscali.co.uk",
                "virgin.net",
                "bt.com",
                "sina.com",
                "sina.cn",
                "qq.com",
                "naver.com",
                "hanmail.net",
                "daum.net",
                "nate.com",
                "yahoo.co.jp",
                "yahoo.co.kr",
                "yahoo.co.id",
                "yahoo.co.in",
                "yahoo.com.sg",
                "yahoo.com.ph",
                "163.com",
                "yeah.net",
                "126.com",
                "21cn.com",
                "aliyun.com",
                "foxmail.com",
                "hotmail.fr",
                "live.fr",
                "laposte.net",
                "yahoo.fr",
                "wanadoo.fr",
                "orange.fr",
                "gmx.fr",
                "sfr.fr",
                "neuf.fr",
                "free.fr",
                "gmx.de",
                "hotmail.de",
                "live.de",
                "online.de",
                "t-online.de",
                "web.de",
                "yahoo.de",
                "libero.it",
                "virgilio.it",
                "hotmail.it",
                "aol.it",
                "tiscali.it",
                "alice.it",
                "live.it",
                "yahoo.it",
                "email.it",
                "tin.it",
                "poste.it",
                "teletu.it",
                "bk.ru",
                "inbox.ru",
                "list.ru",
                "mail.ru",
                "rambler.ru",
                "yandex.by",
                "yandex.com",
                "yandex.kz",
                "yandex.ru",
                "yandex.ua",
                "ya.ru",
                "hotmail.be",
                "live.be",
                "skynet.be",
                "voo.be",
                "tvcablenet.be",
                "telenet.be",
                "hotmail.com.ar",
                "live.com.ar",
                "yahoo.com.ar",
                "fibertel.com.ar",
                "speedy.com.ar",
                "arnet.com.ar",
                "yahoo.com.mx",
                "live.com.mx",
                "hotmail.es",
                "hotmail.com.mx",
                "prodigy.net.mx",
                "yahoo.ca",
                "hotmail.ca",
                "bell.net",
                "shaw.ca",
                "sympatico.ca",
                "rogers.com",
                "yahoo.com.br",
                "hotmail.com.br",
                "outlook.com.br",
                "uol.com.br",
                "bol.com.br",
                "terra.com.br",
                "ig.com.br",
                "r7.com",
                "zipmail.com.br",
                "globo.com",
                "globomail.com",
                "oi.com.br",
            ]
            if domain in domains:
                return "OK"
            else:
                return "BAD"
