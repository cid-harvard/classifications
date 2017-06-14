import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":
    names = pd.read_table("./in/FarmType_Names.tsv", encoding="utf-8",
                          dtype={"code": str})

    hierarchy = pd.read_table("./in/FarmType_Hierarchy.tsv", encoding="utf-8")
    hierarchy.columns = ["level2_code", "level1_code", "level0_code"]

    fields = {
        "level0": [],
        "level1": [],
        "level2": []
    }

    h = Hierarchy(["level0", "level1", "level2"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h, fields)
    parent_code_table.code = parent_code_table.code.astype(str)

    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table["name"] = parent_id_table.name_en

    parent_id_table = parent_id_table[["code", "name", "level", "name_en",
                                       "name_es", "parent_id"]]

    c = Classification(parent_id_table, h)

    c.to_csv("out/farm_type.csv")
    c.to_stata("out/farm_type.dta")
