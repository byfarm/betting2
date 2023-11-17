import json
from devtools import debug
from scrapers.request_client import client
from write import Betline
from write import write_to_csv


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


async def fanduel_request():
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

    all_matchups = []
    for market in markets.values():

        pair = []
        for runner in market.get("runners", []):
            name = runner.get("runnerName")
            odds: int = (
                runner.get("winRunnerOdds", {})
                .get("americanDisplayOdds")
                .get("americanOddsInt")
            )
            player = Betline(name, odds)
            pair.append(player)

        pair[0].matchup, pair[1].matchup = pair[1], pair[0]

        all_matchups.append(pair[0])
        all_matchups.append(pair[1])

    return all_matchups


async def scrape_fanduel():
    data = await fanduel_request()
    all_matchups = parse_fanduel(data)
    return all_matchups


if __name__ == "__main__":
    import asyncio
    data = asyncio.run(fanduel_request())
    all_matchups = parse_fanduel(data)
