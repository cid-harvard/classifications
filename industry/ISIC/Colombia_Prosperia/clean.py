import pandas as pd

from classification import (Hierarchy,
                            parent_code_table_to_parent_id_table,
                            repeated_table_to_parent_id_table,
                            Classification)
if __name__ == "__main__":

    df = pd.read_table("./in/col_industry_name_category_master - Sheet1.tsv", encoding="utf-8")
    df.columns = ["class_code", "division_code", "section_code",
                  "name_es_class", "", "name_short_es_class", "name_en_class",
                  "name_short_en_class", "name_es_division", "",
                  "name_short_es_division", "name_en_division",
                  "name_short_en_division", "name_en_section",
                  "name_es_section"]

    df = df.drop_duplicates(["class_code", "division_code", "section_code"]).reset_index(drop=True)

    df.class_code = df.class_code.astype(int).astype(str).str.zfill(4)
    df.division_code = df.division_code.astype(int).astype(str).str.zfill(2)
    df.section_code = df.section_code.astype(int).astype(str).str.zfill(2)

    h = Hierarchy(["section", "division", "class"])
    parent_code_table = repeated_table_to_parent_id_table(
        df, h,
        level_fields={
            "section": ["name_en_section", "name_es_section"],
            "division": ["name_es_division", "name_short_es_division",
                         "name_en_division", "name_short_en_division"],
            "class": ["name_es_class", "name_short_es_class",
                      "name_en_class", "name_short_en_class"],
        })

    parent_code_table = parent_code_table\
        .sort(["level", "code"])\
        .drop_duplicates(["level", "code"])\
        .reset_index(drop=True)

    parent_code_table.name_short_es.fillna(parent_code_table.name_es, inplace=True)
    parent_code_table.name_short_en.fillna(parent_code_table.name_en, inplace=True)
    parent_code_table = parent_code_table.reset_index(drop=True)

    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    parent_id_table.code = parent_id_table.code.astype(str)
    parent_id_table["name"] = parent_id_table.name_en

    c = Classification(parent_id_table, h)

    c.to_csv("out/industries_colombia_isic_prosperia.csv")
    c.to_stata("out/industries_colombia_isic_prosperia.dta")
