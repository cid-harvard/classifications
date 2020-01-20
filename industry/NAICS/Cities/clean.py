import pandas as pd
import numpy as np

input_file = "./in/2-6digit_2017_Codes.xlsx"

column_map = {
    "Seq. No.": "naics_id",
    "2017 NAICS US   Code": "code",
    "2017 NAICS US Title": "title",
}

df = pd.read_excel(input_file, usecols=2).rename(columns=column_map)
df = df[df.naics_id.notna()]
df.naics_id = df.naics_id.astype(int)
df.code = df.code.astype(str)

df["level"] = df.code.str.len()
df.loc[df.code.str.contains("-"), "level"] = 2

df["parent_code"] = df.code.apply(lambda x: x[:-1])

for i, row in df[df.code.str.contains("-")].iterrows():
    start = row["code"][:2]
    end = row["code"][-2:]

    for n in range(int(start), int(end) + 1):
        df.loc[df.parent_code == str(n), "parent_code"] = f"{start}-{end}"

df.loc[df.level == 2, "parent_code"] = None

df["code_hierarchy"] = df.code.astype(str)
df["naics_id_hierarchy"] = df.naics_id.astype(str)


def format_hierarchy(df, column="code"):
    def _format(row):
        if row[f"{column}_hierarchy_parent"] is np.nan:
            return str(row[f"{column}"])
        return str(row[f"{column}_hierarchy_parent"]) + "." + str(row[f"{column}"])

    return df.apply(_format, axis=1)


for i in range(5):
    df = df.merge(
        df, left_on="parent_code", right_on="code", suffixes=("", "_parent"), how="left"
    )

    df["code_hierarchy"] = format_hierarchy(df, "code")
    df["naics_id_hierarchy"] = format_hierarchy(df, "naics_id")

    df = df[
        [
            "naics_id",
            "code",
            "title",
            "level",
            "parent_code",
            "code_hierarchy",
            "naics_id_hierarchy",
        ]
    ]

df = df.rename(columns={"code": "naics_code"})
df.to_csv("./out/naics_2017.csv")
