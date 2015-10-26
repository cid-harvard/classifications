#!/usr/bin/python
# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    hierarchy = pd.read_table("in/Mexico_industry_master - Hierarchy.tsv")

    fields = {
        "section": [],
        "division": [],
        "group": [],
        "class": [],
    }

    h = Hierarchy(["section", "division", "group", "class"])
    parent_code_table = repeated_table_to_parent_id_table(hierarchy, h, fields)

    # Workaround for Timageddon issue - Tim made some codes like 31 / 32 / 33
    # fall under different sections sometimes, and this breaks the strict
    # treelike hierarchy of the classification. This happens mainly at the
    # division level. We've decided to cut our losses right now and pick one.
    # This comes at the expense of possibly mis-assigning some class level
    # codes to different codes but until someone either fixes the
    # classification or the classification system entirely, there's not much we
    # can do here.

    parent_code_table = parent_code_table[~parent_code_table.duplicated(["code", "level"])]
    parent_code_table = parent_code_table.reset_index(drop=True)

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    names = pd.read_table("in/Mexico_industry_master - Names.tsv", encoding="utf-8")
    parent_id_table = parent_id_table.merge(names, on=["code", "level"], how="outer")

    # We also decided to rename the one category these things fall into to be
    # "Other manufacturing industries", since that seems to fit well and is
    # less confusing.

    metals_section = (parent_id_table.level == "section") & (parent_id_table.code == 5)
    parent_id_table.loc[metals_section, ("name_en", "name_short_en")] = u"Manufacturing Industries"
    parent_id_table.loc[metals_section, ("name_es", "name_short_es")] = u"Industrias Manufactureras"

    parent_id_table["name"] = parent_id_table["name_en"]
    parent_id_table.code = parent_id_table.code.astype(str)

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_mexico_scian_2007_datlas.csv")
    c.to_stata("out/industries_mexico_scian_2007_datlas.dta")
