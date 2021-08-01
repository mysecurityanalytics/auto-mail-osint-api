class Scan_Platforms:
    def __init__(self, email):
        self.email = email

    def scan_social(self):
        try:

            from socialscan.util import Platforms, sync_execute_queries

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
                if result.success:
                    if result.valid:
                        if not result.available:
                            plaform_list.append(str(result.platform))

            return plaform_list
        except:
            return 0

    # PoC
    async def scan_mailbox_providers(self):
        domain = self.email.split("@")[1]
        try:

            if domain == "yaani.com":
                import requests

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
            else:
                return 1
        except:
            return 0
