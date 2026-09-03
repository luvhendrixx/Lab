import json
import os

import requests
from dotenv import load_dotenv # type: ignore

_ = load_dotenv()

API_KEY = os.getenv("NEWS_API")

# Endpoint options: 'everything' or 'top-headlines'
url = "https://newsapi.org/v2/everything"

params = {
    "q": "Apple",  # Search keyword
    "language": "en",  # ISO-639-1 language code
    "from": "2026-09-02",
    "sortBy": "popularity",  # Options: relevancy, popularity, publishedAt
    "pageSize": 5,  # Max 100 per request
    "apiKey": API_KEY,  # Pass key via params or headers
}

response = requests.get(url, params=params)
data = response.json()

if response.status_code == 200:
    for article in data.get("articles", []):
        print(f"Author: {article['author']}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}\n---")

        with open("news.jsonl", "a") as file:
            pretty_json = json.dumps(article, indent=4)

            _ = file.write(pretty_json + "\n\n")
else:
    print(f"Error {response.status_code}: {data.get('message')}")
