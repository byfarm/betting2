from write import combine_data, write_to_csv
import asyncio
from plus_ev import calc_evs
from devtools import debug
from urls import url_db, scraping_functions
import sys


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
    write_to_csv(big_dict, f"{sport}.xlsx")


async def run_scraper():
    async with asyncio.TaskGroup() as tg:
        if len(sys.argv) > 1:
            for sport in sys.argv[1:]:
                tg.create_task(main(sport))
        else:
            tg.create_task(main())

if __name__ == "__main__":
    asyncio.run(run_scraper())

"""
Sports:
NFL
UFC
"""
