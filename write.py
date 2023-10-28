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

    # reorder so pinnacle is first sportsbook
    col_list = df.columns.to_list()
    col_list.remove("pinnacle")
    col_list.insert(-2, "pinnacle")
    df = df[col_list]
    print(df)

    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1")
    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format(
        {'bg_color': '#FFC7CE', 'font_color': '#9C0006'}
    )
    # Set the conditional format range.
    start_row = 1
    start_col = len(df.columns) - 1
    end_row = len(df)
    end_col = start_col

    # Apply a conditional format to the cell range.
    worksheet.conditional_format(
        start_row, start_col, end_row, end_col, {
            'type': 'cell',
            'criteria': '>',
            'value': 2,
            'format': format1
        }
    )
    writer._save()


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
