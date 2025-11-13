import argparse
import requests
import csv
import re
from tabulate import tabulate

def lookup_players(name=None, club=None):
    if name:
        base_url = "http://127.0.0.1:5000/api/player"
        params = {"name": name}
    elif club:
        base_url = "http://127.0.0.1:5000/api/club"
        params = {"club": club}
    else:
        print("Please provide either --name or --club")
        return

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error connecting to Flask server:", e)
        return

    data = response.json()

    if not data or (isinstance(data, dict) and "message" in data):
        print("No players found.")
        return

    headers = data[0].keys()
    rows = [player.values() for player in data]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

    filename_base = name if name else club
    filename = re.sub(r'[\\/*?:"<>|]', "", filename_base.replace(" ", "_")) + ".csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Results saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lookup player data via Flask API")
    parser.add_argument("--name", help="Player name to search")
    parser.add_argument("--club", help="Club name to search")
    args = parser.parse_args()

    lookup_players(name=args.name, club=args.club)

