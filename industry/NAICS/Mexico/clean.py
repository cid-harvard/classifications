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

    h = Hierarchy(["twodigit", "threedigit", "fourdigit", "fivedigit", "sixdigit"])

    df.loc[df.code.str.len() == 2, "level"] = "twodigit"
    df.loc[df.code.str.len() == 3, "level"] = "threedigit"
    df.loc[df.code.str.len() == 4, "level"] = "fourdigit"
    df.loc[df.code.str.len() == 5, "level"] = "fivedigit"
    df.loc[df.code.str.len() == 6, "level"] = "sixdigit"

    df = df[["code", "name_spanish", "level"]]
    df.columns = ["code", "name", "level"]

    parent_code_table = ordered_table_to_parent_code_table(df, h)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_mexico_scian_2007.csv")