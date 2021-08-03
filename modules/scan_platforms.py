from socialscan.util import Platforms, sync_execute_queries
import requests
import httpx
from holehe.modules.mails.google import google
from holehe.modules.mails.protonmail import protonmail


class Scan_Platforms:
    def __init__(self, email):
        self.email = email

    def scan_social(self):
        try:

            plaform_list = []
            query = [self.email]
            platforms = [
                Platforms.TWITTER,
                Platforms.INSTAGRAM,
                Platforms.TUMBLR,
                Platforms.SPOTIFY,
            ]
            results = sync_execute_queries(query, platforms)
            for result in results:
                if (
                    result.success == True
                    and result.valid == True
                    and result.available == False
                ):
                    plaform_list.append(str(result.platform))
            return plaform_list
        except:
            return 0

    # PoC
    async def scan_mailbox_providers(self):
        domain = self.email.split("@")[1]
        try:
            if domain == "yaani.com":

                url = "https://api.yaanimail.com/gateway/v1/accounts/check-email"
                myobj = '{"email":"' + self.email + '"}'
                headers = {
                    "Host": "api.yaanimail.com",
                    "Accept": "application/json, text/plain, */*",
                    "Device-Name": "PoC",
                    "Device-Os": "WEB",
                    "Content-Type": "application/json",
                }

                data = requests.post(url, data=myobj, headers=headers)
                if str(data.json()["status"]) == "200":
                    return False
                else:
                    return True
            elif domain == "gmail.com" or domain == "protonmail.com":

                email = self.email
                out = []
                client = httpx.AsyncClient()
                if domain == "gmail.com":

                    await google(email, client, out)
                if domain == "protonmail.com":

                    await protonmail(email, client, out)
                await client.aclose()
                return out[0]["exists"]
            else:
                return None
        except:
            return 0
