import pandas as pd

from fix_spanish_title_case import fix_spanish_title_case
from classification import (Hierarchy, parent_code_table_to_parent_id_table,
                            Classification)


if __name__ == "__main__":

    df = pd.read_csv("in/ubigeo-data-titlecased.csv",
                     encoding="utf-8",
                     dtype={
                         "inei": str
                     })
    df.columns = ["reniec_code", "code", "name", "complete_name"]

    df = df[["code", "name"]]
    df = df[~df.code.isnull()]

    # This adds a highest level element that represents the whole country
    peru = pd.Series({
        "code": "000000",
        "name": "Peru",
    })
    df = pd.concat([pd.DataFrame(peru).T, df])

    def fix_levels(row):
        if row.code == "000000":
            row["level"] = "country"
            row["parent_code"] = pd.np.nan
        elif row.code.endswith("0000"):
            row["level"] = "department"
            row["parent_code"] = "000000"
        elif row.code.endswith("00"):
            row["level"] = "province"
            row["parent_code"] = row["code"][:2] + "0000"
        else:
            row["level"] = "district"
            row["parent_code"] = row["code"][:4] + "00"
        return row

    df = df.apply(fix_levels, axis=1)

    df.name = df.name.map(fix_spanish_title_case, na_action="ignore")

    h = Hierarchy(["country", "department", "province", "district"])
    df.level = df.level.astype("category", categories=h, ordered=True)

    df = df.sort_values(by=["level", "code"])

    df.level = df.level.astype(str)
    df = df.reset_index(drop=True)
    parent_id_table = parent_code_table_to_parent_id_table(df, h)

    # TODO: This isn't the official classification level name but this makes
    # compatibility between colombia and mexico way easier
    #parent_code_table.loc[parent_code_table.level == "state", "level"] = "department"

    # Drop the "locality" level since we don't use it
    #parent_code_table = parent_code_table[parent_code_table.level != "locality"]

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_peru_inei.csv")
    c.to_stata("out/locations_peru_inei.dta")
