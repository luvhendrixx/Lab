import getpass
import json
import os
import webbrowser
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv("QUOTE_API_KEY")


def main():
    username = getpass.getuser()
    try:
        while True:
            # Get choice from user
            choice = user_prompt(username)

            # Route choice to function
            proc_user_choice(choice)
            print("\n" + "=" * 40)

    except KeyboardInterrupt:
        print(f"\n\nAlright then, see you soon {username.capitalize()}! 👋")


def user_prompt(username: str) -> str:
    print("NOTE: HIT CTRL + C IF YOU WANT TO QUIT THE PROGRAMME!!")

    print("\n" + "=" * 40)

    choices = {
        "A": "Add a URL (shorten a URL)",
        "B": "Delete a URL",
        "C": "Use a URL (open in browser)",
        "D": "Search for a URL",
        "E": "Add a note beside a URL",
        "F": "Get Today's quote of the day (cause why not 🤷‍♂️)",
    }

    while True:
        print()
        for key, desc in choices.items():
            print(f"{key}. {desc}")

        prompt = (
            input(f"\nHi {username.capitalize()}!, what would you like to do today👀? ")
            .strip()
            .capitalize()
        )

        if prompt in choices:
            return prompt

        print(f"Hmm... '{prompt}' isn't an option here, maybe try again? 🫪")


def proc_user_choice(choice: str):
    match choice:
        case "A":
            choice_a()
        case "B":
            choice_b()
        case "C":
            choice_c()
        case "D":
            choice_d()
        case "E":
            choice_e()
        case "F":
            quote()
        case _:
            print("Unhandled choice")


def get_next_id() -> int:
    """Reads urls.jsonl to find the highest existing ID and increments it."""
    try:
        with open("urls.jsonl", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
            if not lines:
                return 1
            last_entry = json.loads(lines[-1])
            return last_entry.get("id", 0) + 1
    except FileNotFoundError:
        return 1


def display_all_urls() -> list[dict]:
    """Reads all entries from urls.jsonl, prints them, and returns the list."""
    urls = []
    try:
        with open("urls.jsonl", "r") as file:
            for line in file:
                if line.strip():
                    urls.append(json.loads(line))
    except FileNotFoundError:
        print("\nNo URLs recorded yet! Try adding one first.")
        return []

    if not urls:
        print("\nNo URLs recorded yet!")
        return []

    print("\n--- Saved URLs ---")
    for entry in urls:
        note_display = f" | Note: {entry['note']}" if entry.get("note") else ""
        print(
            f"[{entry['id']}] {entry['shortened_url']} -> {entry['original_url']}{note_display}"
        )
    print("------------------")

    return urls


def write_all_urls(urls: list[dict]):
    """Overwrites urls.jsonl with the current list of URL dictionaries."""
    with open("urls.jsonl", "w") as file:
        file.writelines(json.dumps(entry) + "\n" for entry in urls)


# Menu Actions
def choice_a():
    """Option A: Add / Shorten a URL"""
    user_url = input("\nAlright then, URL please? ").strip()
    user_slug = input("What do you want to name your shortened url (slug)? ").strip()

    short_url = urlshortener(user_url, user_slug)
    print(f"\n✅ Shortened URL created: {short_url}")


def choice_b():
    """Option B: Delete a URL"""
    urls = display_all_urls()
    if not urls:
        return

    try:
        target_id = int(input("\nEnter the ID of the URL to delete: "))
    except ValueError:
        print("⚠️ Invalid ID. Please enter a number.")
        return

    updated_urls = [entry for entry in urls if entry["id"] != target_id]

    if len(updated_urls) == len(urls):
        print(f"⚠️ No URL found with ID {target_id}.")
        return

    write_all_urls(updated_urls)
    print(f"🗑️ Successfully deleted URL ID {target_id}!")


def choice_c():
    """Option C: Use a URL (Open in browser) cause apparently python can do that"""
    urls = display_all_urls()
    if not urls:
        return

    try:
        target_id = int(input("\nEnter the ID of the URL you want to open: "))
    except ValueError:
        print("⚠️ Invalid ID. Please enter a number.")
        return

    for entry in urls:
        if entry["id"] == target_id:
            target_url = entry["original_url"]
            print(f"🚀 Opening {target_url} in your browser...")
            webbrowser.open(target_url)
            return

    print(f"⚠️ No URL found with ID {target_id}.")


def choice_d():
    """Option D: Search for a URL"""
    urls = display_all_urls()
    if not urls:
        return

    query = input("\nEnter ID or keyword to search: ").strip().lower()

    results = []
    for entry in urls:
        if (
            query == str(entry["id"])
            or query in entry["shortened_url"].lower()
            or query in entry["original_url"].lower()
            or query in entry.get("note", "").lower()
        ):
            results.append(entry)

    if results:
        print(f"\n--- Search Results ({len(results)}) ---")
        for entry in results:
            note_display = f" | Note: {entry['note']}" if entry.get("note") else ""
            print(
                f"[{entry['id']}] {entry['shortened_url']} -> {entry['original_url']}{note_display}"
            )
    else:
        print("⚠️ No matching URLs found.")


def choice_e():
    """Option E: Add a note beside a URL"""
    urls = display_all_urls()
    if not urls:
        return

    try:
        target_id = int(input("\nEnter the ID of the URL you want to add a note to: "))
    except ValueError:
        print("⚠️ Invalid ID. Please enter a number.")
        return

    found = False
    for entry in urls:
        if entry["id"] == target_id:
            note_text = input(f"Enter note for [{entry['shortened_url']}]: ").strip()
            entry["note"] = note_text
            found = True
            break

    if not found:
        print(f"⚠️ No URL found with ID {target_id}.")
        return

    write_all_urls(urls)
    print(f"📝 Note added successfully to ID {target_id}!")


def quote():
    url = "https://api.api-ninjas.com/v2/randomquotes"
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if not data:
                print("⚠️ No quote returned from API.")
                return

            print("\n--- Quote of the Day ---")
            for item in data:
                quote_text = item.get("quote")
                author = item.get("author")
                work = item.get("work")
                categories = item.get("categories", [])

                print(f'"{quote_text}"')
                print(f"  — {author}" + (f" ({work})" if work else ""))
                if categories:
                    print(f"  Tags: {', '.join(categories)}")
                print("-" * 25)

        else:
            print(f"⚠️ API request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching quote: {e}")


# Core Logic
def urlshortener(url: str, custom_slug: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    scheme = parsed.scheme
    netloc = parsed.netloc

    new_url = f"{scheme}://{netloc}/{custom_slug}"
    next_id = get_next_id()

    data_entry = {
        "id": next_id,
        "shortened_url": new_url,
        "original_url": url,
        "note": "",
    }

    with open("urls.jsonl", "a") as file:
        file.write(json.dumps(data_entry) + "\n")

    return new_url


if __name__ == "__main__":
    main()
