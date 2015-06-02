import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_table("in/DIVIPOLA_20150331.txt", encoding="utf-16")
    df.columns = ["department_code", "municipality_code",
                  "populated_area_code", "department_name",
                  "municipality_name", "populated_area_name",
                  "populated_area_type", "longitude", "", "latitude",
                  "district", "municipality_type", "metro_area"]

    df = df[["department_code", "department_name", "municipality_code",
             "municipality_name", "populated_area_code",
             "populated_area_name"]]


    df.department_code = df.department_code.astype(str).str.zfill(2)
    df.municipality_code = df.municipality_code.astype(str).str.zfill(5)
    df.populated_area_code = df.populated_area_code.astype(str).str.zfill(8)

    df.department_name = df.department_name.str.title()
    df.municipality_name = df.municipality_name.str.title()
    df.populated_area_name = df.populated_area_name.str.title()

    h = Hierarchy(["department", "municipality", "populated_area"])

    parent_code_table = repeated_table_to_parent_id_table(df, h)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_colombia_dane.csv")
