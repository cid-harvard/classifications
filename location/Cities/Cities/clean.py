import numpy as np
import pandas as pd

GHS_FILE = "./in/GHS_STAT_UCDB2015MT_GLOBE_R2019A_V1_2.xls"
GHS_TAB = "Data"

INCLUDED_CITIES_FILE = "./in/included_cities.csv"
ATLAS_COUNTRIES_FILE = "../../International/Atlas/out/locations_international_atlas.csv"
UN_REGIONS_FILE = "./in/UNSD — Methodology.csv"

COLUMNS = {
    "ID_HDC_G0": "city_id",
    "UC_NM_MN": "name",
    "UC_NM_LST": "name_list",
    "CTR_MN_ISO": "country_iso",
    "GCPNT_LAT": "centroid_lat",
    "GCPNT_LON": "centroid_lon",
    "AREA": "area",
    "XBRDR": "cross_border",
    "XCTR_NBR": "num_countries",
    "XC_ISO_LST": "country_list",
}

REGIONS_COLUMNS = {
    "Region Name": "region_major",
    "Sub-region Name": "region_minor",
    "ISO-alpha3 Code": "iso_code",
}

if __name__ == "__main__":
    df = pd.read_excel(GHS_FILE, GHS_TAB).rename(columns=COLUMNS)[
        list(COLUMNS.values())
    ]

    df = df[df.city_id.notna()]
    df.city_id = df.city_id.astype(int)

    # Included Cities
    included = pd.read_csv(INCLUDED_CITIES_FILE)
    included.columns = ["city_id"]
    included["included"] = 1
    df = df.merge(included, on="city_id", how="left")
    df.included = df.included.fillna(0)

    # Countries
    ## Use Atlas country IDs
    countries = pd.read_csv(ATLAS_COUNTRIES_FILE, index_col=0)
    countries = (
        countries[countries.level == "country"][["code", "name_en", "name_short_en"]]
        .reset_index()
        .rename(columns={"index": "country_id"})
    )
    df = df.merge(
        countries[["code", "country_id"]],
        how="left",
        left_on="country_iso",
        right_on="code",
    ).drop(columns=["country_iso", "code"])

    # Regions
    regions = pd.read_csv(UN_REGIONS_FILE)

    regions = pd.read_csv(UN_REGIONS_FILE)[REGIONS_COLUMNS.keys()].rename(
        columns=REGIONS_COLUMNS
    )
    regions = regions.merge(
        countries[["country_id", "code"]],
        left_on="iso_code",
        right_on="code",
        how="left",
    ).drop(columns=["iso_code", "code"])

    region_ids = (
        regions[["region_major", "region_minor"]]
        .drop_duplicates()
        .sort_values(["region_major", "region_minor"])
        .reset_index(drop=True)
        .reset_index(drop=False)
        .rename(columns={"index": "region_id"})
    )

    region_ids.to_csv("./out/region.csv", index=False)

    # regions = (
    #     df[["region_major", "region_minor"]]
    #     .drop_duplicates()
    #     .sort_values(["region_major", "region_minor"])
    # ).reset_index(drop=True)
    # regions["region_id"] = regions.index
    # regions.to_csv("./out/region.csv", index=False)

    # df = df.merge(regions, on=["region_major", "region_minor"]).drop(
    #     columns=["region_major", "region_minor"]
    # )

    ## Set country_list to NaN when num_countries == 1
    df.loc[df.num_countries == 1, "country_list"] = np.NaN

    ## Assign country_ids to country_list

    ## Assign regions from GHS to Atlas country file
    country_regions = df[["country_id", "region_id"]].drop_duplicates()
    country_regions = country_regions[country_regions.country_id.notna()]
    ## France (77) has 4 regions, keep only Western Europe
    country_regions = country_regions[country_regions.country_id != 77]
    country_regions = country_regions.append(
        {
            "country_id": 77,
            "region_id": int(
                regions[regions.region_minor == "Western Europe"].region_id
            ),
        },
        ignore_index=True,
    )

    countries = countries.merge(country_regions, how="left", on="country_id")
    countries.to_csv("./out/country.csv", index=False)

    # Geometry

    # Save
    df.to_csv("./out/city.csv", index=False)
