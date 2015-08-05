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
        .read_stata("/Users/makmana/ciddata/Subnationals/Atlas/Colombia/beta/Trade/Keys/Colombia_city_key.dta", encoding="mac-roman")\
        .query("head_mun == 1")[["city_name", "city_code"]]

    metro_areas.columns = ["name", "code"]

    metro_areas["parent_code"] = metro_areas.code.str.slice(0, 2)
    metro_areas["level"] = "msa"

    df = pd.concat([pd.DataFrame(colombia).T, df, metro_areas])

    df = df.reset_index(drop=True)
    df = df.sort(["level", "code"], ascending=True)

    h = Hierarchy(["country", "department", "msa", "municipality"])
    df = parent_code_table_to_parent_id_table(df, h)

    c = Classification(df, h)

    c.to_csv("out/locations_colombia_prosperia.csv")
    c.to_stata("out/locations_colombia_prosperia.dta")
