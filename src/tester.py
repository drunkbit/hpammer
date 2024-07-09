import random
import requests
from concurrent.futures import ThreadPoolExecutor


# get proxy list
dates = [
    "2024011601",
    "2024011602",
    "2024011603",
    "2024011604",
    "2024011605",
    "2024011606",
    "2024011607",
    "2024011608",
]
protocol = "http"
proxies = []
tested = []
for date in dates:
    with open(f"./proxies/{date}/{protocol}.txt", "r") as file:
        proxies += [f"{protocol}://" + proxy for proxy in file.read().splitlines()]


# test proxy
def test():
    proxy = random.choice(proxies)
    proxies.remove(proxy)

    try:
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        response = session.get("http://icanhazip.com", timeout=10)
        if response.status_code == 200:
            proxy = proxy.replace(f"{protocol}://", "")
            tested.append(proxy)
            if len(tested) % 5 == 0:
                with open(f"./proxies/tested/{protocol}.txt", "w") as file:
                    for proxy in tested:
                        file.write(proxy + "\n")
                print(
                    f"wrote {len(tested)} proxies to file ({len(proxies)} left to test)"
                )
    except:
        return


# test parallel
with ThreadPoolExecutor(max_workers=250) as executor:
    for i in range(0, len(proxies)):
        executor.submit(test)
