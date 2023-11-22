from scrapers.request_client import client
from devtools import debug
import json
import asyncio
from write import Betline
import datetime


async def request_betriver(url: str = None):
    if not url:
        url = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=20239281120&cageCode=268&type=prematch&groupId=1000093883&pageNr=1&pageSize=20&offset=0"
    bets_response = await client.request("GET", url)
    bets_response = bets_response.json()

    total_pages = bets_response.get("paging", {}).get("totalPages", 1)

    responses: list[dict] = [bets_response]

    async_reses: list = []
    async with asyncio.TaskGroup() as tg:
        for i in range(2, total_pages + 1):
            queries = url.split("&")
            queries[-3] = f"pageNr={i}"
            url = "&".join(queries)

            bets_response = tg.create_task(client.request("GET", url))
            async_reses.append(bets_response)

    for res in async_reses:
        ar = res.result().json()

        responses.append(ar)

    return responses


async def parse_responses(data: list[dict]):
    all_bets: list = []

    # currtime = (
    #     datetime.datetime.now(datetime.timezone.utc)
    #     .replace(tzinfo=None)
    #     + datetime.timedelta(days=5)
    # )
    # baddays = {"Thu", "Fri"}
    for response in data:
        events = response.get("items", [])

        for event in events:
            offers = event.get("betOffers", [])

            names = event.get("participants", [])
            names = [names[0].get("name", ""), names[1].get("name", "")]
            name_seen = [None, None]
            for j, n in enumerate(names):
                temp = n.strip(" ").split(",")
                names[j] = " ".join(reversed(temp)).strip()
                name_seen[j] = names[j] in [x.name for x in all_bets]

            # date_obj = datetime.datetime.strptime(
            #     event.get("start"), "%Y-%m-%dT%H:%M:%S.%fZ"
            # )
            # # print(date_obj.strftime("%a"))
            # if event.get("eventInfo")[-1].get("name", "") == "NFL":
            #     if (date_obj > currtime) or date_obj.strftime("%a") in baddays:
            #         continue
            if True in name_seen:
                continue

            outcomes = None
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
    url = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?t=202310211550&cageCode=268&type=live&type=prematch&groupId=1000093652&pageNr=1&pageSize=10&offset=0"
    res = asyncio.run(scrape_betriver(url))
    debug(res)
