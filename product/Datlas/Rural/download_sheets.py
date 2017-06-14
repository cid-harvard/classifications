from google_docs_download import get_classification_from_gdrive

# Livestock
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1eTJMg5jaKDS2ohkhr9AA8Lo7gUR0XOtbfZvkcYJpmVQ/edit")
hierarchy.to_csv("./in/Livestock_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/Livestock_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Agricultural Products
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1UV80vfHq0Gopy7Gpxb9SyQ41PfCN3wZthy-Cp5pSf_E/edit#gid=0")
hierarchy.to_csv("./in/AgProducts_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/AgProducts_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Farm types
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1ma0pznYRwg9JDdjMJKDvh-V9oyXwssBMc3X6p-yw_tI/edit#gid=0")
hierarchy.to_csv("./in/FarmType_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/FarmType_Names.tsv", sep="\t", index=False, encoding="utf-8")
