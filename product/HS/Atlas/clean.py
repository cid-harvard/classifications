import pandas as pd
import numpy as np


from classification import (Hierarchy, parent_code_table_to_parent_id_table, Classification)

if __name__ == "__main__":

    hs4 = pd.read_table("in/hs4.tsv", encoding="utf-8")

    hs4 = hs4[["Code", "hs4_name", "community"]]
    hs4.columns = ["code", "name", "community"]

    four_digit = hs4.iloc[:1241]
    four_digit["code"] = four_digit.code.astype(str).str.zfill(4)
    four_digit["parent_code"] = four_digit.code.apply(lambda x: x[:2])
    four_digit = four_digit.drop("community", axis=1)
    four_digit["level"] = "4digit"

    two_digit = hs4.iloc[1241:1339]
    two_digit["code"] = two_digit.code.astype(str).str.zfill(2)
    two_digit = two_digit.rename(columns={"community": "parent_code"})
    two_digit["parent_code"] = two_digit.parent_code.astype(str).str.zfill(3)
    two_digit["level"] = "2digit"

    section = hs4.iloc[1339:].drop("community", axis=1)
    section["code"] = section.code.astype(str).str.zfill(3)
    section["parent_code"] = None
    section["level"] = "section"

    hs_clean = pd.concat([section, two_digit, four_digit])
    hs_clean = hs_clean.reset_index(drop=True)

    h = Hierarchy(["section", "2digit", "4digit"])
    hs_clean = parent_code_table_to_parent_id_table(hs_clean, h)
    c = Classification(hs_clean, h)

    #community = pd.read_table("in/hs4_community.tsv", encoding="utf-8")
    #hs4 = hs4.merge(community, left_on="community", right_on="code", how="inner")

    # weird bug where pandas infer_type was returning mixed instead of string
    c.table.code = c.table.code.astype(str)

    c.to_csv("out/hs92_atlas.csv")
