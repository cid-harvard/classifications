import pandas as pd

from classification import (
    Hierarchy,
    repeated_table_to_parent_id_table,
    parent_code_table_to_parent_id_table,
    Classification,
)

if __name__ == "__main__":

    trans = pd.read_csv("./in/HS4_Spanish_English_Translations.csv", encoding="utf-8")
    trans = trans[
        ["code", "level", "name_es", "name_en", "name_short_es", "name_short_en"]
    ]

    def fill_code(x):
        if x.level == "4digit":
            x.code = str(x.code).zfill(4)
        if x.level == "2digit":
            x.code = str(x.code).zfill(2)
        if x.level == "section":
            x.code = str(x.code)
        if x.level == "prospedia_section":
            x.code = str(x.code).zfill(1)
        return x

    trans = trans.apply(fill_code, axis=1)

    # Prospedia specific
    trans = trans[trans.level != "section"]
    df = pd.read_table("./in/prospedia_hs_structure.txt")
    df.columns = ["4digit_code", "2digit_code", "prospedia_section_code"]
    df["4digit_code"] = df["4digit_code"].astype(str).str.zfill(4)
    df["4digit_name"] = None
    df["2digit_code"] = df["2digit_code"].astype(str).str.zfill(2)
    df["2digit_name"] = None
    df["prospedia_section_name"] = None
    df["prospedia_section_code"] = df["prospedia_section_code"].astype(str).str.zfill(1)

    h = Hierarchy(["prospedia_section", "2digit", "4digit"])

    parent_code_table = repeated_table_to_parent_id_table(df, h)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    parent_id_table = parent_id_table.merge(trans, on=["level", "code"])
    parent_id_table.name = parent_id_table.name_en

    assert parent_id_table.name.isnull().sum() == 3
    parent_id_table.loc[parent_id_table.name.isnull(), "name"] = u"No name"
    assert parent_id_table.name.isnull().sum() == 0

    c = Classification(parent_id_table, h)

    c.to_csv("out/products_mexico_prospedia.csv")
    c.to_stata("out/products_mexico_prospedia.dta")
