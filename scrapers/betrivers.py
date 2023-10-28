import requests
from devtools import debug
import json
import asyncio
from write import Betline


async def request_betriver(num_requests: int = None):
    url = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=20239281120&cageCode=268&type=prematch&groupId=1000093883&pageNr=1&pageSize=20&offset=0"
    bets_response = requests.request("GET", url)
    bets_response = bets_response.json()

    total_pages = bets_response.get("paging", {}).get("totalPages", 1)

    responses: list[dict] = [bets_response]

    for i in range(2, total_pages + 1):
        url = f"https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=20239281120&cageCode=268&type=prematch&groupId=1000093883&pageNr={i}&pageSize=20&offset=0"

        bets_response = requests.request("GET", url)
        bets_response = bets_response.json()

        responses.append(bets_response)

    return responses


def parse_responses(data: list[dict]):
    all_bets: list = []

    for response in data:
        events = response.get("items", [])

        for event in events:
            outcomes = event.get("betOffers", [])[0].get("outcomes", [])
            pair = []

            for outcome in outcomes:
                odds = int(outcome.get("oddsAmerican", 0))
                name = outcome.get("label", "").strip(" ").split(",")
                name = " ".join(reversed(name)).strip()
                bet = Betline(name, odds)
                pair.append(bet)

            pair[0].matchup, pair[1].matchup = pair[1], pair[0]
            all_bets += pair
    return all_bets


async def scrape_betriver():
    bets_data = await request_betriver()
    all_bets = parse_responses(bets_data)
    return all_bets


if __name__ == "__main__":
    asyncio.run(scrape_betriver())
