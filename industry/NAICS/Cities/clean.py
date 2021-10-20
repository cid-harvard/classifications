import pandas as pd
import numpy as np

INPUT_FILE = "./in/2017_naics_code.csv"
SECTOR_FILE = "./in/gl_naics_sectors.csv"

LEVEL_STARTS = {1: 0, 2: 50, 3: 100, 4: 500, 5: 1000, 6: 2000}

# Load data and rename columns
df = pd.read_csv(INPUT_FILE)
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

# Add in GL-created 1-digit sector level
sector = pd.read_csv(SECTOR_FILE)
sector["level"] = 1

df = df.append(sector[["code", "title", "level"]].drop_duplicates())

df = df.merge(
    sector[["code", "child_code"]],
    how="left",
    left_on="code",
    right_on="child_code",
    suffixes=("", "_sector"),
)

df.loc[df.level == 2, "parent_code"] = df.code_sector
df = df.drop(columns=["code_sector", "child_code"])

# Assign naics_id values based on level
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

# Add parent_naics_id in addition to parent_code
parents = df[["naics_id", "code"]].rename(
    columns={"naics_id": "parent_id", "code": "parent_code"}
)
df = (
    df.merge(parents, on="parent_code", how="left")[
        [
            "naics_id",
            "code",
            "title",
            "level",
            "parent_id",
            "parent_code",
            "code_hierarchy",
            "naics_id_hierarchy",
        ]
    ]
    .sort_values("naics_id")
    .rename(columns={"title": "name"})
)

# Output cleaned files
df.to_csv("./out/naics_2017.csv", index=False)
df.to_json("./out/naics_2017.json", orient="records")
