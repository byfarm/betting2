import pandas as pd
from devtools import debug
from name_comparitor import check_single_name


def write_to_csv(big_dict: dict, filepath: str):
    put_in: dict = {"Name": []}
    for name, value in big_dict.items():
        put_in["Name"].append(name)

        for site, odd in value.items():
            if site == "opponent":
                continue
            if not put_in.get(site, None):
                put_in[site] = []

            put_in[site].append(odd)

    df = pd.DataFrame(put_in)

    # reorder so pinnacle is first sportsbook
    col_list = df.columns.to_list()
    col_list.remove("Pinnacle")
    col_list.insert(-1, "Pinnacle")
    col_list.remove("Kelly")
    col_list.append("Kelly")
    df = df[col_list]

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
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
    start_col = len(df.columns) - 2
    end_row = len(df)
    end_col = start_col

    # Apply a red background format to the cell range.
    worksheet.conditional_format(
        start_row, start_col, end_row, end_col+1, {
            'type': 'cell',
            'criteria': '>',
            'value': 0.0,
            'format': red_background
        }
    )

    # write green_background for best bets for each player
    max_df = df[col_list[1:-3]]
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

    column_length = max(df["Name"].astype(str).map(len).max(), len(df["Name"]))
    writer.sheets['Sheet1'].set_column(0, 0, column_length)
    writer._save()


def combine_data(sport, **kwargs):
    name_indexes: dict = {
        "UFC": 1,
        "TEN": 0,
        "NFL": 1,
        "NBA": 1,
    }
    name_change = {
        "Los Angeles Rams": "Angeles LAR",
        "LA Rams": "Angeles LAR",
        "Los Angeles Chargers": "Angeles LAC",
        "LA Charger": "Angeles LAC",
        "NY Jets": "NYJ Jets",
        "New York Jets": "NYJ Jets",
        "NY Giants": "NYG Giants",
        "New York Giants": "NYG Giants",
        "LA Clippers": "LAC Clippers",
        "Los Angeles Clippers": "LAC Clippers",
        "LA Lakers": "LAL Lakers",
        "Los Anngeles Lakers": "LAL Lakers",
    }
    big_dict = {}
    for key, value in kwargs.items():
        for val in value:
            if val.matchup.name in name_change.keys():
                val.matchup.name = name_change[val.matchup.name]
            if val.name in name_change.keys():
                val.name = name_change[val.name]
            # get the name stored in the database
            name = check_single_name(val.name, name_indexes[sport])
            opp_name = check_single_name(val.matchup.name, name_indexes[sport])

            # if the matchup not in, skip
            if not name:
                # print(name, opp_name)
                # print(val.name, val.matchup.name)
                continue

            name = name.title()
            if not big_dict.get(name, None):
                big_dict[name] = {}

            if key not in big_dict[name].keys():
                big_dict[name][key] = val.odds
                big_dict[name]["opponent"] = val.matchup.name

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
