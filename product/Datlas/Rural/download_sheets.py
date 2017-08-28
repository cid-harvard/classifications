from google_docs_download import get_classification_from_gdrive

# Livestock
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1eTJMg5jaKDS2ohkhr9AA8Lo7gUR0XOtbfZvkcYJpmVQ/edit")
hierarchy.to_csv("./in/Livestock_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/Livestock_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Agricultural Products (Census)
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1UV80vfHq0Gopy7Gpxb9SyQ41PfCN3wZthy-Cp5pSf_E/edit#gid=0")
hierarchy.to_csv("./in/AgProducts_Census_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/AgProducts_Census_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Agricultural Products (Non-Census)
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1yye7lVVVEsfmbeVTMY41tymH9mIU84CiUXOwi1wx-lI/edit#gid=743162393")
hierarchy.to_csv("./in/AgProducts_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/AgProducts_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Agricultural Products (Non-Census/expanded)
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1QcuYPynTvfobkkrudvBQxIzPRhhY6AxxRdosQ25Fl38/edit#gid=743162393")
hierarchy.to_csv("./in/AgProducts_Expanded_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/AgProducts_Expanded_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Farm types
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1ma0pznYRwg9JDdjMJKDvh-V9oyXwssBMc3X6p-yw_tI/edit#gid=0")
hierarchy.to_csv("./in/FarmType_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/FarmType_Names.tsv", sep="\t", index=False, encoding="utf-8")


# Land Use
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/17EoKvwQKujYRCKzh2odu--bpR0d2grigrWDn4CjRaeg/edit#gid=1207195644")
hierarchy.to_csv("./in/LandUse_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/LandUse_Names.tsv", sep="\t", index=False, encoding="utf-8")

# Farmsize Type
hierarchy, names = get_classification_from_gdrive("https://docs.google.com/spreadsheets/d/1ORWQDmc0wDPiOW4nBgi40JsKjL7tLm-YzaGBO6TP0Jk/edit#gid=1207195644")
hierarchy.to_csv("./in/FarmSize_Hierarchy.tsv", sep="\t", index=False, encoding="utf-8")
names.to_csv("./in/FarmSize_Names.tsv", sep="\t", index=False, encoding="utf-8")
