import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            spread_out_entries, sort_by_code_and_level,
                            Classification)

if __name__ == "__main__":
    names = pd.read_table("./in/HS92_Atlas_Names.tsv", encoding="utf-8",
                          dtype={"code": str})

    hierarchy = pd.read_table("./in/HS92_Atlas_Hierarchy.tsv", encoding="utf-8", dtype="str")

    fields = {
        "section": [],
        "2digit": [],
        "4digit": [],
    }

    h = Hierarchy(["section", "2digit", "4digit"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h, fields)
    parent_code_table.code = parent_code_table.code.astype(str)
    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    # Sort by level order (not necessarily alphabetical)
    parent_code_table = sort_by_code_and_level(parent_code_table, h)

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table["name"] = parent_id_table.name_en

    parent_id_table = parent_id_table[["code", "name", "level", "name_en",
                                       "name_es", "name_short_en", "name_short_es", "parent_id"]]

    # Decide what id each level should start from
    # Put ample space between each range of ids
    level_starts = {
        "section": 0,
        "2digit": 100,
        "4digit": 650
    }
    parent_id_table = spread_out_entries(parent_id_table, level_starts, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/hs92_atlas.csv")
    c.to_stata("out/hs92_atlas.dta")
