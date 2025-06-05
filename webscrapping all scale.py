import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import re
# Importing necessary libraries
# Load environment variables
load_dotenv()

# Seting up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="allscale.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

# Reading links from the text file
with open("selenium_scraped.txt", "r") as file:
    urls = [line.strip() for line in file if line.strip()]
logger.info("Found the URLs")
class Allscale:
    def __init__(self, driver_path):
        options = Options()
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

        service = Service(driver_path)  # Initializing WebDriver path in the base class
        self.driver = webdriver.Chrome(service=service, options=options)
        logger.info("Initialized Chrome WebDriver.")

    def check_url(self, url):
        try:
            self.driver.get(url)
            print(f"Checking URL: {url}")
            time.sleep(3)  # Time for the page to load in the website

            # Find all h2 headers and tables in each webpage
            h2_elements = self.driver.find_elements(By.TAG_NAME, "h2")
            tables = self.driver.find_elements(By.TAG_NAME, "table")

            # Get the locations of h2s and tables
            h2_locations = [(h2.location['y'], h2.text) for h2 in h2_elements]

            self.dataframes = []

            for table in tables:
                try:
                    table_y = table.location['y']
                    # Find the closest preceding h2
                    preceding_h2 = ""
                    for y, text in reversed(h2_locations):
                        if y < table_y:
                            preceding_h2 = text
                            break

                    headers = []
                    for th in table.find_elements(By.TAG_NAME, "th"):
                        header_text = th.text.strip()
                        if header_text and not th.find_elements(By.TAG_NAME, "a"):
                            headers.append(header_text)

                    if headers:
                        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
                        data = []

                        for row in rows:
                            try:
                                data_th = row.find_element(By.TAG_NAME, "th").text
                            except:
                                data_th = ""

                            cells = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
                            full_row = [data_th] + cells
                            data.append(full_row)

                        df = pd.DataFrame(data, columns=headers)
                        self.dataframes.append((preceding_h2, df))

                except Exception as e:
                    logger.error(f"Error extracting data from table: {e}")
                    print(f"Error extracting data from table: {e}")
                    continue

            for name_of_table, df in self.dataframes:
                filename = f"{name_of_table}.csv"
                df.to_csv(filename, index=False)
                print(f"Saved {filename}")

            logger.info(f"Processed {url} successfully.")
            return f"Processed {url} successfully. Data saved to CSV files."
        except Exception as e:
            logger.error(f"Error while checking {url}: {e}")
            print(f"Error while checking {url}: {e}")
        return "Error: Unable to process page."
# Main detail init
if __name__ == "__main__":
    driver_path = r"C:\\Users\\HP\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"
    scraper = Allscale(driver_path)

    # Get number of URLs from user
    num_urls = int(input("How many URLs would you like to check? "))
    num_urls = min(num_urls, len(urls))

    for i in range(num_urls):  # Process users specified number of URLs
        result = scraper.check_url(urls[i])
        print(result)  # Print output for each URL in the terminal

    scraper.driver.quit() #closing webbrowser