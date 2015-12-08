import pandas as pd

from classification import (Hierarchy,
                            parent_code_table_to_parent_id_table,
                            repeated_table_to_parent_id_table,
                            Classification)
if __name__ == "__main__":

    df = pd.read_table("./in/col_industry_name_category_master - Hierarchy.tsv", encoding="utf-8")

    df.class_code = df.class_code.astype(int).astype(str).str.zfill(4)
    df.division_code = df.division_code.astype(int).astype(str).str.zfill(2)
    df.section_code = df.section_code.astype(int).astype(str).str.zfill(1)

    names = pd.read_table("./in/col_industry_name_category_master - Names.tsv", encoding="utf-8")
    names.loc[names.level == "section", "code"] = names.code.astype(str)
    names.loc[names.level == "division", "code"] = names.code.astype(str).str.zfill(2)
    names.loc[names.level == "class", "code"] = names.code.astype(str).str.zfill(4)

    h = Hierarchy(["section", "division", "class"])
    parent_code_table = repeated_table_to_parent_id_table(
        df, h,
        level_fields={
            "section": [],
            "division": [],
            "class": [],

        }).sort_values(by=["level", "code"])\
        .reset_index(drop=True)

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)
    parent_id_table = parent_id_table.merge(names)

    parent_id_table["name"] = parent_id_table.name_en

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_colombia_isic_prosperia.csv")
    c.to_stata("out/industries_colombia_isic_prosperia.dta")
