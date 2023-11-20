from scrapers.request_client import client
import datetime
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

    # currtime = (
    #     datetime.datetime.now(datetime.timezone.utc)
    #     .replace(tzinfo=None)
    #     + datetime.timedelta(days=6)
    # )
    # baddays = {"Thu", "Fri"}

    for event in events:

        market = event.get("fixedOddsMarkets", [])

        if not market:
            market = event.get("specialFixedOddsMarkets", [])

        if not market:
            continue
        if market[0].get("sportKey", "") == "mma":
            market_check = "Fight Result"
        else:
            market_check = "Moneyline"

        market = [x for x in market if x.get("eventClass", "") == market_check]
        try:
            market = market[0]
        except IndexError:
            continue

        # tzcheck = True if event.get("sportKey") == "american-football" else False
        #
        # dt = datetime.datetime.strptime(
        #     market.get("advertisedStartTime"), "%Y-%m-%dT%H:%M:%SZ"
        # )
        #
        # if ((dt > currtime) and tzcheck) or dt.strftime("%a") in baddays:
        #     continue

        bets = market.get("outcomes", [])
        pair = []
        for bet in bets:
            odd: int = decimal_to_american(bet.get("price", 0))
            name: str = bet.get("name", "")
            if name in [x.name for x in all_bets]:
                break
            card = Betline(name, odd)
            pair.append(card)

        if len(pair) == 2:
            pair[0].matchup, pair[1].matchup = pair[1], pair[0]
            all_bets += pair
    return all_bets


async def scrape_pointsbet(url: str = None):
    response = await pointsbet_request(url)
    bets = await parse_pointsbet(response)
    return bets


if __name__ == "__main__":
    bets = asyncio.run(scrape_pointsbet("https://api.co.pointsbet.com/api/v2/competitions/58/events/featured?includeLive=false&page=1"))
    debug(bets)
