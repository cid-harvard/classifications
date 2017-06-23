import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":
    names = pd.read_table("./in/SITC_Rev2_Names.tsv", encoding="utf-8",
                          dtype={"code": str})

    hierarchy = pd.read_table("./in/SITC_Rev2_Hierarchy.tsv", encoding="utf-8", dtype="str")
    hierarchy.columns = ["level4_code", "level3_code", "level2_code", "level1_code", "level0_code"]

    # Drop the 5-digit level.
    names = names[names.level != "level4"]
    hierarchy = hierarchy.iloc[:, 1:].drop_duplicates()

    fields = {
        "level0": [],
        "level1": [],
        "level2": [],
        "level3": [],
    }

    h = Hierarchy(["level0", "level1", "level2", "level3"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h, fields)
    parent_code_table.code = parent_code_table.code.astype(str)

    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table["name"] = parent_id_table.name_en

    parent_id_table = parent_id_table[["code", "name", "level", "name_en",
                                       "name_es", "name_short_en", "name_short_es", "parent_id"]]

    c = Classification(parent_id_table, h)

    c.to_csv("out/sitc_rev2.csv")
    c.to_stata("out/sitc_rev2.dta")
