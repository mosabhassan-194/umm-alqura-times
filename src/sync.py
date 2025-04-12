import os
import json
import datetime
from github import Github
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup Selenium headless browser
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=options)

try:
    # Get today's Gregorian date in Jazan timezone (UTC+3)
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    formatted_date = today.strftime("%Y-%m-%d")

    # Open Umm Al-Qura page
    driver.get("https://www.ummulqura.org.sa/")
    time.sleep(4)  # Allow time for full load

    # Locate table and find Jazan row
    rows = driver.find_elements(By.CSS_SELECTOR, "table#azanTable tbody tr")
    jazan_row = None

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and "جازان" in cells[0].text:
            jazan_row = cells
            break

    if not jazan_row:
        raise Exception("Jazan row not found in prayer table.")

    # Extract prayer times from the row
    prayer_times = {
        "date": formatted_date,
        "fajr": jazan_row[1].text.strip(),
        "sunrise": jazan_row[2].text.strip(),
        "dhuhr": jazan_row[3].text.strip(),
        "asr": jazan_row[4].text.strip(),
        "maghrib": jazan_row[5].text.strip(),
        "isha": jazan_row[6].text.strip()
    }

    print("Prayer times:", prayer_times)

    # Save to local file
    with open("src/jazan.json", "w", encoding="utf-8") as f:
        json.dump(prayer_times, f, ensure_ascii=False, indent=2)

    # Push updated file to GitHub
    gh_token = os.getenv("GH_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    g = Github(gh_token)
    repo = g.get_repo(repo_name)

    # Read the file content
    with open("src/jazan.json", "r", encoding="utf-8") as f:
        content = f.read()

    # Update the file on GitHub
    file_path = "src/jazan.json"
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, f"Auto update jazan.json for {formatted_date}", content, contents.sha)

    print("jazan.json updated on GitHub.")

finally:
    driver.quit()
