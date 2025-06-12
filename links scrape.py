from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time

# Path to your chromedriver on my system
CHROMEDRIVER_PATH = r"C:\\Users\\HP\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"  # <- Update this path!

# Set up Chrome options (headless browser)
chrome_options = Options() # options to avoid being identified as a bot
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--enable-unsafe-swiftshader')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3")

service = Service(CHROMEDRIVER_PATH)
# Initialize WebDriver with options and service
driver = webdriver.Chrome(service=service, options=chrome_options)
#base url for wepages i want to extract data from
base_url = "https://fbref.com/en/comps"
visited = set()
to_visit = [base_url]
internal_links = set()
with open("selenium_scraped.txt", "a") as file:
    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        print(f"Visiting: {url}")
        visited.add(url)

        try:
            driver.get(url)
            time.sleep(2)

            links = driver.find_elements(By.TAG_NAME, "a")
        except Exception as e:
            print(f"Failed to load {url}: {e}")
            continue

        for link in links:
            href = link.get_attribute("href")
            if href:
                full_url = urljoin(base_url, href)
                full_url = full_url.split('#')[0]

                if full_url.startswith(base_url): #identifying links that start with the base_url
                    if full_url not in visited and full_url not in to_visit:
                        internal_links.add(full_url)
                        to_visit.append(full_url)
                        file.write(full_url + "\n")  # Write immediately while scrapping
        time.sleep(1)
