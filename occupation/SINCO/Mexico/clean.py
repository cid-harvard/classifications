# vim: set fileencoding=utf8 :

import pandas as pd

from classification import (Hierarchy, ordered_table_to_parent_code_table,
                            parent_code_table_to_parent_id_table,
                            Classification)

if __name__ == "__main__":

    sinco = pd.read_csv("in/SINCO_2011.csv", header=None, encoding="latin-1")

    sinco.columns = ["data"]
    sinco = sinco[~sinco.data.str.startswith("INEGI.")]
    sinco = sinco[~sinco.data.str.startswith(u"Clave Descripción")]

    for index, row in reversed(list(sinco[~sinco.data.str.match("^\d* ")].iterrows())):
        sinco.ix[index - 1] += (" " + sinco.ix[index])

    sinco = sinco[sinco.data.str.match("^\d* ")]

    sinco = sinco.data.str.split(" ", 1).apply(pd.Series, 1)
    sinco.columns = ["code", "name"]

    sinco["level"] = sinco["code"].apply(lambda x: str(len(x)) + "digit")
    h = Hierarchy(["1digit", "2digit", "3digit", "4digit"])

    parent_code_table = ordered_table_to_parent_code_table(sinco, h)
    parent_code_table = parent_code_table.reset_index(drop=True)
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    c = Classification(parent_id_table, h)

    c.to_csv("out/occupations_sinco_2011.csv")
    c.to_stata("out/occupations_sinco_2011.dta")
