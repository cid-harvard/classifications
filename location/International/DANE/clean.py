import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_stata("in/Colombia_countries_key.dta", encoding="mac-roman")
    df.columns = ["alpha3", "code", "name_es"]

    df = df[["alpha3", "code", "name_es"]]

    iso = pd.read_csv("../iso/in/wikipedia-iso-country-codes.csv", encoding="utf-8")
    iso = iso[["Alpha-3 code", "English short name (upper/lower case)"]]
    iso.columns = ["alpha3", "name"]

    df = df.merge(iso, on="alpha3", how="left")

    mex = pd.read_csv("../Mexico/Mexico Country codes - continents - Countries.csv")
    mex = mex[["code", "name_es", "name_short_es", "continent_code"]]

    df = df.merge(mex, how = "left", left_on = "alpha3", right_on = "code", suffixes=('_col', '_mex'))
    df = df[["alpha3", "code_col", "name_es_col", "name", "continent_code"]]

    missing = pd.read_table("../DANE/in/Colombia_countries_not_in_mexico.txt", encoding = "utf-16")
    missing = missing[["alpha3", "code_col", "name_es_col", "name", "continent_code"]]

    df = pd.concat([df, missing])
    df = df[~df.continent_code.isnull()].reset_index(drop = True)
    
    df["level"] = "country"
    
    df = df.rename(columns={
        "code_col": "code",
        "name_es_col": "name_es",
        "continent_code": "parent_code"
        })
        
    assert df.loc[6, "name"] is pd.np.nan
    df.loc[6, "name"] = u"Netherlands Antilles"
    
    regions = pd.read_table("./in/Mexico Country codes - continents - Continents - Regions.tsv", encoding="utf-8")
    df = pd.concat([df, regions]).reset_index(drop=True)
    
    h = Hierarchy(["region", "country"])
    parent_id_table = parent_code_table_to_parent_id_table(df, h)
    
    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_international_dane.csv")
    #c.to_stata("out/locations_international_dane.dta")
