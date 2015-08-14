import pandas as pd

from classification import (Classification, Hierarchy,
                            parent_code_table_to_parent_id_table)


def id_table_to_code_table(df):
    df["parent_code"] = df.parent_id.map(df.code)
    return df.drop("parent_id", axis=1)


if __name__ == "__main__":

    c = Classification.from_csv("../DANE/out/locations_colombia_dane.csv")

    df = id_table_to_code_table(c.table)
    df = df[df.level != "population_center"]

    colombia = pd.Series({
        "code": "COL",
        "name": "Colombia",
        "level": "country"
    })

    metro_areas = pd\
        .read_stata("./in/Colombia_city_key.dta", encoding="mac-roman")\
        .query("head_mun == 1")[["city_name", "city_code"]]

    metro_areas.columns = ["name", "code"]

    metro_areas["parent_code"] = metro_areas.code.str.slice(0, 2)
    metro_areas["level"] = "msa"

    df.loc[df.level=="department", "parent_code"] = "COL"

    df = pd.concat([pd.DataFrame(colombia).T, df, metro_areas])

    df = df.sort(["level", "code"], ascending=True)
    df = df.reset_index(drop=True)

    h = Hierarchy(["country", "department", "msa", "municipality"])
    parent_id_table = parent_code_table_to_parent_id_table(df, h)
    parent_id_table["name_es"] = parent_id_table.name
    parent_id_table["name_short_en"] = parent_id_table.name
    parent_id_table["name_short_es"] = parent_id_table.name

    # Work around issue where parent_code_table_to_parent_id_table breaks
    # because the parent of munis are not msas
    depts = df[df.level == "department"]
    depts = depts[["code"]].reset_index().set_index("code")
    lookup_table = depts.to_dict()["index"]

    def fill_parents(row):
        if row.level == "municipality" and pd.isnull(row.parent_id):
            row.parent_id = lookup_table[row.code[:2]]
        return row
    parent_id_table = parent_id_table.apply(fill_parents, axis=1)

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_colombia_prosperia.csv")
    c.to_stata("out/locations_colombia_prosperia.dta")
