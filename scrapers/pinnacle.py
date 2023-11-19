import json
from devtools import debug
from scrapers.request_client import client
from datetime import datetime
from write import Betline
from name_comparitor import add_names


class PinnacleMatchup:

    bet1: int
    bet2: int

    def __init__(self, data: dict):
        participant1 = data.get("participants", [])[0]
        participant2 = data.get("participants", [])[1]

        self.home, self.away = None, None

        if participant1.get("alignment") == "home":
            self.home = participant1.get("name")
        else:
            self.away = participant1.get("name")

        if self.home:
            self.away = participant2.get("name")
        else:
            self.home = participant2.get("name")

        self.id = data.get("id", "")

        time: str = data.get("periods", [])[0].get("cutoffAt")
        date_format: str = '%Y-%m-%dT%H:%M:%SZ'
        self.start_time = datetime.strptime(time, date_format)

    def __repr__(self):
        return f"{self.home}, {self.away}, {self.id}"


class Moneyline:
    def __init__(self, data: dict):
        self.bet1, self.bet2 = None, None

        participant2 = data.get("prices", [])[1]
        participant1 = data.get("prices", [])[0]

        if participant1.get("designation", "") == "home":
            self.bet1 = participant1.get("price", 0)
        else:
            self.bet2 = participant1.get("price", 0)

        if self.bet2:
            self.bet1 = participant2.get("price", 0)
        else:
            self.bet2 = participant2.get("price", 0)

    def __repr__(self):
        return f"{self.bet1}, {self.bet2}"


async def pinnacle_request(url: str = None):
    headers = {"X-Api-Key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R"}

    # set urls and api key
    if not url:
        url = "https://guest.api.arcadia.pinnacle.com/0.1/sports/22/markets/straight?primaryOnly=false&withSpecials=false"

    # get the betting response
    bets_response = await client.request("GET", url, headers=headers)

    if bets_response.status_code != 200:
        raise Exception(
            f"status code {bets_response.satatus_code} in request"
        )

    splitted = "/".join(url.split("?")[0].split("/")[:-2])
    url = splitted + "/matchups?brandId=0"

    matchups_response = await client.request(
        "GET", url, headers=headers
    )

    if matchups_response.status_code != 200:
        raise Exception(
            f"status code {matchups_response.satatus_code} in request"
        )

    return bets_response, matchups_response


async def pinnacle_parse(bets_response: dict, matchups_response: dict):
    """
    parse through both responses and match up the bets witht the correct player
    """
    bets: dict = bets_response.json()
    matchups: dict = matchups_response.json()

    # putht the odds into an id dict
    all_bets: dict = {}
    for bet in bets:
        if not bet.get("type", "") == "moneyline":
            continue
        if not bet.get("period") == 0:
            continue
        if len(bet.get("prices", [])) < 2:
            continue
        if "points" in bet.get("prices", {})[0].keys():
            continue

        id = bet.get("matchupId", "")
        moneyline = Moneyline(bet)
        try:
            all_bets[id]
        except KeyError:
            all_bets[id] = moneyline
    #     try:
    #         all_bets[id] += [bet]
    #     except KeyError:
    #         all_bets[id] = [bet]
    # for k, r in all_bets.items():
    #     if len(r) > 1:
    #         debug(k, r)

    # find the matchups and pair them with their ids
    all_matchups: set = []
    for matchup in matchups:
        if matchup.get("participants")[0].get("alignment", "") == "neutral":
            continue
        match = PinnacleMatchup(data=matchup)
        try:
            s1 = Betline(match.home, all_bets[match.id].bet1)
            s2 = Betline(match.away, all_bets[match.id].bet2)
        except KeyError:
            continue
        s1.matchup, s2.matchup = s2, s1
        all_matchups.append(s1)
        all_matchups.append(s2)

    # add all the names to the names database
    names = [match.name for match in all_matchups]
    add_names(names)

    return all_matchups


async def scrape_pinnacle(url: str = None):
    bets_response, matchups_response = await pinnacle_request(url)
    all_matchups = await pinnacle_parse(bets_response, matchups_response)
    return all_matchups


if __name__ == "__main__":
    url = "https://guest.api.arcadia.pinnacle.com/0.1/leagues/889/markets/straight"
    import asyncio
    res = asyncio.run(scrape_pinnacle(url))
    debug(res)
