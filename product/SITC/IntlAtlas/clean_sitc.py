import pandas as pd
import sys

sys.path.append("../../..")
from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    spread_out_entries,
    sort_by_code_and_level,
    Classification,
)

TOP_LEVEL = "section"

if __name__ == "__main__":
    names = pd.read_table(
        "./in/SITC_Rev2_Names.tsv", encoding="utf-8", dtype={"code": str}
    )

    hierarchy = pd.read_table(
        "./in/SITC_Rev2_Hierarchy.tsv", encoding="utf-8", dtype="str"
    )
    hierarchy.columns = [
        "5digit_code",
        "4digit_code",
        "3digit_code",
        "2digit_code",
        "section_code",
    ]

    services = pd.read_csv(
        "./in/Services_Hierarchy.csv", encoding="utf-8", dtype={"code": str}
    )
    services["top_parent_id"] = 0

    # Drop the 5-digit level.
    names = names[names.level != "5digit"]
    hierarchy = hierarchy.iloc[:, 1:].drop_duplicates()

    fields = {"section": [], "2digit": [], "3digit": [], "4digit": []}

    h = Hierarchy(["section", "2digit", "3digit", "4digit"])
    parent_code_table = repeated_table_to_parent_id_table(
        hierarchy, h, fields, top_level=TOP_LEVEL
    )
    parent_code_table.code = parent_code_table.code.astype(str)
    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    # Sort by level order (not necessarily alphabetical)
    parent_code_table = sort_by_code_and_level(parent_code_table, h)

    parent_id_table = parent_code_table_to_parent_id_table(
        parent_code_table, h, top_level=TOP_LEVEL
    )
    parent_id_table["name"] = parent_id_table.name_en

    parent_id_table = parent_id_table[
        [
            "code",
            "name",
            "level",
            "name_en",
            "name_es",
            "name_short_en",
            "name_short_es",
            "parent_id",
            "top_parent_id",
        ]
    ]

    # Decide what id each level should start from
    # Put ample space between each range of ids
    level_starts = {"section": 0, "2digit": 100, "3digit": 250, "4digit": 650}
    parent_id_table = spread_out_entries(
        parent_id_table, level_starts, h, top_level=TOP_LEVEL
    )

    # Add services classes with additional padding
    service_starts = {"section": 10, "2digit": 200, "3digit": 600, "4digit": 2000}
    services = spread_out_entries(services, service_starts, h)

    # Append to main table and sort on combined spread out indices
    parent_id_table = parent_id_table.append(services).sort_index()

    c = Classification(parent_id_table, h)
    c.to_csv("out/sitc_rev2_with3digit.csv")
    c.to_stata("out/sitc_rev2_with3digit.dta")

    # Now handle without 3 digit - do this on parent code table so we don't
    # have to rejigger all the parent ids again and can have
    # parent_code_table_to_parent_id_table deal with it.

    fields = {"section": [], "2digit": [], "4digit": []}
    h = Hierarchy(["section", "2digit", "4digit"])

    # Drop the 3-digit level.
    names = names[names.level != "3digit"]
    hierarchy = hierarchy.drop(columns="3digit_code").drop_duplicates()

    parent_code_table = repeated_table_to_parent_id_table(
        hierarchy, h, fields, top_level=TOP_LEVEL
    )
    parent_code_table.code = parent_code_table.code.astype(str)
    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    # Sort by level order (not necessarily alphabetical)
    parent_code_table = sort_by_code_and_level(parent_code_table, h)

    parent_id_table = parent_code_table_to_parent_id_table(
        parent_code_table, h, top_level=TOP_LEVEL
    )
    parent_id_table["name"] = parent_id_table.name_en

    parent_id_table = parent_id_table[
        [
            "code",
            "name",
            "level",
            "name_en",
            "name_es",
            "name_short_en",
            "name_short_es",
            "parent_id",
            "top_parent_id",
        ]
    ]

    # Decide what id each level should start from
    # Put ample space between each range of ids
    level_starts = {"section": 0, "2digit": 100, "4digit": 650}
    parent_id_table = spread_out_entries(
        parent_id_table, level_starts, h, top_level=TOP_LEVEL
    )

    # Add services classes with additional padding
    services = pd.read_csv(
        "./in/Services_Hierarchy.csv", encoding="utf-8", dtype={"code": str}
    )
    services["top_parent_id"] = 0
    services = services[services.level != "3digit"]
    services.loc[services.level == "4digit", "parent_id"] = [1, 2, 3, 4, 5]

    service_starts = {"section": 10, "2digit": 200, "4digit": 2000}
    services = spread_out_entries(services, service_starts, h, top_level=TOP_LEVEL)

    # Append to main table and sort on combined spread out indices
    parent_id_table = parent_id_table.append(services).sort_index()

    c = Classification(parent_id_table, h)
    c.to_csv("out/sitc_rev2.csv")
    c.to_stata("out/sitc_rev2.dta")
