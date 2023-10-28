import pandas as pd
from odds_calc import american_to_percentage
from devtools import debug


def write_to_csv(big_dict: dict):
    put_in: dict = {"names": []}
    for name, value in big_dict.items():
        put_in["names"].append(name)

        for site, odd in value.items():
            if site == "opponent":
                continue
            if not put_in.get(site, None):
                put_in[site] = []

            put_in[site].append(odd)
    df = pd.DataFrame(put_in)
    df.to_excel("data.xlsx")


def combine_data(**kwargs):
    big_dict = {}
    for key, value in kwargs.items():
        for val in value:
            if not big_dict.get(val.name, None):
                big_dict[val.name] = {}
            big_dict[val.name][key] = val.odds
            big_dict[val.name]["opponent"] = val.matchup

    # fileter out non-matching names
    bad_ones = set()
    for name, values in big_dict.items():
        if len(values.values()) - 1 < len(kwargs.keys()):
            bad_ones.add(name)

    for namer in bad_ones:
        del big_dict[namer]

    return big_dict


class Betline:

    matchup = None

    def __init__(self, name: str, odds: dict):
        self.name: str = name
        self.odds: dict = odds

    def __repr__(self):
        return f"{self.name}: {self.odds}"
