#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import pandas as pd
import numpy as np

import os.path
import sys


DANE_HIERARCHY = ["section", "division", "group", "class"]


def parse_dane(df):
    """Convert messed-up DANE excel treelike correlation table format into a
    clean dataframe. You basically copy one side of the correlation table into
    a separate sheet, including header, and then save as UTF-16 text. Then you
    can read it like:

        df = pd.read_table("Correlativas3.0vs4_only3.txt", encoding="utf-16")

    The columns are "Section / Division", "Group", "Class", "Description", and
    examples are "SECCIÓN A" or "DIVISIÓN 01", "11", "111", "Producción
    especializada de café".

    Returns items at the same order as the spreadsheet, may contain duplicates.
    """

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

    df["name"] = df.name.str.strip()

    # Put em all together
    df.fillna("", inplace=True)
    df["code"] = df["section"] + df["division"] + df["group"] + df["class"]

    # clean out original columns
    df = df.drop(["raw_secdiv", "raw_group", "raw_class", "section",
                  "division", "group", "class"], axis=1)

    df = df.reset_index(drop=True)

    return df


def get_parent_code(row_type, hierarchy):
    """Given a list that defines a hierarchy from highest to lowest level, find
    the parent of the given level."""
    try:
        current_level = hierarchy.index(row_type)
    except ValueError:
        raise ValueError("Hierarchy level {} does not exist. Valid: {}",
                         row_type, hierarchy)

    if current_level == 0:
        return None

    parent_level = current_level - 1
    return hierarchy[parent_level]


def set_parents(df, hierarchy):
    """Go through a parsed classification spreadsheet and infer the hierarchy
    from the order of the items. Assumed: a lower level item must be the child
    of the previous higher level item."""

    hier_index = dict(zip(hierarchy, [None] * 4))

    df["parent"] = np.NaN

    def traversal_iteration(x):
        hier_index[x.type] = x.code
        parent_code = get_parent_code(x.type, hierarchy)
        if parent_code is not None:
            x.parent = hier_index[parent_code]
        return x

    df = df.apply(traversal_iteration, axis=1)
    return df


def filter_by_hierarchy_level(df, levels):
    return df[df.type.isin(levels)]


def build_aggregation_table(df, start_level, end_level, hierarchy):
    """Build a table from one level of a hierarchy to another, like 2digit to
    4digit."""

    assert(start_level in hierarchy)
    assert(end_level in hierarchy)

    start_index = hierarchy.index(start_level)
    end_index = hierarchy.index(end_level)

    assert(start_index < end_index)

    lookup_table = df[["code", "type", "parent"]].set_index("code").copy()
    parents = df.loc[df.type == end_level, ["code", "parent"]]

    def update(x):
        x.parent = lookup_table.loc[x.parent].parent
        return x

    for _ in range(end_index - start_index - 1):
        parents = parents.apply(update, axis=1)

    parents = parents.set_index("code")
    parents.columns = [start_level]
    parents.index.name = end_level

    return parents


if __name__ == "__main__":
    assert(len(sys.argv) == 3)

    file_name = sys.argv[1]
    new_file_prefix = sys.argv[2]

    df = pd.read_table(file_name, encoding="utf-16")
    df = parse_dane(df)
    df = df[~df.duplicated(["code"])]
    df = set_parents(df, DANE_HIERARCHY)

    file_prefix = os.path.basename(file_name)

    df.columns = ["name", "level", "code", "parent_code"]

    from classification import parent_code_table_to_parent_id_table, Classification, Hierarchy
    h = Hierarchy(DANE_HIERARCHY)
    df = parent_code_table_to_parent_id_table(df, h)
    c = Classification(df, h)

    # weird bug where pandas infer_type was returning mixed instead of string
    df.code = df.code.astype(str)

    df.to_csv(new_file_prefix + ".csv", encoding="utf-8", index=False)
    df.to_stata(new_file_prefix + ".dta", encoding="latin-1", write_index=False)
    # agg = build_aggregation_table(df, "section", "class", DANE_HIERARCHY)
    #agg = agg.merge(df.set_index("code")[["name"]], left_on="section", right_index=True)
