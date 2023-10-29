from numba import jit


@jit(nopython=True)
def american_to_percentage(american_odd: int) -> float:

    if american_odd > 0:
        american_odd += 100
        percentage: float = 100 / american_odd
    else:
        denomenator = -american_odd + 100
        percentage: float = -american_odd / denomenator

    return percentage


@jit(nopython=True)
def decimal_to_american(decimal_odd: float) -> int:

    if decimal_odd >= 2:
        return round((decimal_odd - 1) * 100)
    else:
        return round(-100 / (decimal_odd - 1))


if __name__ == "__main__":
    percentage = american_to_percentage(-300)
    print(percentage)
