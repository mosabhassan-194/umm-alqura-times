import requests
from bs4 import BeautifulSoup
from github import Github
from datetime import datetime
import json
import os

GITHUB_TOKEN = os.environ["GH_TOKEN"]
REPO_NAME = os.environ["REPO_NAME"]
FILE_PATH = "jazan.json"

def fetch_jazan_times():
    url = "https://www.ummulqura.org.sa/Default.aspx"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols and "جازان" in cols[0]:
            return {
                "fajr": cols[1],
                "dhuhr": cols[3],
                "asr": cols[4],
                "maghrib": cols[5],
                "isha": cols[6],
                "date": datetime.now().strftime("%Y-%m-%d")
            }
    return {"error": "Jazan not found"}


def upload_to_github(data):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        contents = repo.get_contents(FILE_PATH, ref="main")
        repo.update_file(FILE_PATH, "update jazan.json", json.dumps(data, ensure_ascii=False, indent=2), contents.sha, branch="main")
    except:
        repo.create_file(FILE_PATH, "create jazan.json", json.dumps(data, ensure_ascii=False, indent=2), branch="main")

upload_to_github(fetch_jazan_times())
