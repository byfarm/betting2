from scrapers.request_client import client
import json
from devtools import debug
import asyncio
from write import Betline
from odds_calc import decimal_to_american


async def pointsbet_request(url: str = None):
    # ufc is default url
    if not url:
        url = "https://api.va.pointsbet.com/api/v2/competitions/16210/events/featured?includeLive=false&page=1"
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    response = await client.request("GET", url, headers=headers)
    response = response.json()
    return response


async def parse_pointsbet(data: dict):
    events = data.get("events", [])
    all_bets: list[Betline] = []
    for event in events:
        market = event.get("fixedOddsMarkets", [])[0]
        bets = market.get("outcomes", [])
        pair = []
        for bet in bets:
            odd: int = decimal_to_american(bet.get("price", 0))
            name: str = bet.get("name", "")
            card = Betline(name, odd)
            pair.append(card)

        pair[0].matchup, pair[1].matchup = pair[1], pair[0]
        all_bets += pair
    return all_bets


async def scrape_pointsbet(url: str = None):
    response = await pointsbet_request(url)
    bets = await parse_pointsbet(response)
    return bets


if __name__ == "__main__":
    bets = asyncio.run(scrape_pointsbet("https://api.nj.pointsbet.com/api/v2/sports/tennis/events/nextup?limit=50"))
    debug(bets)
