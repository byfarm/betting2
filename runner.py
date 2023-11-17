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


async def main():
    async with asyncio.TaskGroup() as tg:
        fanduel = tg.create_task(scrape_fanduel())
        pinnacle = tg.create_task(scrape_pinnacle())
        draftkings = tg.create_task(scrape_draftkings())
        mgm = tg.create_task(scrape_mgm())
        betriver = tg.create_task(scrape_betriver())
        ceasers = tg.create_task(scrape_ceasers())
        pointsbet = tg.create_task(scrape_pointsbet())

    big_dict = combine_data(
        fanduel=fanduel.result(),
        pinnacle=pinnacle.result(),
        draftkings=draftkings.result(),
        mgm=mgm.result(),
        betriver=betriver.result(),
        ceasers=ceasers.result(),
        pointsbet=pointsbet.result()
    )
    calc_evs(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
