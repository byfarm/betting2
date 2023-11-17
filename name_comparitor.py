names_db: list[list[str]] = []


def check_names(names_to_check: list[str]):
    """checks a list of names to see if they are in the db"""
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

            if name_match > 1:
                matches.append(True)
                if len(name_lis) > len(good_name):
                    names_db[idx] = name_lis
                break
            else:
                matches.append(False)

    return matches


def check_single_name(name: str):
    """Checks to see if a single name is in the names db"""
    name = name.lower()

    name_lis: list[str] = name.split(" ")
    for idx, good_name in enumerate(names_db):
        name_match: int = 0
        for single_name in name_lis:
            if single_name in good_name:
                name_match += 1

        if name_match > 1:
            # if len(name_lis) > len(good_name):
            #     names_db[idx] = name_lis
            return " ".join(names_db[idx])

    return False


def add_names(names: list[str]):
    """
    adds a list of names into the db
    """
    for name in names:
        name = name.lower()
        names_db.append(name.split(" "))


if __name__ == "__main__":
    from devtools import debug
    names_in = ["byron farmar"]
    names_check = ["byron george Farmar", "sarah Jones", "Byron Jones"]
    add_names(names_check)
    debug(names_db)
    boolien = check_single_name(names_in[0])
    debug(names_db)
    debug(boolien)
