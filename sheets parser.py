import gspread
from google.oauth2.service_account import Credentials
import logging
from webscrapping_all_scale import Allscale, find_url_by_keywords, logger
logging.basicConfig(level=logging.INFO)

class SheetsManager:
    def __init__(self):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file(
            'crested-pursuit-457714-c8-012a42374576.json',
            scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)
