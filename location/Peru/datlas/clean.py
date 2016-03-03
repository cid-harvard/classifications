import pandas as pd

from classification import (Hierarchy, parent_code_table_to_parent_id_table,
                            Classification)


if __name__ == "__main__":

    df = pd.read_csv("../INEI/out/locations_peru_inei.csv",
                     encoding="utf-8",
                     index_col=0,
                     dtype={
                         "code": str
                     })

    # Rename the levels to what the frontend uses
    df.loc[df.level == "province", "level"] = "msa"

    # Drop the "district" / level since we don't use it
    df = df[df.level != "district"]

    h = Hierarchy(["country", "department", "msa", "municipality"])
    df.level = df.level.astype("category", categories=h, ordered=True)
    df.level = df.level.astype(str)

    c = Classification(df, h)

    c.to_csv("out/locations_peru_datlas.csv")
    c.to_stata("out/locations_peru_datlas.dta")
