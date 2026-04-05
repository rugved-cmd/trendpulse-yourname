# task1_data_collection.py

import requests
import time
import json
import os
from datetime import datetime

# API URLs
TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header required
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# function to find category based on title
def get_category(title):
    title = title.lower()
    for cat in categories:
        for word in categories[cat]:
            if word in title:
                return cat
    return "technology"

def main():
    all_data = []
    count = {cat: 0 for cat in categories}

    # Step 1: get top 500 IDs
    try:
        res = requests.get(TOP_URL, headers=headers)
        res.raise_for_status()
        ids = res.json()[:500]
    except Exception as e:
        print("Error getting IDs:", e)
        return

    # Step 2: loop category-wise
    for cat in categories:
        print("Collecting:", cat)

        for id in ids:
            if count[cat] >= 25:
                break

            try:
                r = requests.get(ITEM_URL.format(id), headers=headers)
                r.raise_for_status()
                story = r.json()
            except Exception as e:
                print("Error fetching story:", id)
                continue

            # skip invalid
            if not story or "title" not in story:
                continue

            title = story["title"]

            # check category
            assigned = get_category(title)

            if assigned == cat:
                record = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": cat,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                all_data.append(record)
                count[cat] += 1

        # wait 2 seconds after each category
        time.sleep(2)

    # Step 3: save file
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)

    print("Collected", len(all_data), "stories. Saved to", filename)


# run program
if __name__ == "__main__":
    main()