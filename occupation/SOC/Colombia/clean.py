# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    df = pd.read_table("in/Col_occupations_SOC_2010 - Hierarchy.tsv", encoding="utf-8")

    h = Hierarchy(["major_group", "minor_group", "broad_occupation", "detailed_occupation"])
    fields = {
        "major_group": ["name_en_major_group", "name_es_major_group"],
        "minor_group": ["name_en_minor_group", "name_es_minor_group", "name_short_es_minor_group"],
        "broad_occupation": ["name_en_broad_occupation", "name_es_broad_occupation"],
        "detailed_occupation": ["name_en_detailed_occupation", "name_es_detailed_occupation", "name_short_es_detailed_occupation"],
    }

    # TODO: no short names for these
    df["name_short_es_broad_occupation"] = ""
    df["name_short_es_major_group"] = ""

    from IPython import embed; embed()
    df = repeated_table_to_parent_id_table(df, h, fields)

    df["name_short_en"] = df["name_en"]
    df["name_short_es"] = df["name_short_es"].fillna(df.name_es)

    assert not df[df.level == "detailed_occupation"].code.str.endswith("0").all()
    assert df[df.level == "broad_occupation"].code.str.endswith("0").all()
    assert df[df.level == "major_group"].code.str.endswith("000").all()
    assert df[df.level == "minor_group"].code.str.endswith("00").all()

    df["name"] = df.name_en
    df = parent_code_table_to_parent_id_table(df, h)

    c = Classification(df, h)

    c.to_csv("out/occupations_soc_2010.csv")
    c.to_stata("out/occupations_soc_2010.dta")
