import requests
import os
from dotenv import load_dotenv
import sys

load_dotenv()

api_key = os.getenv("API_NINJA")
if api_key == None:
    print("Failed to find .env file")
    sys.exit(1)

try:
    query_bin = int(input("What bin are you looking for? "))
except ValueError:
    print("That's not a valid B.I.N")
    sys.exit(1)

url = f"https://api.api-ninjas.com/v2/bin?bin={query_bin}"
headers = {"x-Api-key": api_key}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    if data:
        # access any dict key directly from the first element
        bin = data[0].get('bin', 'Unknown')
        country = data[0].get('country', 'Unknown')
        country_code = data[0].get('country_iso2', 'N/A')


        print(f"Country: {country} ({country_code})\nB.I.N: {bin}")

    else:
        print("No B.I.N data found")

else:
    print(f"Error {response.status_code}: {response.text}")