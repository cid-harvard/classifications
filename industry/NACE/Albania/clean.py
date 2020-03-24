import pandas as pd

from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    spread_out_entries,
    sort_by_code_and_level,
    Classification,
)


if __name__ == "__main__":
    df = pd.read_csv("./in/NACE_Rev2_custom_hierarchy.csv")
    df.columns = ["level", "code", "parent_code", "name"]

    df.level = df.level.astype(str)

    df.loc[df.level == "1", "level"] = "section"
    df.loc[df.level == "2", "level"] = "division"
    df.loc[df.level == "3", "level"] = "group"

    h = Hierarchy(["section", "division", "group"])

    df = sort_by_code_and_level(df, h)
    df = parent_code_table_to_parent_id_table(df, h)

    level_starts = {"section": 0, "division": 100, "group": 300}
    df = spread_out_entries(df, level_starts, h)

    c = Classification(df, h)
    c.to_csv("./out/nace_industries.csv")
