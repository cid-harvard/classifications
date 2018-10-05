import pandas as pd
import babel

from classification import (
    Hierarchy,
    parent_code_table_to_parent_id_table,
    Classification,
)

if __name__ == "__main__":

    df = pd.read_csv(
        "./in/wikipedia-iso-country-codes.csv",
        encoding="utf-8",
        dtype={"Numeric code": str},
        na_values=None,
        keep_default_na=False,
    )
    df.columns = ["name_short_en", "code_alpha2", "code_alpha3", "code_numeric", "link"]

    df = df[["code_alpha2", "code_alpha3", "code_numeric"]]

    df = df.sort_values("code_alpha3").reset_index(drop=True)

    # Merge in customary names in different languages from babel (Unicode CLDR)
    en_names = pd.DataFrame.from_dict(
        dict(babel.Locale.parse("en_US").territories), orient="index"
    )
    en_names.columns = ["name_en"]
    df = df.merge(en_names, left_on="code_alpha2", right_index=True, how="left")

    es_names = pd.DataFrame.from_dict(
        dict(babel.Locale.parse("es_419").territories), orient="index"
    )
    es_names.columns = ["name_es"]
    df = df.merge(es_names, left_on="code_alpha2", right_index=True, how="left")

    # Merge in region codes
    alpha3_to_region = pd.read_csv(
        "./in/countries_to_regions.csv", dtype={"parent_code": str}
    )
    df = df.merge(alpha3_to_region, on="code_alpha3", how="left")

    # Add custom codes
    custom_codes = pd.read_csv("./in/custom-codes.csv", dtype={"parent_code": str})
    df = pd.concat([df, custom_codes]).reset_index(drop=True)

    df["level"] = "country"

    # Add region code level
    region_codes = pd.read_table("./in/regions.tsv", dtype={"code": str})
    region_codes["code_alpha2"] = region_codes["code"]
    region_codes["code_alpha3"] = region_codes["code"]
    region_codes["code_numeric"] = region_codes["code"]
    region_codes = region_codes.drop("code", axis=1)
    df = pd.concat([df, region_codes]).reset_index(drop=True)

    h = Hierarchy(["region", "country"])
    df["name"] = df["name_en"]
    df["code"] = df["code_alpha3"]
    df = parent_code_table_to_parent_id_table(df, h)

    # Alpha3 classification
    df["code"] = df["code_alpha3"]
    Classification(df, h).to_csv("out/locations_international_iso_cid.csv")
