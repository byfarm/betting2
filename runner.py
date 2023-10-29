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
    fanduel = await scrape_fanduel()
    pinnacle = await scrape_pinnacle()
    draftkings = await scrape_draftkings()
    mgm = await scrape_mgm()
    betriver = await scrape_betriver()
    ceasers = await scrape_ceasers()
    pointsbet = await scrape_pointsbet()
    big_dict = combine_data(
        fanduel=fanduel,
        pinnacle=pinnacle,
        draftkings=draftkings,
        mgm=mgm,
        betriver=betriver,
        ceasers=ceasers,
        pointsbet=pointsbet
    )
    calc_evs(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
