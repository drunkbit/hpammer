import os
import requests
import shutil
import sys

# delete old proxies for a clean start
delete_old_proxies = True

url_repo = "https://github.com/TheSpeedX/PROXY-List"
url_api = "https://api.github.com/repos/TheSpeedX/PROXY-List/commits"
url_raw = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List"

response = requests.get(url_api)
commits = response.json()

# if api rate limit is exceeded
if "message" in commits:
    if commits["message"].startswith("API rate limit exceeded"):
        print(commits["message"])
        sys.exit()

# define protocols
protocols = ["http", "socks4", "socks5"]

# delete old proxy files if delete_old_proxies is true
if delete_old_proxies:
    for protocol in protocols:
        path = f"proxies/{protocol}"
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s: %s" % (file_path, e))

print(f"Commits: {len(commits)}\n")

# for each commit
for commit in commits:

    sha = commit["sha"]

    # skip commit if message is not 'updated proxies'
    if (commit["commit"]["message"] == "Updated Proxies") == False:
        print(f"Skip commit: {sha}")
        continue

    print(f"\nCommit: {sha}")

    # for each protocol, download and save proxy file
    for protocol in protocols:

        # download file
        file_url = f"{url_raw}/{sha}/{protocol}.txt"
        print(f"Url: {file_url}")
        r = requests.get(file_url)

        # save file
        file_name = f"proxies/{protocol}/{sha}"
        with open(file_name, "wb") as f:
            f.write(r.content)

        print(f"Downloaded: {file_name}")
