import pandas as pd

from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    Classification,
)

if __name__ == "__main__":

    df = (
        pd.read_csv(
            "./in/Mexico Country codes - continents - Countries.csv",
            encoding="utf-8",
            dtype={"continent_code": str},
        )
        .rename(columns={"continent_code": "parent_code"})
        .drop("total_export", axis=1)
    )
    df["level"] = "country"

    regions = pd.read_table(
        "./in/Mexico Country codes - continents - Continents - Regions.tsv",
        encoding="utf-8",
    ).rename(columns={"name": "name_en"})
    regions["name_short_en"] = regions["name_en"]
    regions["name_short_es"] = regions["name_es"]
    regions["level"] = "region"
    regions["code"] = regions["code"].astype(unicode)

    df = pd.concat([df, regions]).reset_index(drop=True)

    h = Hierarchy(["region", "country"])
    parent_id_table = parent_code_table_to_parent_id_table(df, h)
    parent_id_table["name"] = parent_id_table["name_en"]

    c = Classification(parent_id_table, h)
    c.to_csv("out/locations_international_mexico.csv")
    c.to_stata("out/locations_international_mexico.dta")
