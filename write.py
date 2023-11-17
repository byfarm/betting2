import pandas as pd
from odds_calc import american_to_percentage
from devtools import debug
from name_comparitor import check_single_name


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
    col_list.insert(-1, "pinnacle")
    df = df[col_list]

    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a format.
    red_background = workbook.add_format(
        {'bg_color': '#FFC7CE'}
    )
    green_background = workbook.add_format(
        {'bg_color': '#ADFFAD'}
    )
    bottom_boarder = workbook.add_format(
        {
            "bottom": 2,
            "bottom_color": "#000000"
        }
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
            'value': 1.5,
            'format': red_background
        }
    )

    # write green_background for best bets for each player
    max_df = df[col_list[1:-2]]
    for idx, row in max_df.iterrows():
        row_min = row.max()
        col_index = list(row).index(row_min)
        worksheet.write(1 + idx, 1 + col_index, row_min, green_background)

        # write in boarders between matchups
        if idx % 2 == 0:
            for i, name in enumerate(df.columns):
                worksheet.conditional_format(
                    idx, i, idx, i, {
                        "type": "cell",
                        "criteria": "!=",
                        "value": "3.14159",
                        "format": bottom_boarder
                    }
                )
    writer._save()


def combine_data(**kwargs):
    big_dict = {}
    for key, value in kwargs.items():
        for val in value:
            # get the name stored in the database
            name = check_single_name(val.name)
            opp_name = check_single_name(val.matchup.name)

            # if the matchup not in, skip
            if not name or not opp_name:
                continue

            name = name.title()
            if not big_dict.get(name, None):
                big_dict[name] = {}

            big_dict[name][key] = val.odds
            big_dict[name]["opponent"] = val.matchup

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
