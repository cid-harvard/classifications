from google_docs_download import get_classification_from_gdrive

hierarchy, names = get_classification_from_gdrive(
    "https://docs.google.com/spreadsheets/d/1y6UUixlfbW0jLnUtKycHF1ICUaD-kROQIvscwCGFzzE/edit#gid=0"
)
hierarchy.to_csv(
    "./in/HS92_Atlas_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8"
)
names.to_csv("./in/HS92_Atlas_Names.tsv", sep="\t", index=False, encoding="utf-8")
