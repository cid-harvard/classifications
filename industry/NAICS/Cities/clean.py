import pandas as pd
import numpy as np

INPUT_FILE = "./in/2017_naics_code.xlsx"

LEVEL_STARTS = {1: 1, 2: 50, 3: 100, 4: 500, 5: 1000, 6: 2000}

# Load data and rename columns
df = pd.read_excel(INPUT_FILE, usecols=2)
df = df[df.code.notna()]
df.code = df.code.astype(str)

# Set level based on length of NAICS code
# Range codes with - are all 2-digit
df["level"] = df.code.str.len()
df.loc[df.code.str.contains("-"), "level"] = 2

# NAICS parent codes are all but the last digit of the current code
df["parent_code"] = df.code.apply(lambda x: x[:-1])

for i, row in df[df.code.str.contains("-")].iterrows():
    start = row["code"][:2]
    end = row["code"][-2:]

    for n in range(int(start), int(end) + 1):
        df.loc[df.parent_code == str(n), "parent_code"] = f"{start}-{end}"

df.loc[df.level == 2, "parent_code"] = None

# Assign id values based on level
for i, g in df.groupby("level"):
    c = LEVEL_STARTS.get(i)
    df.loc[g.index, "naics_id"] = g.code.sort_values().rank() + c - 1

df.naics_id = df.naics_id.astype(int)

df["code_hierarchy"] = df.code.astype(str)
df["naics_id_hierarchy"] = df.naics_id.astype(str)

# Make hierarchy rows fit Postgres ltree standards
def format_hierarchy(df, column="code"):
    def _format(row):
        if row[f"{column}_hierarchy_parent"] is np.nan:
            return str(row[f"{column}"])
        return str(row[f"{column}_hierarchy_parent"]) + "." + str(row[f"{column}"])

    return df.apply(_format, axis=1)


# Built hierarchy columns
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

# Add parent_id in addition to parent_code
parents = df[["naics_id", "naics_code"]].rename(
    columns={"naics_id": "parent_id", "naics_code": "parent_code"}
)
df = df.merge(parents, on="parent_code", how="left")[
    [
        "naics_id",
        "naics_code",
        "title",
        "level",
        "parent_id",
        "parent_code",
        "code_hierarchy",
        "naics_id_hierarchy",
    ]
]

# Output cleaned files
df.to_csv("./out/naics_2017.csv", index=False)
df.to_json("./out/naics_2017.json", orient="records")
