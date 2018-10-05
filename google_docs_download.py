import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from io import BytesIO
import os.path


def bytes_to_df(data, **kwargs):
    io = BytesIO()
    io.write(data)
    io.seek(0)
    return pd.read_csv(io, **kwargs)


def get_classification_from_gdrive(url, credentials_path=None):

    if credentials_path is None:
        dir = os.path.dirname(__file__)
        credentials_path = os.path.join(dir, "creds.json")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path,
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    gc = gspread.authorize(credentials)

    sheet = gc.open_by_url(url)
    hierarchy_sheet, names_sheet = sheet.worksheets()

    hierarchy = bytes_to_df(hierarchy_sheet.export(), dtype="str")
    names = bytes_to_df(names_sheet.export(), dtype={"code": "str"})

    return hierarchy, names
