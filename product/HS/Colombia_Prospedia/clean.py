import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":
    names = pd.read_table("./in/HS_hierarchy_master - Names.tsv", encoding="utf-8", dtype={"code": str})

    hierarchy = pd.read_table("./in/HS_hierarchy_master - Hierarchy.tsv",
                              encoding="utf-8",
                              dtype={
                                  "4digit": str,
                                  "2digit": str,
                                  "prosperia_section": str,
                                  "section": str,
                              })
    hierarchy.columns = ["4digit_code", "2digit_code", "prosperia_section_code", "atlas_section"]
    hierarchy["4digit_name"] = None
    hierarchy["2digit_name"] = None
    hierarchy["prosperia_section_name"] = None


    h = Hierarchy(["prosperia_section", "2digit", "4digit"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h)

    parent_code_table = parent_code_table.merge(names, on=["code", "level"])

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table.name = parent_id_table.name_en

    from IPython import embed; embed()

    c = Classification(parent_id_table, h)

    c.to_csv("out/products_mexico_prospedia.csv")
    c.to_stata("out/products_mexico_prospedia.dta")
