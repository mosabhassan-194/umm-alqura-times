import requests
from bs4 import BeautifulSoup
from github import Github
import datetime
import json
import os

# GitHub credentials via environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
FILE_PATH = "jazan.json"

def fetch_jazan_times():
    url = "https://www.ummulqura.org.sa/Default.aspx"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    table = soup.find("table", {"id": "ContentPlaceHolder1_GridView1"})

    if not table:
        print("DEBUG: Table not found — here’s a preview:")
        print(response.text[:1000])
        return {"error": "Prayer time table not found"}

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [td.text.strip() for td in cols]
        if len(cols) >= 7 and ("جازان" in cols[0] or "Jazan" in cols[0]):
            return {
                "fajr": cols[2],
                "dhuhr": cols[3],
                "asr": cols[4],
                "maghrib": cols[5],
                "isha": cols[6],
                "date": today,
                "fetched_at": datetime.datetime.now().isoformat()  # <== Always changes
            }

    return {"error": "Jazan not found"}

def upload_to_github(data):
    if not GITHUB_TOKEN or not REPO_NAME:
        print("❌ Missing GitHub token or repository name.")
        return

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    try:
        contents = repo.get_contents(FILE_PATH, ref="main")
        repo.update_file(
            FILE_PATH,
            f"update jazan.json on {datetime.datetime.now().isoformat()}",
            json.dumps(data, ensure_ascii=False, indent=2),
            contents.sha,
            branch="main"
        )
        print("✅ Updated existing file.")
    except Exception as e:
        print("⚠️ File not found. Creating new file.")
        repo.create_file(
            FILE_PATH,
            f"create jazan.json on {datetime.datetime.now().isoformat()}",
            json.dumps(data, ensure_ascii=False, indent=2),
            branch="main"
        )

upload_to_github(fetch_jazan_times())
