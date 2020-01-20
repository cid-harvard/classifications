import pandas as pd
import geopandas as gp

shape_file = "./in/nafta_metro.dbf"
region_file = "./in/nafta_region.parquet"
country_out_file = "../../International/Atlas/out/locations_international_atlas.csv"

remap_columns = {
    "GEOID": "geo_id",
    "GID_0": "country",
    "NAME": "name",
    "MTYPE": "geo_type",
    "geometry": "polygon",
    "center_lon": "center_y",
    "center_lat": "center_x",
    "region": "region",
}

metro_types = {
    "CAN": {"B": True, "D": False, "K": False},
    "USA": {"M1": True, "M2": False},
    "MEX": {"M1": True},
}

# Read files
msas = gp.read_file(shape_file).rename(columns=remap_columns).sort_values("country")
regions = pd.read_parquet(region_file)[
    ["GEOID", "center_lon", "center_lat", "region"]
].rename(columns=remap_columns)
country_class = pd.read_csv(country_out_file)

# Merge region and geometry files
msas = msas.merge(regions, on="geo_id", how="left")

# Distinguish between metro areas and micro areas
msas["metro"] = msas.apply(lambda x: metro_types[x.country][x.geo_type], axis=1)

# Initialize level column
msas["level"] = "msa"

# Insert rows for distinct countries
countries = country_class[country_class.code.isin(msas.country.drop_duplicates())][
    ["name_short_en", "code"]
].rename(columns={"name_short_en": "name", "code": "geo_id"})
countries["level"] = "country"

# Insert rows for distinct regions
regions = msas[msas.region.notna()][["region", "country"]].drop_duplicates()
regions["name"] = regions.region.apply(lambda x: x.split("_")[1])
regions = regions.rename(columns={"region": "geo_id", "country": "parent_id"})
regions.geo_id = regions.geo_id.str.upper()
regions["level"] = "region"

# Set MSA parent to region field and combine DataFrames
msas = msas.rename(columns={"region": "parent_id"})
msas = pd.concat([countries, regions, msas]).drop(columns=["geo_type", "country"])

# Cast polygon to string for writing purposes
msas.polygon = msas.polygon.astype(str)

# Reorder columns for writing output
msas[
    ["geo_id", "name", "level", "parent_id", "metro", "center_x", "center_y", "polygon"]
].to_csv("./out/cities_msa.csv", index=False)

