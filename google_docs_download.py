import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from io import BytesIO

def bytes_to_df(data):
    io = BytesIO()
    io.write(data)
    io.seek(0)
    return pd.read_csv(io)

def get_classification_from_gdrive(url, credentials_path='creds.json'):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path,
        [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    gc = gspread.authorize(credentials)

    sheet = gc.open_by_url(url)
    hierarchy_sheet, names_sheet = sheet.worksheets()

    hierarchy = bytes_to_df(hierarchy_sheet.export())
    names = bytes_to_df(names_sheet.export())

    return hierarchy, names
