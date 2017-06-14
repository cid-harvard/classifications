import pandas as pd
import numpy as np
from six import string_types

import collections
import os.path

import csv

from unidecode import unidecode


def load(path):
    path = os.path.join(os.path.dirname(__file__), path)
    return Classification.from_csv(path)


def parent_code_table_to_parent_id_table(df, hierarchy):
    """From a classification that has parent_code, go to one that has
    parent_id."""

    code_table = df[["code", "level"]].reset_index()
    code_table.columns = ["parent_id", "parent_code", "parent_level"]

    df["parent_level"] = df["level"]\
        .map(hierarchy.parent)\
        .fillna(value=pd.np.nan)

    return df.merge(code_table,
                    on=["parent_level", "parent_code"],
                    how="left")\
        .drop(["parent_code", "parent_level"], axis=1)


def ordered_table_to_parent_code_table(df, hierarchy):

    # Mapping of current level -> code
    hier_index = dict(list(zip(hierarchy, [None] * 4)))

    df["parent_code"] = np.NaN

    def traversal_iteration(x):
        hier_index[x.level] = x.code
        parent_level = hierarchy.parent(x.level)
        if parent_level is not None:
            x.parent_code = hier_index[parent_level]
        return x

    df = df.apply(traversal_iteration, axis=1)
    return df


def repeated_table_to_parent_id_table(df, hierarchy, level_fields={}):
    """
    Convert from the "merged" table format to a parent_id format, e.g.

      level1  level0
      cats    animals
      dogs    animals
      cod     fish
      salmon  fish

    into:

      code    level   name
      cats    level1  Cats

    and to do that, specify level_fields=
      {
          "level0": [],
          "level1": []
      }
    """

    # Check there is a code and name field for every entry in the hierarchy
    for level in hierarchy:
        for field_name in level_fields[level]:
            assert field_name in df.columns, "Missing field: {}".format(field_name)

    # Check there are no duplicate codes for the same country + dept + muni
    # etc.
    codes = ["{}_code".format(x) for x in hierarchy]
    assert df[codes].duplicated().any() == False
    assert pd.Series(hierarchy).isin(list(level_fields.keys())).all()


    new_table = []
    for idx, row in df.iterrows():

        parent_codes = [None]

        for level in hierarchy:
            code = row["{}_code".format(level)]

            row_dict = {
                "code": code,
                "level": level,
                "parent_code": parent_codes[-1]
            }

            for field in level_fields[level]:

                # Strip _section from the end
                assert field.endswith("_"+ level)
                new_field_name = field[:-1 * len(level) - 1]

                row_dict[new_field_name] = row[field]

            new_table.append(row_dict)
            parent_codes.append(code)


    new_df = pd.DataFrame(new_table)
    new_df = new_df[~new_df.duplicated()]
    new_df = new_df.reset_index(drop=True)
    # new_df.level = new_df.level.astype("category")

    return new_df


class Hierarchy(collections.Mapping):

    def __init__(self, items):
        self.items = list(items)

    def __contains__(self, item):
        return item in self.items

    def __repr__(self):
        return "<Hierarchy {}>".format(self.items)

    def __getitem__(self, item):
        if type(item) == int:
            return self.items[item]
        elif isinstance(item, string_types):
            return self.items.index(item)
        else:
            raise KeyError("Don't know how to find {} in hierarchy\
                           {}".format(item, self))

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return len(self.items)

    def move(self, item, amount):
        if type(item) == int:
            index = item
        elif isinstance(item, string_types):
            index = self[item]
        else:
            raise KeyError("Don't know how to find {} in hierarchy\
                           {}".format(item, self))

        parent_index = index + amount
        if parent_index < 0:
            return None
        elif parent_index >= len(self.items):
            return None

        return self.items[parent_index]

    def parent(self, item):
        return self.move(item, -1)

    def child(self, item):
        return self.move(item, 1)


class Classification(object):
    """
    - id: Numeric id that is unique across levels and ordered in classification
    order
    - code: Code of the current classification element expressed as a string
    - parent_id: Numeric id of parent code
    - name: Name of the element
    - level: The element's position in the hierarchy
    - extra fields """

    REQUIRED_FIELDS = ["code", "parent_id", "name", "level"]

    def __init__(self, table, levels):
        self.table = table
        self.levels = levels

        assert type(table) is pd.DataFrame
        self.validate()

    def validate(self):

        for field in ["code", "parent_id", "name", "level"]:
            assert field in self.table.columns

        assert self.table.index.has_duplicates is False
        assert self.table.index.hasnans is False
        assert self.table.index.values[0] == 0

        # Check that index is in sorted order
        assert sorted(self.table.index) == self.table.index.tolist()

        assert (self.table[["name", "level", "code"]].isnull()
                .any().any() == False)

        assert np.issubdtype(self.table.index.dtype, np.int)
        assert np.issubdtype(self.table.parent_id.dtype, np.number)

        assert self.table.code.dtype == np.object_
        assert self.table.name.dtype == np.object_
        assert self.table.level.dtype == np.object_


    def level(self, level):
        """Return only codes from a specific aggregation level."""
        assert level in self.levels
        return self.table[self.table.level == level]

    def aggregation_table(self, from_level, to_level, names=False):
        """Return mapping from higher level x to lower level y"""

        assert from_level != to_level
        assert from_level in self.levels
        assert to_level in self.levels

        # Make the mapping from the higher level to the lower level
        from_index = self.levels[from_level]
        to_index = self.levels[to_level]

        if not (from_index > to_index):
            raise ValueError("""{} is higher level than {}. Did you specify them
                             backwards?""".format(from_level, to_level))

        # Shortcut
        df = self.table

        # Table of all ids and all parents
        parent_table = df[["parent_id"]]

        # Mapping to traverse with: id -> parent_id at a given from_level
        parents = df.loc[df.level == from_level, ["parent_id"]]

        for _ in range(from_index - to_index - 1):
            parents.parent_id = parents.parent_id.map(parent_table.parent_id)

        parents.columns = [to_level]
        parents.index.name = from_level

        return parents

    def to_merged_table(self):
        """Turn table into a format where every line has all digit level codes
        and names. For example, it'd have the 0112, 011, 01, A."""
        data = None
        prev_level = None

        for level in reversed(list(self.levels)):

            levelize = lambda x: x + "_" + level
            prev_levelize = lambda x: x + "_" + prev_level

            current_level = self\
                .level(level)\
                .rename(columns=levelize)\
                .drop("level_" + level, axis=1)

            if data is None:
                data = current_level
            else:
                data = data.merge(current_level,
                                  left_on=prev_levelize("parent_id"),
                                  right_index=True,
                                  how="inner",
                                  suffixes=("_" + prev_level, "_" + level)
                                  )
                data = data.drop(prev_levelize("parent_id"), axis=1)
            prev_level = level

        data = data.drop(levelize("parent_id"), axis=1)
        return data

    @staticmethod
    def from_csv(path):
        df = pd.read_csv(path, dtype={"code": "str"}, index_col=0)
        h = Hierarchy(df.level.unique())
        return Classification(df, h)

    def to_csv(self, path):
        self.table.to_csv(path, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

    def to_stata(self, path):
        merged_table = self.to_merged_table().copy()

        for column in merged_table.columns:
            col = merged_table[column]
            if col.dtype == pd.np.object_:

                # Chop long fields because STATA format doesn't support them
                if pd.lib.infer_dtype(col.dropna()) == "string":
                    merged_table[column] = col.str.slice(0, 244)
                elif pd.lib.infer_dtype(col.dropna()) == "unicode":
                    merged_table[column] = col.str.slice(0, 244).map(unidecode, na_action="ignore")

                # Workaround issue in pandas where to_stata() rejects an object
                # field full of nulls
                if col.isnull().all():
                    merged_table[column] = col.astype(float)

        merged_table.to_stata(path, encoding="latin-1", write_index=False)
