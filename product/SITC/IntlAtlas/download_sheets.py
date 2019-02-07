import sys

sys.path.append("../../..")
from google_docs_download import download_sheet

if __name__ == "__main__":

    sheets = [
        {
            "key": "16Wpxs5SL4s1YUus29lqCkbgC2acXQ19iXZwWEPvvcpM",
            "sheet_id": "0",
            "output_path": "./in/SITC_Rev2_Hierarchy",
        },
        {
            "key": "16Wpxs5SL4s1YUus29lqCkbgC2acXQ19iXZwWEPvvcpM",
            "sheet_id": "1207195644",
            "output_path": "./in/SITC_Rev2_Names",
        },
    ]

    for sheet in sheets:
        download_sheet(**sheet)
