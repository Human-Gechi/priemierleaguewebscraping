# priemierleaguewebscraping
# 🕸️ Web Scraping Pipeline with Selenium & Spreadsheet Export

## 📌 Project Overview

This project automates the end-to-end process of discovering web pages via keyword search, extracting tabular data from those pages using **Selenium**, and delivering the results as **structured spreadsheets via email**. Each spreadsheet reflects a single webpage, with each table saved on a separate sheet, clearly labeled by the section header found just above it on the original page.

---

## 🔄 Workflow

### 1. 🔍 Keyword-Based URL Discovery
- Selenium is used to search the target website for pages containing specific **keywords**.
- All matching page links are saved to `selenium_scrapped.txt`.

### 2. 🌐 Webpage Table Extraction
- The scraper reads each URL from `selenium_scraped.txt`.
- Selenium opens each page to ensure all dynamic content is fully rendered.
- All HTML tables are located.
- For each table, the **nearest header just above it** (e.g., `<h2>`,) is used to name the corresponding spreadsheet **sheet/tab**.

### 3. 📊 Spreadsheet Generation
- Each webpage becomes one Excel spreadsheet
- Spreadsheet names are the generate by splitting after /comps/ 'https://fbref.com/en/comps/season/1956-1957' so the spreadsheet name becomes season-1956-1957
- Each spreadsheet contains:
  - Multiple **sheets** (one per table)
  - Sheet names based on the **section heading above each table**
  - Clean formatting via `pandas`
- The original URL is optionally included in the spreadsheet metadata or first sheet for traceability.

### 4. 📤 Email Delivery
- Once all spreadsheets are generated, they are automatically **emailed to designated recipients**.


## 🧰 Technologies Used
- **Selenium** – For automated web navigation and keyword-based link extraction
- **Pandas** – For table parsing and cleanup
- **Googleapi/servics** - For sheets handling
- **urllib** - For links parsing slash sending request


