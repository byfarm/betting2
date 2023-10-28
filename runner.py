import json
from scrapers.fanduel import scrape_fanduel
from scrapers.pinnacle import scrape_pinnacle
from scrapers.draftkings import scrape_draftkings
from write import combine_data, write_to_csv
import asyncio
from plus_ev import calc_evs
from devtools import debug


async def main():
    fanduel = await scrape_fanduel()
    pinnacle = await scrape_pinnacle()
    draftkings = await scrape_draftkings()
    big_dict = combine_data(
        fanduel=fanduel,
        pinnacle=pinnacle,
        draftkings=draftkings,
    )
    calc_evs(big_dict)
    debug(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
