import json
from scrapers.fanduel import scrape_fanduel
from scrapers.pinnacle import scrape_pinnacle
from scrapers.draftkings import scrape_draftkings
from scrapers.betrivers import scrape_betriver
from scrapers.ceasers import scrape_ceasers
from scrapers.mgm import scrape_mgm
from scrapers.pointsbet import scrape_pointsbet
from write import combine_data, write_to_csv
import asyncio
from plus_ev import calc_evs
from devtools import debug
from urls import url_db, scraping_functions


async def main(sport: str = None):
    if not sport:
        sport = "UFC"
    urls = url_db[sport]
    results = {}
    async with asyncio.TaskGroup() as tg:
        for key in urls.keys():
            results[key] = tg.create_task(scraping_functions[key](urls[key]))

    results = {key: result.result() for key, result in results.items()}
    big_dict = combine_data(sport, **results)
    calc_evs(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
