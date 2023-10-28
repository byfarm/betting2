import json
from scrapers.fanduel import scrape_fanduel
from scrapers.pinnacle import scrape_pinnacle
from scrapers.draftkings import scrape_draftkings
from scrapers.mgm import scrape_mgm
from write import combine_data, write_to_csv
import asyncio
from plus_ev import calc_evs
from devtools import debug


async def main():
    fanduel = await scrape_fanduel()
    pinnacle = await scrape_pinnacle()
    draftkings = await scrape_draftkings()
    mgm = await scrape_mgm()
    big_dict = combine_data(
        fanduel=fanduel,
        pinnacle=pinnacle,
        draftkings=draftkings,
        mgm=mgm,
    )
    calc_evs(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
