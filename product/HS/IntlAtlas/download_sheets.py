import sys

sys.path.append("../../..")
from google_docs_download import download_sheet

if __name__ == "__main__":

    sheets = [
        {
            "key": "1xPMiNhKf8DKMMU3ntUADQsouCWOLM2-2lY_2o58gSIQ",
            "sheet_id": "0",
            "output_path": "./in/HS92_Atlas_Hierarchy",
        },
        {
            "key": "1xPMiNhKf8DKMMU3ntUADQsouCWOLM2-2lY_2o58gSIQ",
            "sheet_id": "1029116973",
            "output_path": "./in/HS92_Atlas_Names",
        },
    ]

    for sheet in sheets:
        download_sheet(**sheet)
