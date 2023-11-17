import requests
import json
from write import Betline
import asyncio
from devtools import debug


async def request_si():
    url = "https://spectate-web.sisportsbook.com/spectate/sportsbook-req/getUpcomingEvents/mma/upcoming"
    url2 = "https://www.sisportsbook.com/ufc-mma/"
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "X-Spectateclient-V": "2.37",
        "Referer": "https://www.sisportsbook.com/",
        "Origin": "https://www.sisportsbook.com",
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    }
    cookies: dict = {
        "_rdt_uuid": "1698624300270.b713b46f-edce-41f4-b926-b0efc"
    }
    response = requests.request("GET", url2)
    response_2 = requests.request("POST", url, cookies=response.cookies, headers=headers)
    debug(response_2)


async def scrape_si():
    data = await request_si()


if __name__ == "__main__":
    asyncio.run(scrape_si())
