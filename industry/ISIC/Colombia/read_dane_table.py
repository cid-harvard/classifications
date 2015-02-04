#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import pandas as pd
import numpy as np

import StringIO
import sys


def parse_dane(df):
    """Convert messed-up DANE excel treelike correlation table format into a
    clean dataframe. You basically copy one side of the correlation table into
    a separate sheet, including header, and then save as UTF-16 text. Then you
    can read it like:

        df = pd.read_table("Correlativas3.0vs4_only3.txt", encoding="utf-16")

    The columns are "Section / Division", "Group", "Class", "Description", and
    examples are "SECCIÓN A" or "DIVISIÓN 01", "11", "111", "Producción
    especializada de café"."""

    msg = """Input doesn't contain 4 columns, you sure this is DANE format?"""
    assert len(df.columns) == 4, msg

    df = df.dropna(axis=0, how="all")
    original_columns = ["raw_secdiv", "raw_group", "raw_class", "name"]
    df.columns = original_columns

    df["type"] = np.NaN

    sections = df.raw_secdiv.str.extract("SECC.*N ([a-zA-Z]*)")
    df.loc[sections.dropna().index, "type"] = "section"
    df["section"] = sections

    divisions = df.raw_secdiv.str.extract("DIVIS.*N ([0-9]*)")
    divisions = divisions.map(lambda x: x.zfill(2) if type(x) == str else x)
    df.loc[divisions.dropna().index, "type"] = "division"
    df["division"] = divisions

    groups = df.raw_group.astype(str).str.extract("([0-9]*)").replace([""], np.NaN)
    groups = groups.map(lambda x: x.zfill(3) if type(x) == str else x)
    df.loc[groups.dropna().index, "type"] = "group"
    df["group"] = groups

    classes = df["raw_class"].astype(str).str.extract("([0-9]*)").replace([""], np.NaN)
    classes = classes.map(lambda x: x.zfill(4) if type(x) == str else x)
    df.loc[classes.dropna().index, "type"] = "class"
    df["class"] = classes

    # Put em all together
    df.fillna("", inplace=True)
    df["code"] = df["section"] + df["division"] + df["group"] + df["class"]

    # clean out original columns
    df = df.drop(["raw_secdiv", "raw_group", "raw_class", "section",
                  "division", "group", "class"], axis=1)

    df = df.set_index("code")

    return df


if __name__ == "__main__":
    assert(len(sys.argv) == 2)
    df = pd.read_table(sys.argv[1], encoding="utf-16")
    df = parse_dane(df)
    s = StringIO.StringIO()
    df.to_csv(s, encoding="utf-8")
    print s.getvalue()
