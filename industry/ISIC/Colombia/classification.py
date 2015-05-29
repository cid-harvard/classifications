import pandas as pd
import numpy as np

class Reader(object):
    def __init__(self):
        pass

    @staticmethod
    def read(self):
        pass


class DANEReader(Reader):

    LEVELS = []

    def __init__(self, file_name):
        pass

    def parse(self):
        pass

    def get_parent_level(self):
        pass

    def set_parents(self):
        pass


def hierarchy_get_parent(hierarchy, level):
    assert level in hierarchy

    parent_index = hierarchy.index(level) - 1
    if parent_index < 0:
        return None
    else:
        return hierarchy[parent_index]


def parent_code_table_to_parent_id_table(df, hierarchy):
    """From a classification that has parent_code, go to one that has
    parent_id."""

    def replace(x):
        parent_level = hierarchy.parent(x.level)

        if parent_level is None:
            x["parent_id"] = None
        else:
            parent_rows = df[(df.code == x.parent_code)
                             & (df.level == parent_level)]
            x["parent_id"] = parent_rows.index[0]

        return x.drop("parent_code")

    return df.apply(replace, axis=1)

# TODO: ordered table to parent id table (like DANE)

def repeated_table_to_parent_id_table(df, hierarchy):

    # Check there is a code and name field for every entry in the hierarchy
    for level in hierarchy:
        for suffix in ["code", "name"]:
            field_name = "{}_{}".format(level, suffix)
            assert field_name in df.columns, "Missing field: {}".format(field_name)

    # Check there are no duplicate codes for the same country + dept + muni
    # etc.
    codes = ["{}_code".format(x) for x in hierarchy]
    assert df[codes].duplicated().any() == False

    new_table = []
    for idx, row in df.iterrows():

        parent_codes = [None]

        for level in hierarchy:
            name = row["{}_name".format(level)]
            code = row["{}_code".format(level)]
            new_table.append([code, name, level, parent_codes[-1]])
            parent_codes.append(code)

    new_df = pd.DataFrame(new_table, columns=["code", "name", "level", "parent_code"])
    new_df = new_df[~new_df.duplicated()]
    #new_df = new_df.reset_index(drop=True)
    new_df.level = new_df.level.astype("category")
    return new_df




import collections

class Hierarchy(collections.Mapping):

    def __init__(self, items):
        self.items = items

    def __contains__(self, item):
        return item in self.items

    def __repr__(self):
        return "<Hierarchy {}>".format(self.items)

    def __getitem__(self, item):
        if type(item) == int:
            return self.items[item]
        elif isinstance(item, basestring):
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
        elif isinstance(item, basestring):
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
        assert self.table.index.is_monotonic_increasing is True

        assert (self.table[["name", "level", "code"]].isnull()
                .any().any() == False)

        assert self.table.index.dtype == np.int
        assert self.table.parent_id.dtype == np.number

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

        # Mapping: id -> parent_id
        parents = df.loc[df.level == from_level, ["parent_id"]]

        # Returns parent's parent
        def traverse_up(x):
            x.parent_id = df.loc[int(x.parent_id)].parent_id
            return x

        for _ in range(from_index - to_index - 1):
            parents = parents.apply(traverse_up, axis=1)

        parents.columns = [to_level]
        parents.index.name = from_level

        return parents
