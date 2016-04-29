import pandas as pd

from classification import (Hierarchy, Classification)

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

    def get_id_by_code(df, code):
        rows = df[df.code == code].index.tolist()
        assert len(rows) == 1
        return float(rows[0])

    # Create the "Other" provinces that are XX9900 for unknown province data
    # points
    def create_others(row):
        row.parent_id = get_id_by_code(df, row.code)
        row.code = row.code[:2] + "9900"
        row.level = "msa"
        row.name_en = row.name_en + " (unknown province)"
        row.name_short_en = row.name_short_en + " (unknown province)"
        row.name_es = row.name_es + " (provincia desconocida)"
        row.name_short_es = row.name_short_es + " (provincia desconocida)"
        row["name"] = row.name_en
        return row

    others = df[df.level == "department"].apply(create_others, axis=1)

    # Add Callao province that moved from Callo dept that no longer exists
    callao = pd.Series({
        "code": "159800",
        "level": "msa",
        "name_es": u"Callao",
        "name_short_es": u"Callao",
        "name_en": u"Callao",
        "name_short_en": u"Callao",
        "name": u"Callao",
        "parent_id": get_id_by_code(df, "150000")  # Callao's parent is Lima
    })

    df = pd.concat([df,
                    others,
                    pd.DataFrame(callao).T,
                    ]).reset_index(drop=True)

    df.parent_id = df.parent_id.astype(float)

    h = Hierarchy(["country", "department", "msa", "municipality"])
    df.level = df.level.astype("category", categories=h, ordered=True)
    df.level = df.level.astype(str)

    # Drop old Callao department and province
    # Do this after reset_index to not mess up the id order
    df = df[df.code != "070000"]
    df = df[df.code != "070100"]

    # Order the columns
    df = df[["code","name","level","name_es","name_en","name_short_es","name_short_en","parent_id"]]

    c = Classification(df, h)

    c.to_csv("out/locations_peru_datlas.csv")
    c.to_stata("out/locations_peru_datlas.dta")
