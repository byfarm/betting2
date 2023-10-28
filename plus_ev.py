from odds_calc import american_to_percentage
from devtools import debug


def plus_ev(probability: float, true_probability: float):
    return probability - true_probability


def calc_evs(big_dict: dict):
    for name, books in big_dict.items():
        evs: list = []
        for book in books:
            if book == "opponent":
                continue
            ev: float = plus_ev(
                american_to_percentage(books[book]),
                american_to_percentage(big_dict[name]["pinnacle"])
            )
            evs.append(ev)
        big_dict[name]["ev"] = round(100 * max(evs), 2)
