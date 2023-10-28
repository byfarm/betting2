import requests
import json
import asyncio
from devtools import debug
from write import Betline


async def request_mgm_ids():
    url = "https://sports.co.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small&page=SportLobby&sportId=45&widgetId=/mobilesports-v1.0/layout/layout_us/modules/ufc/mmalobby&shouldIncludePayload=true"
    headers = {
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    event_id_response = requests.request("GET", url, headers=headers)

    event_id_response = event_id_response.json()

    secondary_navigation: list = (
        event_id_response.get("widgets", [])[0]
        .get("payload", {})
        .get("secondaryNavigation", [])
    )
    ids = [event.get("id", "") for event in secondary_navigation]
    return ids


def request_mgm_odds(id: str):
    url = f"https://sports.co.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small&page=SportLobby&sportId=45&competitionId={id}&widgetId=/mobilesports-v1.0/layout/layout_us/modules/ufc/mmalobby&shouldIncludePayload=true"
    headers = {
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    bet_response = requests.request("GET", url, headers=headers)

    bet_response = bet_response.json()
    return bet_response


def parse_mgm(api_response: dict):
    fixtures: list = (
        api_response.get("widgets", [])[0]
        .get("payload", {})
        .get("fixtures", [])
    )
    all_fights = []
    for fixture in fixtures:
        games = fixture.get("games", {})
        for game in games:
            results = game.get("results", [])
            pair = []

            for result in results:
                odd: int = result.get("americanOdds", 0)
                name = result.get("name", {}).get("value", "").split(".")[-1]
                bet = Betline(name, odd)
                pair.append(bet)

            pair[0].matchup, pair[1].matchup = pair[1], pair[0]

            for participant in fixture.get("participants", []):
                name = participant.get("name", {}).get("value", "")
                for bet in pair:
                    if bet.name in name:
                        bet.name = " ".join(name.split(" ")[:-1])

            all_fights += pair

    return all_fights


async def scrape_mgm():
    ids = await request_mgm_ids()
    bet_responses = map(request_mgm_odds, ids)

    all_bets = []
    for response in bet_responses:
        bets = parse_mgm(response)
        all_bets += bets

    return all_bets

if __name__ == "__main__":
    asyncio.run(scrape_mgm())
