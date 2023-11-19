import json
from devtools import debug
from scrapers.request_client import client
from write import Betline
from write import write_to_csv
import datetime


class Bet:
    def __init__(self, data: dict):
        self.name = data.get("runnerName")
        self.odds: int = (
            data.get("winRunnerOdds", {})
            .get("americanDisplayOdds")
            .get("americanOddsInt")
        )


class Matchup:
    def __init__(self, data: dict):
        debug(data)
        runners = data.get("runners", [])
        players = []
        for runner in runners:
            bet = Bet(runner)
            players.append(bet)
        self.home, self.away = players


async def fanduel_request(url: str = None):
    if not url:
        url = "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=SPORT&eventTypeId=26420387&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FNew_York"

    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = await client.request("Get", url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"status code {response.status_code} in request")

    data: dict = response.json()
    return data


def parse_fanduel(data: dict):
    markets = data.get("attachments", {}).get("markets", {})

    currtime = (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(tzinfo=None)
        + datetime.timedelta(days=6)
    )

    tzcheck = False
    if "nfl" in (
        list(markets.values())[0].get("runners", [])[0].get("logo", "")
    ):
        tzcheck = True

    all_matchups = []
    baddays = {"Thu", "Fri"}
    for market in markets.values():
        if market.get("marketName", "") != "Moneyline":
            continue

        dt = datetime.datetime.strptime(
            market.get("marketTime"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if ((dt > currtime) and tzcheck) or dt.strftime("%a") in baddays:
            continue

        # debug(market)
        pair = []
        for runner in market.get("runners", []):
            name = runner.get("runnerName", "")
            if name in [x.name for x in all_matchups]:
                break
            odds: int = (
                runner.get("winRunnerOdds", {})
                .get("americanDisplayOdds")
                .get("americanOddsInt")
            )
            player = Betline(name, odds)
            pair.append(player)

        if len(pair) == 2:
            pair[0].matchup, pair[1].matchup = pair[1], pair[0]

            all_matchups.append(pair[0])
            all_matchups.append(pair[1])

    return all_matchups


async def scrape_fanduel(url: str = None):
    data = await fanduel_request(url)
    all_matchups = parse_fanduel(data)
    return all_matchups


if __name__ == "__main__":
    url = "https://sbapi.co.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nfl&pbHorizontal=false&_ak=FhMFpcPWXMeyZxOx&timezone=America%2FDenver"
    import asyncio
    data = asyncio.run(scrape_fanduel(url))
    debug(data)
