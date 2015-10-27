import pandas as pd

from classification import (Hierarchy, repeated_table_to_parent_id_table,
                            parent_code_table_to_parent_id_table,
                            Classification)


if __name__ == "__main__":

    df = pd.read_csv("in/cat_localidad_MAY2015.csv.gz", encoding="ISO-8859-2",
                     compression="gzip")
    df.columns = ["state_code", "state_name", "state_name_short",
                  "municipality_code", "municipality_name",
                  "locality_code", "locality_name",
                  "latitude", "longitude", "altitude",
                  "map_code", "ambito",
                  "population_total", "population_male", "population_female",
                  "dwellings_occupied"]

    df = df[["state_code", "state_name", "municipality_code",
             "municipality_name", "locality_code",
             "locality_name"]]

    df.state_code = df.state_code.astype(str).str.zfill(2)
    df.municipality_code = df.municipality_code.astype(str).str.zfill(3)
    df.locality_code = df.locality_code.astype(str).str.zfill(4)

    df.municipality_code = df.state_code + df.municipality_code
    df.locality_code = df.municipality_code + df.locality_code

    df.state_name = df.state_name.str.title()
    df.municipality_name = df.municipality_name.str.title()
    df.locality_name = df.locality_name.str.title()

    df = df.rename(columns={"state_name": "name_en_state",
                            "municipality_name": "name_en_municipality",
                            "locality_name": "name_en_locality",
                            })

    h = Hierarchy(["state", "municipality", "locality"])

    parent_code_table = repeated_table_to_parent_id_table(
        df, h,
        level_fields={
            "state": ["name_en_state"],
            "municipality": ["name_en_municipality"],
            "locality": ["name_en_locality"],
        }
    )

    # TODO: This isn't the official classification level name but this makes
    # compatibility between colombia and mexico way easier
    parent_code_table.loc[parent_code_table.level == "state", "level"] = "department"

    # Drop the "locality" level since we don't use it
    parent_code_table = parent_code_table[parent_code_table.level != "locality"]

    # This adds a highest level element that represents the whole country
    mex = pd.Series({
        "code": "MEX",
        "name_en": "Mexico",
        "level": "country"
    })
    parent_code_table.loc[parent_code_table.level == "department", "parent_code"] = "MEX"

    parent_code_table = pd.concat([pd.DataFrame(mex).T, parent_code_table])
    parent_code_table = parent_code_table.reset_index(drop=True)

    h = Hierarchy(["country", "department", "municipality"])
    parent_id_table = parent_code_table_to_parent_id_table(parent_code_table, h)

    # Add MSA level
    msa = pd.read_stata("in/Mex_Metro_key.dta", encoding="latin-1")
    msa.columns = ["code", "name_en", "muni_code"]
    msa = msa.drop_duplicates(["code", "name_en"]).reset_index(drop=True)
    msa["level"] = "msa"
    msa["parent_code"] = msa["muni_code"].apply(lambda x: str(x).zfill(5)[:2])
    msa["code"] = msa["code"].astype(int).astype(str).str.zfill(2)

    lookup_table = parent_id_table[parent_id_table.level == "department"]
    lookup_table = lookup_table[["code"]].reset_index().set_index("code")['index']
    msa["parent_id"] = msa["parent_code"].map(lookup_table)
    del msa["muni_code"]
    del msa["parent_code"]

    parent_id_table = pd.concat([parent_id_table, msa]).reset_index(drop=True)

    parent_id_table["name"] = parent_id_table["name_en"]
    parent_id_table["name_es"] = parent_id_table["name_en"]
    parent_id_table["name_short_en"] = parent_id_table["name_en"]
    parent_id_table["name_short_es"] = parent_id_table["name_es"]

    # Get rid of antiquated colonial names of states
    state_level = (parent_id_table.level == "department")
    coahuila = (parent_id_table.code == "05")
    michoacan = (parent_id_table.code == "16")
    veracruz = (parent_id_table.code == "30")

    name_fields = ("name", "name_en", "name_es", "name_short_en",
                   "name_short_es")

    parent_id_table.loc[state_level & coahuila, name_fields] = u"Coahuila"
    parent_id_table.loc[state_level & michoacan, name_fields] = u"Michoac\u00e1n"
    parent_id_table.loc[state_level & veracruz, name_fields] = u"Veracruz"

    h = Hierarchy(["country", "department", "msa", "municipality"])
    c = Classification(parent_id_table, h)

    c.to_csv("out/locations_mexico_inegi.csv")
    c.to_stata("out/locations_mexico_inegi.dta")
