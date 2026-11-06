import sqlite3

con = sqlite3.connect("university.sqlite.db")

cursor = con.cursor()

rows = cursor.execute("SELECT * FROM groups").fetchall()

print(rows)
for row in rows:
    print(row)