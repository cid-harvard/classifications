import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)


if __name__ == "__main__":

    df = pd.read_csv("in/cat_localidad_MAY2015.csv.gz", encoding="ISO-8859-2",
                     compression="gzip")
    df.columns = ["state_code", "state_name", "state_name_short",
                  "municipality_code", "municipality_name",
                  "locality_code", "locality_name",
                  "latitude", "longitude", "altitude",
                  "map_code", "ambito",
                  "population_total", "population_male", "population_female",
                  "dwellings_occupied"]

    df = df[["state_code", "state_name", "municipality_code",
             "municipality_name", "locality_code",
             "locality_name"]]


    df.state_code = df.state_code.astype(str).str.zfill(2)
    df.municipality_code = df.municipality_code.astype(str).str.zfill(3)
    df.locality_code = df.locality_code.astype(str).str.zfill(4)

    df.municipality_code = df.state_code + df.municipality_code
    df.locality_code = df.municipality_code + df.locality_code

    df.state_name = df.state_name.str.title()
    df.municipality_name = df.municipality_name.str.title()
    df.locality_name = df.locality_name.str.title()

    h = Hierarchy(["state", "municipality", "locality"])

    parent_code_table = repeated_table_to_parent_id_table(df, h)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_mexico_inegi.csv")
    c.to_stata("out/locations_mexico_inegi.dta")
