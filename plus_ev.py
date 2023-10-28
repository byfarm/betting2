from odds_calc import american_to_percentage
from devtools import debug


def plus_ev(probability: float, true_probability: float):
    return probability - true_probability


def calc_evs(big_dict: dict):
    for name, books in big_dict.items():
        ev_names: list = []
        evs: list = []
        for book in books:
            if book == "opponent" or book == "pinnacle":
                continue
            ev: float = plus_ev(
                american_to_percentage(books[book]),
                american_to_percentage(big_dict[name]["pinnacle"])
            )
            evs.append(ev)
            ev_names.append(book)

        best_ev = max(evs)
        big_dict[name]["ev"] = round(100 * best_ev, 2)

        if best_ev == 0:
            big_dict[name]["ev_book"] = ""
        else:
            index = evs.index(best_ev)
            big_dict[name]["ev_book"] = ev_names[index]
