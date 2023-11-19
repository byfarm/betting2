from scrapers.request_client import client
import json
import asyncio
from devtools import debug
from write import Betline


async def draftkings_request(url: str = None):
    if not url:
        url = "https://sportsbook-us-tl.draftkings.com/sites/US-WATL-SB/api/v5/eventgroups/9034?format=json"
    response = await client.request("GET", url)
    json_data = response.json()

    return json_data


async def parse_draftkings(json_data: dict):
    bet_offers: list = (
        json_data.get("eventGroup", {})
        .get("offerCategories", [])[0]
        .get("offerSubcategoryDescriptors", [])[0]
        .get("offerSubcategory", {})
        .get("offers", [])
    )

    all_bets: list = []
    for offer in bet_offers:
        try:
            section = [sec for sec in offer if sec.get("label") == "Moneyline"][0]
        except IndexError:
            continue

        matchup: list = []
        for player in section.get("outcomes", []):
            name = player.get("label", "")
            odds = int(player.get("oddsAmerican", 0))
            if name in [x.name for x in all_bets]:
                continue
            bet = Betline(name, odds)
            matchup.append(bet)

        if len(matchup) == 2:
            matchup[0].matchup, matchup[1].matchup = matchup[1], matchup[0]
            all_bets += matchup

    return all_bets


async def scrape_draftkings(url: str = None):
    data = await draftkings_request(url)
    matchups = await parse_draftkings(data)
    return matchups


if __name__ == "__main__":
    url = "https://sportsbook-us-co.draftkings.com/sites/US-CO-SB/api/v5/eventgroups/88808?format=json"
    # url = None
    res = asyncio.run(scrape_draftkings(url))
    debug(res)
