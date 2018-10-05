#!/usr/bin/python
# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    Classification,
)

if __name__ == "__main__":

    hierarchy = pd.read_table("in/Mexico_industry_master - Hierarchy.tsv")

    fields = {"section": [], "division": [], "group": [], "class": []}

    h = Hierarchy(["section", "division", "group", "class"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h, fields)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    names = pd.read_table("in/Mexico_industry_master - Names.tsv", encoding="utf-8")
    parent_id_table = parent_id_table.merge(names, on=["code", "level"], how="outer")

    parent_id_table["name"] = parent_id_table["name_en"]
    parent_id_table.code = parent_id_table.code.astype(str)

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_mexico_scian_2007_datlas.csv")
    c.to_stata("out/industries_mexico_scian_2007_datlas.dta")
