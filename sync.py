import requests
from bs4 import BeautifulSoup
from github import Github
import datetime
import json
import os

# GitHub credentials
GITHUB_TOKEN = "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"
REPO_NAME = "mosabhassan-194/umm-alqura-times"
FILE_PATH = "jazan.json"

def fetch_jazan_times():
    url = "https://www.ummulqura.org.sa/Default.aspx"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    today = datetime.datetime.now().strftime("%d-%m-%Y")
    table = soup.find("table", {"id": "ContentPlaceHolder1_GridView1"})

    if not table:
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
                "date": today
            }

    return {"error": "Jazan not found"}

def upload_to_github(data):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    try:
        contents = repo.get_contents(FILE_PATH, ref="main")
        repo.update_file(FILE_PATH, "update jazan.json", json.dumps(data, ensure_ascii=False, indent=2), contents.sha, branch="main")
        print("Updated existing file.")
    except Exception as e:
        print("File not found. Creating new file.")
        repo.create_file(FILE_PATH, "create jazan.json", json.dumps(data, ensure_ascii=False, indent=2), branch="main")

upload_to_github(fetch_jazan_times())
