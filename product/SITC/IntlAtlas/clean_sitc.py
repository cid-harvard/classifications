import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            spread_out_entries, sort_by_code_and_level,
                            Classification)

if __name__ == "__main__":
    names = pd.read_table("./in/SITC_Rev2_Names.tsv", encoding="utf-8",
                          dtype={"code": str})

    hierarchy = pd.read_table("./in/SITC_Rev2_Hierarchy.tsv", encoding="utf-8", dtype="str")
    hierarchy.columns = ["5digit_code", "4digit_code", "3digit_code", "2digit_code", "section_code"]

    services = pd.read_table("./in/Services_Hierarchy.tsv", encoding="utf-8", dtype={"code": str})

    # Drop the 5-digit level.
    names = names[names.level != "5digit"]
    hierarchy = hierarchy.iloc[:, 1:].drop_duplicates()

    fields = {
        "section": [],
        "2digit": [],
        "3digit": [],
        "4digit": [],
    }

    h = Hierarchy(["section", "2digit", "3digit", "4digit"])
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
        "3digit": 250,
        "4digit": 650
    }
    parent_id_table = spread_out_entries(parent_id_table, level_starts, h)

    # Add services classes with additional padding
    service_starts = {
        "section": 10,
        "2digit": 200,
        "3digit": 600,
        "4digit": 2000
    }
    services = spread_out_entries(services, service_starts, h)

    # Append to main table and sort on combined spread out indices
    parent_id_table = parent_id_table.append(services).sort_index()

    c = Classification(parent_id_table, h)

    c.to_csv("out/sitc_rev2.csv")
    c.to_stata("out/sitc_rev2.dta")
