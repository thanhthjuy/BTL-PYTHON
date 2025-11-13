import sqlite3
import pandas as pd

conn = sqlite3.connect("players.db")
df = pd.read_sql_query("SELECT * FROM players", conn)
conn.close()

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

stats_list = []
grouped = df.groupby('club')

for club, group in grouped:
    stats_dict = {'club': club}
    for col in numeric_cols:
        stats_dict[f'{col}_mean'] = group[col].mean()
        stats_dict[f'{col}_median'] = group[col].median()
        stats_dict[f'{col}_std'] = group[col].std()
    stats_list.append(stats_dict)

stats_df = pd.DataFrame(stats_list)

stats_df.to_csv("team_stats.csv", index=False)
print("Đã lưu thống kê trung bình, trung vị, độ lệch chuẩn vào 'team_stats.csv'")

best_teams = {}

for col in numeric_cols:
    best_club = stats_df.loc[stats_df[f'{col}_mean'].idxmax(), 'club']
    best_teams[col] = best_club

print("\nĐội có phong độ tốt nhất theo từng chỉ số (trung bình):")
for col, club in best_teams.items():
    print(f"{col}: {club}")
