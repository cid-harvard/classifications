import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_stata("in/Colombia_countries_key.dta", encoding="mac-roman")
    df.columns = ["alpha3", "code", "name_es"]

    df = df[["alpha3", "code", "name_es"]]

    df["parent_code"] = pd.np.nan
    df["level"] = "country"

    iso = pd.read_csv("../iso/in/wikipedia-iso-country-codes.csv", encoding="utf-8")
    iso = iso[["Alpha-3 code", "English short name (upper/lower case)"]]
    iso.columns = ["alpha3", "name"]

    df = df.merge(iso, on="alpha3", how="left")

    assert df[df.name.isnull()].shape[0] == 4

    assert df.loc[7, "name"] is pd.np.nan
    df.loc[7, "name"] = "Netherlands Antilles"

    assert df.loc[192, "name"] is pd.np.nan
    df.loc[192, "name"] = "Serbia and Montenegro"

    assert df.loc[249, "name"] is pd.np.nan
    df.loc[249, "name"] = "Not Declared"

    assert df.loc[250, "name"] is pd.np.nan
    df.loc[250, "name"] = "Special Economic Zones"

    df.name = df.name.astype(unicode)

    h = Hierarchy(["country"])

    parent_id_table = parent_code_table_to_parent_id_table(df, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_international_dane.csv")
    c.to_stata("out/locations_international_dane.dta")
