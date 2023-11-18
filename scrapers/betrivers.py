from scrapers.request_client import client
from devtools import debug
import json
import asyncio
from write import Betline


async def request_betriver(url: str = None):
    if not url:
        url = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=20239281120&cageCode=268&type=prematch&groupId=1000093883&pageNr=1&pageSize=20&offset=0"
    bets_response = await client.request("GET", url)
    bets_response = bets_response.json()

    total_pages = bets_response.get("paging", {}).get("totalPages", 1)

    responses: list[dict] = [bets_response]

    for i in range(2, total_pages + 1):
        queries = url.split("&")
        queries[-3] = f"pageNr={i}"
        url = "&".join(queries)

        bets_response = await client.request("GET", url)
        bets_response = bets_response.json()

        responses.append(bets_response)

    return responses


async def parse_responses(data: list[dict]):
    all_bets: list = []

    for response in data:
        events = response.get("items", [])

        for event in events:
            offers = event.get("betOffers", [])

            names = event.get("participants", [])
            names = [names[0].get("name", ""), names[1].get("name", "")]
            for j, n in enumerate(names):
                temp = n.strip(" ").split(",")
                names[j] = " ".join(reversed(temp)).strip()

            for offer in offers:
                if offer.get("betDescription", "") == "Moneyline":
                    outcomes = offer.get("outcomes", [])

            if not outcomes:
                continue
            pair = []

            for i, outcome in enumerate(outcomes):
                odds = int(outcome.get("oddsAmerican", 0))
                name = names[i]
                bet = Betline(name, odds)
                pair.append(bet)

            pair[0].matchup, pair[1].matchup = pair[1], pair[0]
            all_bets += pair
    return all_bets


async def scrape_betriver(url: str = None):
    bets_data = await request_betriver(url)
    all_bets = await parse_responses(bets_data)
    return all_bets


if __name__ == "__main__":
    url = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=202310181910&cageCode=268&type=live&type=prematch&groupId=1000093656&pageNr=1&pageSize=10&offset=0"
    res = asyncio.run(scrape_betriver(url))
    debug(res)
