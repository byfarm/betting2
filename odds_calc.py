BET = 100


def american_to_percentage(american_odd: int) -> float:

    if american_odd > 0:
        american_odd += 100
        percentage: float = 100 / american_odd
    else:
        denomenator = -american_odd + 100
        percentage: float = -american_odd / denomenator

    return percentage


def expected_value(percentage: float):
    return BET * percentage


if __name__ == "__main__":
    percentage = american_to_percentage(-300)
    print(percentage)
