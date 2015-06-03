import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_table("in/DIVIPOLA_20150331.txt", encoding="utf-16")
    df.columns = ["department_code", "municipality_code",
                  "population_center_code", "department_name",
                  "municipality_name", "population_center_name",
                  "population_center_type", "longitude", "", "latitude",
                  "district", "municipality_type", "metro_area"]

    df = df[["department_code", "department_name", "municipality_code",
             "municipality_name", "population_center_code",
             "population_center_name"]]


    df.department_code = df.department_code.astype(str).str.zfill(2)
    df.municipality_code = df.municipality_code.astype(str).str.zfill(5)
    df.population_center_code = df.population_center_code.astype(str).str.zfill(8)

    df.department_name = df.department_name.str.title()
    df.municipality_name = df.municipality_name.str.title()
    df.population_center_name = df.population_center_name.str.title()

    h = Hierarchy(["department", "municipality", "population_center"])

    parent_code_table = repeated_table_to_parent_id_table(df, h)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_colombia_dane.csv")
