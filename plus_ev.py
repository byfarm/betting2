from odds_calc import american_to_percentage, decimal_to_american
from devtools import debug
from numba import jit


betamount = 100


@jit(nopython=True)
def expected_value(probability: float, true_probability: float):
    """
    calculates the expected value of a bet
    """
    amercian_prob = decimal_to_american(1/probability)
    if amercian_prob < 0:
        payout = (100 / -amercian_prob)
    else:
        payout = amercian_prob / 100
    ev = true_probability * payout - (1 - true_probability)
    return ev * 100


def novig(odd1: int, odd2: int):
    """Calculates the no vig odds from pinnacle"""
    odd1 = american_to_percentage(odd1)
    odd2 = american_to_percentage(odd2)
    novig1 = odd1/(odd1 + odd2)
    novig2 = odd2/(odd1 + odd2)
    return novig1, novig2


def calc_evs(big_dict: dict):
    """
    Calculates the best ev from the sportsbooks
    """
    debug(big_dict)
    found = set()
    for k, v in big_dict.items():

        if k in found:
            continue
        no1, no2 = novig(
            big_dict[k]["Pinnacle"],
            big_dict[big_dict[k]["opponent"].title()]["Pinnacle"]
        )
        big_dict[k]["Pinnacle"] = decimal_to_american(1/no1)
        big_dict[big_dict[k]["opponent"].title()]["Pinnacle"] = decimal_to_american(1/no2)
        found.add(k)
        found.add(big_dict[k]["opponent"])

    for name, books in big_dict.items():
        ev_names: list = []
        evs: list = []
        kellies: list = []
        for book in books:
            if book == "opponent" or book == "Pinnacle":
                continue
            ev: float = expected_value(
                american_to_percentage(books[book]),
                american_to_percentage(big_dict[name]["Pinnacle"])
            )
            kell: float = kelly(
                american_to_percentage(books[book]),
                american_to_percentage(big_dict[name]["Pinnacle"])
            )
            kellies.append(kell)
            evs.append(ev)
            ev_names.append(book)

        best_ev = max(evs)
        i = evs.index(best_ev)
        kelly_number = kellies[i]
        big_dict[name]["Kelly"] = round(kelly_number, 2)
        big_dict[name]["EV"] = round(best_ev, 2)

        # if best_ev == 0:
        #     big_dict[name]["ev_book"] = ""
        # else:
        #     index = evs.index(best_ev)
        #     big_dict[name]["ev_book"] = ev_names[index]


@jit(nopython=True)
def kelly(given_percent: float, true_percent: float):
    given_decimal = (1 / given_percent) - 1
    kellyn = (given_decimal * true_percent - (1 - true_percent)) / given_decimal
    return kellyn * betamount


if __name__ == "__main__":
    odd1 = +324
    odd2 = -395
    print(novig(odd1, odd2))
