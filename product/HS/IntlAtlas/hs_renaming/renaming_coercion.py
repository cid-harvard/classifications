import pandas as pd
from linnaeus import classification

hs_classification = classification.load(
    "/Users/brl669/projects/classifications/product/HS/IntlAtlas/out/hs92_atlas.csv"
)

df = pd.read_csv("./hs_6digit_renaming.csv")
df.columns = [
    "code",
    "full_name",
    "long_name",
    "short_name",
    "4digit_name",
    "4digit_total",
    "6digit_total",
    "6digit_share",
    "4digit_code",
    "current_4digit_short_name",
    "new_4digit_short_name",
    "2digit_code",
    "2digit_name",
]

six_digit = df[["code", "long_name", "short_name"]]
four_digit = df[["4digit_code", "new_4digit_short_name"]].drop_duplicates()

# Six Digit
six_digit["code"] = six_digit["code"].apply(lambda x: f"{x:06}")
six_digit["level"] = "6digit"
six_digit = six_digit.rename(
    {"long_name": "name_en", "short_name": "name_short_en"}, axis=1
)

# TODO: missing codes at tail, XXXXXX, 999999, 9999AA...

# Four Digit
four_digit["4digit_code"] = four_digit["4digit_code"].apply(lambda x: f"{x:04}")
four_digit = four_digit.merge(
    hs_classification.table[hs_classification.table.level == "4digit"],
    left_on="4digit_code",
    right_on="code",
    how="right",
)
four_digit["name_short_en"] = four_digit.new_4digit_short_name.combine_first(
    four_digit.name_short_en
)
four_digit = four_digit.rename({"4digit_code": "code"}, index=1)
four_digit = four_digit[
    ["code", "level", "name_en", "name_es", "name_short_en", "name_short_es"]
]

# Two Digit

# TODO: Included in this ticket: update "ICT" so that its long name (i.e. in tooltip)
# is "Information, Communication and Technology"

# Create new sheet
output = pd.concat([four_digit, six_digit])
