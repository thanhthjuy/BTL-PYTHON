import sqlite3
import argparse
import csv
import re
from tabulate import tabulate

def lookup_players(db_path, name=None, club=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lấy tất cả cột trong bảng
    cursor.execute("PRAGMA table_info(players)")
    columns = [col[1] for col in cursor.fetchall()]

    # Tạo câu truy vấn
    query = "SELECT * FROM players"
    params = []
    conditions = []
    if name:
        conditions.append("player LIKE ?")
        params.append(f"%{name}%")
    if club:
        conditions.append("club LIKE ?")
        params.append(f"%{club}%")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    else:
        print("Please provide either --name or --club")
        return

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No players found.")
        return

    # In bảng ra màn hình
    print(tabulate(rows, headers=columns, tablefmt="grid"))

    # Tạo tên file CSV hợp lệ
    filename_base = name if name else club
    filename = re.sub(r'[\\/*?:"<>|]', "", filename_base.replace(" ", "_")) + ".csv"

    # Lưu CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Results saved to {filename}")

# ===== Main =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lookup player data from players.db")
    parser.add_argument("--name", help="Player name to search")
    parser.add_argument("--club", help="Club name to search")
    args = parser.parse_args()

    db_path = "players.db"
    lookup_players(db_path, name=args.name, club=args.club)

# python II.2.py --name "Mohamed Salah" --club "Liverpool"
# python II.2.py --name "Mohamed Salah" 
# python II.2.py --club "Liverpool"