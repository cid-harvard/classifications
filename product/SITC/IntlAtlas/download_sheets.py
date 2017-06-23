from google_docs_download import get_classification_from_gdrive

# SITC Rev2
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1pgVamRALdpc7IlmzkvJrLk4Hkm4H4wvNyoIycQ6wr_E/edit#gid=1207195644")
hierarchy.to_csv("./in/SITC_Rev2_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/SITC_Rev2_Names.tsv", sep="\t", index=False, encoding="utf-8")
