#!/usr/bin/python
# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (Hierarchy, ordered_table_to_parent_code_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

import re
import sys

if __name__ == "__main__":

    assert len(sys.argv) == 2
    filename = sys.argv[1]

    df = pd.read_excel("./in/est_ingles_2007.xlsx", sheetname=0)
    df.columns = ["code", "name_spanish", "code2", "name_english"]

    assert df.code.equals(df.code2)
    df = df[["code", "name_spanish", "name_english"]]

    df.code = df.code.astype(str)

    regexes = {"mex": u"MÉX\.", "can": u"CAN\.", "usa": u"EE\.UU\."}

    # Remove weird "Mex" "Can" identifiers within the name fields
    for name, regex in regexes.items():
        selected_rows = df.name_english.str.contains(regex)
        df["tag_en_" + name] = False
        df.loc[selected_rows, "tag_en_" + name] = True
        df.name_english = df.name_english.map(lambda x: re.sub(regex, "", x))

    for name, regex in regexes.items():
        selected_rows = df.name_spanish.str.contains(regex)
        df["tag_sp_" + name] = False
        df.loc[selected_rows, "tag_sp_" + name] = True
        df.name_spanish = df.name_spanish.map(lambda x: re.sub(regex, "", x))

    # Replace trailing comma and space
    df.name_spanish = df.name_spanish.str.replace(", $", "")
    df.name_english = df.name_english.str.replace(", $", "")

    df.loc[df.code.str.len() == 2, "level"] = "twodigit"
    df.loc[df.code.str.len() == 3, "level"] = "threedigit"
    df.loc[df.code.str.len() == 4, "level"] = "fourdigit"
    df.loc[df.code.str.len() == 5, "level"] = "fivedigit"
    df.loc[df.code.str.len() == 6, "level"] = "sixdigit"

    spanish = df[["code", "level", "name_spanish"]]
    spanish.columns = ["code", "level", "name_es"]

    # make sure this is the hand-fixed version
    assert df.loc[304, "code"] == '31'

    df = df[["code", "name_english", "level"]]
    df.columns = ["code", "name", "level"]

    h = Hierarchy(["twodigit", "threedigit", "fourdigit", "fivedigit", "sixdigit"])
    parent_code_table = ordered_table_to_parent_code_table(df, h)

    # TODO: changing these levels, but it'd be better if this was done in a
    # separate classification named datlas_mexico or something similar, in
    # order to not mess up the original.
    parent_code_table = parent_code_table[~parent_code_table.level.isin(["fivedigit", "sixdigit"])]
    parent_code_table = parent_code_table.reset_index(drop=True)

    def rename_level(df, from_level, to_level):
        df.loc[df.level == from_level, "level"] = to_level

    rename_level(parent_code_table, "twodigit", "section")
    rename_level(parent_code_table, "threedigit", "division")
    rename_level(parent_code_table, "fourdigit", "class")

    rename_level(spanish, "twodigit", "section")
    rename_level(spanish, "threedigit", "division")
    rename_level(spanish, "fourdigit", "class")

    h = Hierarchy(["section", "division", "class"])
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table = parent_id_table.merge(spanish, on=["level", "code"])

    parent_id_table["name_short_en"] = parent_id_table["name"]
    parent_id_table["name_short_es"] = parent_id_table["name_es"]

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_mexico_scian_2007.csv")
    c.to_stata("out/industries_mexico_scian_2007.dta")
