from scrapers.request_client import client
import json
import asyncio
from devtools import debug
from write import Betline


async def request_ceasers(url: str = None):
    if not url:
        url = "https://api.americanwagering.com/regions/us/locations/wa-ms/brands/czr/sb/v3/sports/ufcmma/events/schedule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    bets_response = await client.request("GET", url, headers=headers)
    return bets_response.json()


def parse_ceasers(response: dict):
    competitions = response.get("competitions", [])
    all_bets: list[Betline] = []
    for competition in competitions:
        events = competition.get("events", [])

        for event in events:
            if len(event.get("markets", [])) < 1:
                continue
            selections = event.get("markets", [])[0].get("selections", [])

            pair = []
            for selection in selections:
                name: str = selection.get("name", "").strip("|")
                if name in [x.name for x in all_bets]:
                    break
                odd: int = selection.get("price", {}).get("a", 0)
                bet = Betline(name, odd)
                pair.append(bet)

            if len(pair) == 2:
                pair[0].matchup, pair[1].matchup = pair[1], pair[0]
                all_bets += pair
    return all_bets


async def scrape_ceasers(url: str = None):
    response = await request_ceasers(url)
    bets = parse_ceasers(response)
    return bets


if __name__ == "__main__":
    url = "https://api.americanwagering.com/regions/us/locations/co/brands/czr/sb/v3/sports/basketball/events/schedule/"
    res = asyncio.run(scrape_ceasers(url))
    debug(res)
