import json
from devtools import debug
import requests
from datetime import datetime
from write import write_to_csv, Betline


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


async def pinnacle_request():
    # set urls and api key
    bets_url = "https://guest.api.arcadia.pinnacle.com/0.1/sports/22/markets/straight?primaryOnly=false&withSpecials=false"

    matchups_url = "https://guest.api.arcadia.pinnacle.com/0.1/sports/22/matchups?withSpecials=false&brandId=0"

    headers = {"X-Api-Key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R"}

    # get the betting response
    bets_response = requests.request("GET", bets_url, headers=headers)
    matchups_response = requests.request("GET", matchups_url, headers=headers)
    return bets_response, matchups_response


def pinnacle_parse(bets_response: dict, matchups_response: dict):
    bets: dict = bets_response.json()
    matchups: dict = matchups_response.json()

    all_bets: dict = {}
    for bet in bets:
        id = bet.get("matchupId", "")
        moneyline = Moneyline(bet)
        all_bets[id] = moneyline

    all_matchups: set = []
    for matchup in matchups:
        match = PinnacleMatchup(data=matchup)
        s1 = Betline(match.home, all_bets[match.id].bet1)
        s2 = Betline(match.away, all_bets[match.id].bet2)
        s1.matchup, s2.matchup = s2, s1
        all_matchups.append(s1)
        all_matchups.append(s2)
    return all_matchups


async def scrape_pinnacle():
    bets_response, matchups_response = await pinnacle_request()
    all_matchups = pinnacle_parse(bets_response, matchups_response)
    return all_matchups


if __name__ == "__main__":
    bets_response, matchups_response = pinnacle_request()
    all_matchups = pinnacle_parse(bets_response, matchups_response)
    write_to_csv(all_matchups)
