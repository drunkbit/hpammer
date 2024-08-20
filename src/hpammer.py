from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from fake_useragent import UserAgent  # https://github.com/fake-useragent/fake-useragent
import json
import os
import random
import requests
import time

# define request
number = 0
url = ""
headers = {
    "Host": "",
    "Accept": "application/json",
    "User-Agent": UserAgent(min_percentage=20.0).random,
    "X-Requested-With": "XMLHttpRequest",
}
data = {"choice[]": f"{number}"}

# get proxies
protocols = ["http", "socks4", "socks5"]
proxies = []
for protocol in protocols:
    for file_name in os.listdir(f"proxies/{protocol}"):
        file_path = os.path.join(f"proxies/{protocol}", file_name)
        with open(file_path, "r") as f:
            proxies += [f"{protocol}://" + proxy for proxy in f.read().splitlines()]


# vote
def vote():
    proxy = random.choice(proxies)
    proxies.remove(proxy)
    # print(f"{datetime.now()}: {proxy}: start ({len(proxies)} proxies left)")

    for j in range(1, 21):
        try:
            session = requests.Session()
            session.proxies = {"http": proxy, "https": proxy}
            response = session.post(url, headers=headers, data=data, timeout=10)
            response_data = json.loads(response.text)
            result = response_data["result"][""]
            text = result["text"]
            percentage = result["percentage"]
            count = result["count"]
            print(
                f"{datetime.now()}: {proxy}: nr {j}: {percentage}% / {count} votes: {text} - {len(proxies)} proxies left"
            )
            time.sleep(random.randint(2, 5))

        except:
            try:
                test = response_data["result"]
                # print(response_data)
            except:
                # print(f"{datetime.now()}: {proxy}: error")
                break


# vote parallel
with ThreadPoolExecutor(max_workers=100) as executor:
    for i in range(0, len(proxies)):
        executor.submit(vote)
