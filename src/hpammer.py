from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from fake_useragent import UserAgent  # https://github.com/fake-useragent/fake-useragent
import json
import os
import random
import requests
import time

# define request
url = ""
headers = {
    "Host": "",
    "Accept": "application/json",
    "User-Agent": UserAgent(min_percentage=20.0).random,
}
data = {"data": "empty"}

# get proxies
path = "proxies"
protocols = ["http", "socks4", "socks5"]
proxies = []
for protocol in protocols:
    for file_name in os.listdir(f"{path}/{protocol}"):
        file_path = os.path.join(f"{path}/{protocol}", file_name)
        with open(file_path, "r") as f:
            proxies += [f"{protocol}://" + proxy for proxy in f.read().splitlines()]


# send request
def send(rate_limit: int = 20, sleep_interval: int = 5):
    proxy = random.choice(proxies)
    proxies.remove(proxy)
    print(f"{datetime.now()}: {proxy}: start ({len(proxies)} proxies left)")

    for j in range(0, rate_limit):
        try:
            session = requests.Session()
            session.proxies = {"http": proxy, "https": proxy}
            response = session.post(url, headers=headers, data=data, timeout=10)
            response_data = json.loads(response.text)

            # custom response handling
            result = response_data["result"][""]
            text = result["text"]
            percentage = result["percentage"]
            count = result["count"]
            output = f"{percentage}% / {count} votes: {text}"

            print(f"{datetime.now()}: {proxy}: nr {j}: {output}")
            time.sleep(random.randint(1, sleep_interval))

        except:
            print(f"{datetime.now()}: {proxy}: error")
            break


# send requests parallel
with ThreadPoolExecutor(max_workers=100) as executor:
    for i in range(0, len(proxies)):
        executor.submit(send)
