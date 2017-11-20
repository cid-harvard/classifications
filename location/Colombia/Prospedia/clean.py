# vim: set fileencoding=utf-8 :

import pandas as pd

from classification import (Classification, Hierarchy,
                            parent_code_table_to_parent_id_table)


def id_table_to_code_table(df):
    df["parent_code"] = df.parent_id.map(df.code)
    return df.drop("parent_id", axis=1)


if __name__ == "__main__":

    c = Classification.from_csv("../DANE/out/locations_colombia_dane.csv", encoding="utf-8")

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

    wrongtext = u"Bogotá, D. C."
    assert parent_id_table.loc[3, "name"] == wrongtext
    assert parent_id_table.loc[3, "name_es"] == wrongtext
    assert parent_id_table.loc[3, "name_short_en"] == wrongtext
    assert parent_id_table.loc[3, "name_short_es"] == wrongtext

    righttext = u"Bogotá, D.C."
    parent_id_table.loc[3, "name"] = righttext
    parent_id_table.loc[3, "name_es"] = righttext
    parent_id_table.loc[3, "name_short_en"] = righttext
    parent_id_table.loc[3, "name_short_es"] = righttext

    msa_desc = pd.read_excel("./in/Munis_in_Mets.xlsx")
    msa_desc.columns = ["name", "code", "description_en", "description_es"]
    del msa_desc["name"]
    msa_desc["level"] = "msa"
    msa_desc["code"] = msa_desc["code"].astype(str).str.zfill(6)

    parent_id_table = parent_id_table.merge(msa_desc, on=["level", "code"], how="outer")

    # For names that are the same for different municipalities
    duplicated_names = parent_id_table.name.duplicated(keep=False)
    to_change = duplicated_names & (parent_id_table.level == "municipality")

    to_change_parents = parent_id_table.loc[to_change, "parent_id"].to_frame()
    parent_names = to_change_parents.join(parent_id_table["name"], on="parent_id")

    parent_id_table.loc[to_change, "name"] = parent_id_table.loc[to_change, "name"] + " (" + parent_names.name + ")"
    parent_id_table["name_es"] = parent_id_table["name"]
    parent_id_table["name_short_en"] = parent_id_table["name"]
    parent_id_table["name_short_es"] = parent_id_table["name"]

    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_colombia_prosperia.csv")
    c.to_stata("out/locations_colombia_prosperia.dta")
