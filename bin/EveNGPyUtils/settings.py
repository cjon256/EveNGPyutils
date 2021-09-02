import os

USERNAME = os.getenv("EVE_USERNAME", "admin")
PASSWORD = os.getenv("EVE_PASSWORD", "eve")
BASE_URL = os.getenv("EVE_BASE_URL", "https://eve-ng.lab.local")
HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json; q=1.0, text/javascript;q=0.8, */*; q=0.01',
    'html5': '-1'
}


def server_conf():
    return BASE_URL, HEADERS, PASSWORD, USERNAME


"""
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 0
Content-Type: text/plain;charset=UTF-8
Host: tps10223.doubleverify.com
Origin: https://mkyong.com
Referer: https://mkyong.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: cross-site
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
"""
