import pandas as pd

from fix_spanish_title_case import fix_spanish_title_case
from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    Classification,
)

if __name__ == "__main__":

    df = pd.read_table("in/DIVIPOLA_20150331.txt", encoding="utf-16")
    df.columns = [
        "department_code",
        "municipality_code",
        "population_center_code",
        "department_name",
        "municipality_name",
        "population_center_name",
        "population_center_type",
        "longitude",
        "",
        "latitude",
        "district",
        "municipality_type",
        "metro_area",
    ]

    df = df[
        [
            "department_code",
            "department_name",
            "municipality_code",
            "municipality_name",
            "population_center_code",
            "population_center_name",
        ]
    ]

    df.department_code = df.department_code.astype(str).str.zfill(2)
    df.municipality_code = df.municipality_code.astype(str).str.zfill(5)
    df.population_center_code = df.population_center_code.astype(str).str.zfill(8)

    df.department_name = df.department_name.str.title()
    df.municipality_name = df.municipality_name.str.title()
    df.population_center_name = df.population_center_name.str.title()

    df.department_name = df.department_name.map(
        fix_spanish_title_case, na_action="ignore"
    )
    df.municipality_name = df.municipality_name.map(
        fix_spanish_title_case, na_action="ignore"
    )
    df.population_center_name = df.population_center_name.map(
        fix_spanish_title_case, na_action="ignore"
    )

    h = Hierarchy(["department", "municipality", "population_center"])

    df = df.rename(
        columns={
            "department_name": "name_department",
            "municipality_name": "name_municipality",
            "population_center_name": "name_population_center",
        }
    )

    parent_code_table = repeated_table_to_parent_id_table(
        df,
        h,
        level_fields={
            "department": ["name_department"],
            "municipality": ["name_municipality"],
            "population_center": ["name_population_center"],
        },
    )
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    # Reorder columns to keep diff clean
    parent_id_table = parent_id_table.ix[:, ["code", "name", "level", "parent_id"]]

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_colombia_dane.csv")
    c.to_stata("out/locations_colombia_dane.dta")
