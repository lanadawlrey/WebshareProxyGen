from src.console import Console
import httpx
import random
import time
import threading
import json

class Webshare:
    def __init__(self) -> None:
        self.config = json.loads(open("config.json", 'r').read())
        self.proxies = []

    def solver(self):
        jsosn =  {
            "clientKey": self.config["key"],
            "task": {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://proxy2.webshare.io/register",
                "websiteKey": "6LeHZ6UUAAAAAKat_YS--O2tj_by3gv3r_l03j9d",
                "isInvisible": True,
            }
        }
        taskid = httpx.post("https://api.capsolver.com/createTask", json=jsosn).json()["taskId"]   
        while True:
            ok = {"clientKey": self.config["key"], "taskId": taskid}
            response = httpx.post("https://api.capsolver.com/getTaskResult", json=ok)
            if response.json()["status"] == "ready":
                return response.json()["solution"]["gRecaptchaResponse"]
            else:
                pass
            time.sleep(0.5)

    def register(self):
        while True:
            try:
                if not self.proxies:
                    with open("output/proxies.txt", "r") as f:
                        self.proxies = f.read().splitlines()

                proxy = random.choice(self.proxies)
                proxy_parts = proxy.split('@')
                proxy_userpass = proxy_parts[0]
                proxy_ipport = proxy_parts[1]

                if ':' in proxy_userpass:
                    proxy_user, proxy_pass = proxy_userpass.split(':')
                else:
                    proxy_user = proxy_userpass
                    proxy_pass = None

                if ':' in proxy_ipport:
                    proxy_ip, proxy_port = proxy_ipport.split(':')
                else:
                    raise ValueError("Invalid proxy format")

                proxy_dict = {
                    "http://": f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}",
                    "https://": f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
                }

                headers = {
                    'authority': 'proxy.webshare.io',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'origin': 'https://proxy2.webshare.io',
                    'referer': 'https://proxy2.webshare.io/',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                }

                key = self.solver()
                Console.log(f"Solved {key[:23]}")

                self.domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@protonmail.com"]
                self.email =  f"Slotths" + "_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8)) + random.choice(self.domains)

                json_data = {
                    'email': self.email,
                    'password': 'lkjsdflkjsldkfj',
                    'tos_accepted': True,
                    'recaptcha': key
                }

                with httpx.Client(proxies=proxy_dict) as session:
                    response = session.post('https://proxy.webshare.io/api/v2/register/', headers=headers, json=json_data)
                    if response.status_code == 200:
                        token = response.json()["token"]
                        Console.success(f"Made Account: {self.email}:lkjsdflkjsldkfj")

                        headers['authorization'] = f'Token {token}'

                        params = {
                            'mode': 'direct',
                            'page': '1',
                            'page_size': '10',
                        }

                        response = session.get('https://proxy.webshare.io/api/v2/proxy/list/', params=params, headers=headers)
                        for i in response.json()["results"]:
                            username = i["username"]
                            password = i["password"]
                            ip = i["proxy_address"]
                            port = i["port"]
                            Console.success(f"Created {username}:{password}@{ip}:{port}")
                            with open("output/proxies.txt", "a") as e:
                                e.write(f"{username}:{password}@{ip}:{port}\n")
                    else:
                        print(response.text)
            except Exception as e:
                print(e)
                pass

for i in range(10):
    threading.Thread(target=Webshare().register).start()
