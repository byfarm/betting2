import json
from fanduel import scrape_fanduel
from pinnacle import scrape_pinnacle
from write import combine_data, write_to_csv
import asyncio
from plus_ev import calc_evs
from devtools import debug


async def main():
    fanduel = await scrape_fanduel()
    pinnacle = await scrape_pinnacle()
    big_dict = combine_data(fanduel=fanduel, pinnacle=pinnacle)
    calc_evs(big_dict)
    debug(big_dict)
    write_to_csv(big_dict)


if __name__ == "__main__":
    asyncio.run(main())
