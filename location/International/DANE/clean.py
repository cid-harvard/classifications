import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_stata("in/Colombia_countries_key.dta", encoding="mac-roman")
    df.columns = ["alpha3", "code", "name"]

    df = df[["alpha3", "code", "name"]]

    df["parent_code"] = pd.np.nan
    df["level"] = "country"

    iso = pd.read_csv("../iso/in/wikipedia-iso-country-codes.csv", encoding="utf-8")
    iso = iso[["Alpha-3 code", "English short name (upper/lower case)"]]
    iso.columns = ["alpha3", "name_en"]

    df = df.merge(iso, on="alpha3", how="left")

    h = Hierarchy(["country"])

    parent_id_table = parent_code_table_to_parent_id_table(df, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_international_dane.csv")
    c.to_stata("out/locations_international_dane.dta")
