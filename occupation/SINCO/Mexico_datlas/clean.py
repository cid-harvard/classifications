# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (Hierarchy, ordered_table_to_parent_code_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    sinco = pd.read_table("in/Mexico Occupations (SINCO 2011) - Classification with translations.tsv",
                          encoding="utf-8",
                          dtype={"code": unicode})
    sinco = sinco.set_index("id")
    sinco = sinco[["name_es", "name_en", "name_short_es", "name_short_en", "code", "level", "parent_id"]]

    sinco["name"] = sinco["name_en"]

    sinco.loc[sinco.name_short_en.isnull(), "name_short_en"] = sinco["name_en"]
    sinco.loc[sinco.name_short_es.isnull(), "name_short_es"] = sinco["name_es"]

    h = Hierarchy(["1digit", "2digit", "3digit", "4digit"])
    c = Classification(sinco, h)

    c.to_csv("out/occupations_sinco_datlas_2011.csv")
    c.to_stata("out/occupations_sinco_datlas_2011.dta")
