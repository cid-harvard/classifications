
import pandas as pd
import numpy as np

import sys


DANE_HIERARCHY = ["section", "division", "group", "class"]


if __name__ == "__main__":
    assert(len(sys.argv) == 3)

    file_name = sys.argv[1]
    new_file_prefix = sys.argv[2]

    df = pd.read_table(file_name, encoding="utf-16")
    df = parse_dane(df)
    df = df[~df.duplicated(["code"])]
    df = df.reset_index(drop=True)
    df.columns = ["name", "level", "code"]

    from classification import (parent_code_table_to_parent_id_table,
                                Classification, Hierarchy,
                                ordered_table_to_parent_code_table)

    h = Hierarchy(DANE_HIERARCHY)
    df = ordered_table_to_parent_code_table(df, h)
    df = parent_code_table_to_parent_id_table(df, h)
    c = Classification(df, h)

    # weird bug where pandas infer_type was returning mixed instead of string
    c.table.code = c.table.code.astype(str)

    c.table.to_csv(new_file_prefix + ".csv", encoding="utf-8")
