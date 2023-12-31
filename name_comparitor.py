import pandas as pd
from devtools import debug
names_db: list[list[str]] = []
nfl_enum = pd.read_csv("~/coding/python/betting/enums.csv")
nba_enum = pd.read_csv("~/coding/python/betting/NBA.csv")


def check_names(names_to_check: list[str], name_index: int = None):
    """checks a list of names to see if they are in the db"""
    if not name_index:
        name_index = 1

    matches = []
    for name in names_to_check:
        # switch names to lowercase
        name = name.lower()

        name_lis: list[str] = name.split(" ")
        for idx, good_name in enumerate(names_db):
            name_match: int = 0
            for single_name in name_lis:
                if single_name in good_name:
                    name_match += 1

            if name_match > name_index:
                matches.append(True)
                if len(name_lis) > len(good_name):
                    names_db[idx] = name_lis
                break
            else:
                matches.append(False)

    return matches


def check_single_name(name: str, name_index: int = None):
    """Checks to see if a single name is in the names db"""
    name = name.lower()
    if not name_index:
        name_index = 1

    name_lis: list[str] = name.split(" ")
    for idx, good_name in enumerate(names_db):
        name_match: int = 0
        for single_name in name_lis:
            if single_name in good_name:
                name_match += 1

        if name_match > name_index:
            # if len(name_lis) > len(good_name):
            #     names_db[idx] = name_lis
            return " ".join(names_db[idx])

    return False


def add_names(names: list[str]):
    """
    adds a list of names into the db
    """
    for name in names:
        if namecheck(name, nfl_enum["Name"]):
            idx = list(nfl_enum["Name"]).index(name)
            name += " " + list(nfl_enum["Abbreviation"])[idx]

        elif namecheck(name, nba_enum["name"]):
            idx = list(nba_enum["name"]).index(name)
            name += " " + list(nba_enum["prefix_1"])[idx]

        name = name.lower()
        names_db.append(name.split(" "))
    # debug(names_db)


def namecheck(name, lis):
    for r in lis:
        if r == name:
            return True
    return False


if __name__ == "__main__":
    names_in = ["byron farmar"]
    names_check = ["byron george Farmar", "sarah Jones", "Byron Jones"]
    add_names(names_check)
    debug(names_db)
    boolien = check_single_name(names_in[0])
    debug(names_db)
    debug(boolien)
