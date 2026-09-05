import getpass
import os
from typing import Any

import requests
from dotenv import load_dotenv  # type: ignore

_ = load_dotenv()

API_KEY = os.getenv("NEWS_API")

# Endpoint options: 'everything' or 'top-headlines'
url = "https://newsapi.org/v2/everything"

username = getpass.getuser()

print(f"Welome back {username}\n")


def fetch_articles(query: str, page_size: int = 20) -> list[dict[str, Any]]:
    # fetch artciles from the API and return them as a list of dicts
    # Endpoint options: 'everything' or 'top-headlines'
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",  # TODO: do our own sorting later
        "pageSize": page_size,
        "apiKey": API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # to throw an error handling early just incase instead of silent failing
    data = response.json()
    return data.get("articles", [])


def recency_score(published_at: str, half_life_hours: float = 12) -> float:










def main():
    query = input("What news are you looking for today 👀 ? ")

    page = 20

    result = fetch_articles(query, page)

    print(len(result))


if __name__ == "__main__":
    main()
