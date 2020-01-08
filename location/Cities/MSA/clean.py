import pandas as pd
import geopandas as gp

shape_file = "./in/nafta_metro.dbf"

remap_columns = {
    "GEOID": "geo_id",
    "GID_0": "country",
    "NAME": "name",
    "MTYPE": "geo_type",
    "geometry": "polygon",
}

metro_types = {
    "CAN": {"B": True, "D": False, "K": False},
    "USA": {"M1": True, "M2": False},
    "MEX": {"M1": True},
}

sh = gp.read_file(shape_file).rename(columns=remap_columns).sort_values("country")
sh["metro"] = sh.apply(lambda x: metro_types[x.country][x.geo_type], axis=1)

sh.polygon = sh.polygon.astype(str)
sh.to_csv("./out/cities_msa.csv")
