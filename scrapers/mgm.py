from scrapers.request_client import client
import json
import asyncio
from devtools import debug
from write import Betline


async def request_mgm_ids(url: str = None):
    if not url:
        url = "https://sports.co.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small&page=SportLobby&sportId=45&widgetId=/mobilesports-v1.0/layout/layout_us/modules/ufc/mmalobby&shouldIncludePayload=true"
    headers = {
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    event_id_response = await client.request("GET", url, headers=headers)
    if event_id_response.status_code != 200:
        raise Exception(
            f"status code {event_id_response.satatus_code} in request"
        )

    event_id_response = event_id_response.json()

    secondary_navigation: list = (
        event_id_response.get("widgets", [])[0]
        .get("payload", {})
        .get("secondaryNavigation", [])
    )
    ids = [event.get("id", "") for event in secondary_navigation]
    return ids


async def request_mgm_odds(id: str):
    url = f"https://sports.co.betmgm.com/en/sports/api/widget/widgetdata?layoutSize=Small&page=SportLobby&sportId=45&competitionId={id}&widgetId=/mobilesports-v1.0/layout/layout_us/modules/ufc/mmalobby&shouldIncludePayload=true"
    headers = {
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    bet_response = await client.request("GET", url, headers=headers)
    if bet_response.status_code != 200:
        raise Exception(f"status code {bet_response.satatus_code} in request")

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


async def scrape_mgm(url: str = None):
    ids = await request_mgm_ids(url)
    bet_responses = [request_mgm_odds(id) for id in ids]
    bet_responses = await asyncio.gather(*bet_responses)

    all_bets = []
    for response in bet_responses:
        bets = parse_mgm(response)
        all_bets += bets

    return all_bets

if __name__ == "__main__":
    asyncio.run(scrape_mgm())
