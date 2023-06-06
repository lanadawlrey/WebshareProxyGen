from src.console import Console

import httpx
import random
import time
import threading
import json

lol = json.loads(open("config.json", 'r').read())

class Webshare:
    def __init__(self) -> None:
        self.client = httpx.Client(proxies=None, timeout=120)
    
    def solver(self):
       jsosn =  {
            "clientKey": lol["key"],
            "task": {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://proxy2.webshare.io/register",
                "websiteKey": "6LeHZ6UUAAAAAKat_YS--O2tj_by3gv3r_l03j9d",
                "isInvisible": True,
            }
        }
       taskid = httpx.post("https://api.capsolver.com/createTask", json=jsosn).json()["taskId"]   
       while True:
           ok = {"clientKey": lol["key"], "taskId": taskid}
           response = httpx.post("https://api.capsolver.com/getTaskResult", json=ok)
           #print(response.text)
           if response.json()["status"] == "ready":
                return response.json()["solution"]["gRecaptchaResponse"]
           else:
               # print(response.text)
               pass
           
           time.sleep(0.5)

       


    def register(self):
        while True:
            try:
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
                response = self.client.post('https://proxy.webshare.io/api/v2/register/', headers=headers, json=json_data)
                if response.status_code == 200:
                    token = response.json()["token"]
                    Console.success(f"Made Account: {self.email}:lkjsdflkjsldkfj")

                    headers = {
                        'authority': 'proxy.webshare.io',
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'en-US,en;q=0.9',
                        'authorization': f'Token {token}',
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

                    params = {
                        'mode': 'direct',
                        'page': '1',
                        'page_size': '10',
                    }

                    response = self.client.get('https://proxy.webshare.io/api/v2/proxy/list/', params=params, headers=headers)
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
            except:
                pass

for i in range(10):
    threading.Thread(target=Webshare().register).start()