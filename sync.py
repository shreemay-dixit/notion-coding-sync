import requests
from datetime import datetime

import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
LEETCODE_USERNAME = os.getenv("LEETCODE_USERNAME")


def fetch_leetcode_stats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "total_solved": data["totalSolved"],
            "easy": data["easySolved"],
            "medium": data["mediumSolved"],
            "hard": data["hardSolved"]
        }
    else:
        raise Exception(f"Failed to fetch stats from LeetCode. HTTP {response.status_code}")

def send_to_notion(stats):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Date": {
                "date": {
                    "start": datetime.today().strftime("%Y-%m-%d")
                }
            },
            "Platform": {
                "select": {
                    "name": "LeetCode"
                }
            },
            "Total Solved": {
                "number": stats["total_solved"]
            },
            "Easy": {
                "number": stats["easy"]
            },
            "Medium": {
                "number": stats["medium"]
            },
            "Hard": {
                "number": stats["hard"]
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Notion response:", response.status_code, response.text)

def main():
    try:
        stats = fetch_leetcode_stats(LEETCODE_USERNAME)
        send_to_notion(stats)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
