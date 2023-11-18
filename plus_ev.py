from odds_calc import american_to_percentage
from devtools import debug


def expected_value(probability: float, true_probability: float):
    """
    calculates the expected value of a bet
    """
    return probability - true_probability


def calc_evs(big_dict: dict):
    """
    Calculates the best ev from the sportsbooks
    """
    for name, books in big_dict.items():
        ev_names: list = []
        evs: list = []
        for book in books:
            if book == "opponent" or book == "Pinnacle":
                continue
            ev: float = expected_value(
                american_to_percentage(books[book]),
                american_to_percentage(big_dict[name]["Pinnacle"])
            )
            evs.append(-ev)
            ev_names.append(book)

        best_ev = max(evs)
        big_dict[name]["ev"] = round(100 * best_ev, 2)

        # if best_ev == 0:
        #     big_dict[name]["ev_book"] = ""
        # else:
        #     index = evs.index(best_ev)
        #     big_dict[name]["ev_book"] = ev_names[index]
