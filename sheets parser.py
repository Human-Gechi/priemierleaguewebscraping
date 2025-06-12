import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.chrome.options import Options
import logging
from webscrapping_all_scale import Allscale, find_url_by_keywords, logger
import re
import pandas as pd

logging.basicConfig(level=logging.INFO)

class SheetsManager:# base class for google sheets updates
    def __init__(self, email):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file(
            'crested-pursuit-457714-c8-012a42374576.json',
            scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)
        self.email = email
        options = Options()# options to avoid being identified as a scraper bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/135.0.0.0 Safari/537.36"
        )
    def create_spreadsheet_with_several_tables(self, url, tables): # functio to create spreadsheeets with atbnles
        spreadsheet_title = url.split('/comps/', 1)[-1]
        spreadsheet_title = re.sub(r'[\\/*?:"<>|]', "-", spreadsheet_title) or "data"# repalcing special charecters in the url addres with a hypen as a title for the spreadsheet
        spreadsheet = self.client.create(spreadsheet_title)
        spreadsheet.share(self.email, perm_type='user', role='writer')
        logging.info(f"Created spreadsheet '{spreadsheet_title}' and shared with {self.email}.")

        # Add each table as a worksheet/tab
        for name_of_table, df in tables:
            # Get everything after the last two slashes of the url or link
            sheet_name = re.sub(r'[\\/*?:"<>|]', "-", name_of_table) or "table"
            df = df.replace([float('inf'), float('-inf')], pd.NA)
            df = df.fillna('')
            try:
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=str(len(df)+1), cols=str(len(df.columns)))
            except Exception as e:
                logging.warning(f"Could not create worksheet '{sheet_name}': {e}") # logging message if worksheet could not be created
                continue
            worksheet.update([df.columns.values.tolist()] + df.values.tolist()) # converting dataframe to a flat file
            logging.info(f"Uploaded data to worksheet '{sheet_name}'.") #logger message indicating tables have been uploaded successfully

        try:
            spreadsheet.del_worksheet(spreadsheet.sheet1)
        except Exception:
            pass

        print(f"Spreadsheet '{spreadsheet_title}' created and shared with {self.email}.")
#main script for execution
if __name__ == "__main__":
    driver_path = r"C:\\Users\\HP\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"
    scraper = Allscale(driver_path) # Initialize the Allscale scraper
    logger.info("Allscale scraper initialized.")
    writer_email = input("Enter the email address to share the Google Sheets with: ").strip()
    if not writer_email:
        raise ValueError("Provide an email address")
    sheets_manager = SheetsManager(writer_email)# wrting table to Google Sheets
    user_input = input("Enter keywords to search for URLs (separated by spaces): ")# user input for finding links to scrape
    user_input = user_input.split()

    urls = find_url_by_keywords("selenium_scraped.txt", *user_input)
    try:
        for u in urls:
            scraper.check_url(u)
            #upload all tables found in each url as sheets intto a particular spreadsheet
            tables = getattr(scraper, "dataframes", [])
            if tables:
                sheets_manager.create_spreadsheet_with_several_tables(u, tables)
                print(f"Created Google Spreadsheet for: {u}")
        logger.info("All URLs processed.")
    finally:
        scraper.driver.quit()