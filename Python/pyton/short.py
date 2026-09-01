import getpass
import json
import random
from urllib.parse import urlparse


def urlshortener(url: str) -> str:
    # create an empty list and append the words for the url shortneder
    words = [
        "gemini",
        "raven",
        "starfire",
        "beastboy",
        "neutron",
        "alice",
        "bob",
        "captain",
        "gugb",
        "astra"
    ]

    random_word = random.choice(words)

    # check if the user added a https://...
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # scheme -> http/https
    scheme = parsed.scheme

    # netloc -> www.example.com
    netloc = parsed.netloc

    slash = random_word # the shortend path

    # join scheme, netlock and short_path all together
    new_url = f"{scheme}://{netloc}/{slash}"

    url_data = {"shortend_url": new_url}

    org_url = {"original_url": url}

    # ouput should look smthing like.. {new_url: "..", "original_url": "..."}
    combo_url = [url_data | org_url] # merging the two lists


    # save/create the file if it doesn't exist then append to the file
    # jsonl lets other devs and IDE know that the file contains multiple json rows rather than one single json object
    with open("urls.jsonl", "a") as file:
        # json.dumps() converts the dict to a string then appends a new line to it
        pretty_json = json.dumps(combo_url, indent=4)

        # write the block and extra spacig at the end to separate entries
        _ = file.write(pretty_json + "\n\n")

    return new_url



def main():
    try:
        user_url = input("URL please? ").strip() # strip strips out any whitespace

        # Call your shortener here
        short_url = urlshortener(user_url)
        print(f"Shortened URL: {short_url}")

    except KeyboardInterrupt:
        username = getpass.getuser()
        print(f"\nAddios {username}")


if __name__ == "__main__":
    main()
