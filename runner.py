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
    fanduel = asyncio.create_task(scrape_fanduel())
    pinnacle = asyncio.create_task(scrape_pinnacle())
    draftkings = asyncio.create_task(scrape_draftkings())
    mgm = asyncio.create_task(scrape_mgm())
    betriver = asyncio.create_task(scrape_betriver())
    ceasers = asyncio.create_task(scrape_ceasers())
    pointsbet = asyncio.create_task(scrape_pointsbet())
    await fanduel, await pinnacle, await draftkings, await mgm, \
        await betriver, await ceasers, await pointsbet
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
