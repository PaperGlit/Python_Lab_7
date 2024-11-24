import csv
import json
import sqlite3


class History:
    def __init__(self, db_name="prompt_history.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('GET', 'POST', 'PATCH', 'DELETE')),
            entity_id TEXT NOT NULL
        )
        """)
        self.connection.commit()

    def insert_history(self, link, request_type, entity_id):
        self.cursor.execute("""
        INSERT INTO history (link, type, entity_id) 
        VALUES (?, ?, ?)
        """, (link, request_type, entity_id))
        self.connection.commit()

    def fetch_history(self):
        self.cursor.execute("SELECT * FROM history")
        return self.cursor.fetchall()

    def export_to_txt(self, filename="history.txt"):
        history = self.fetch_history()
        with open(filename, "w") as file:
            file.write(f"{'ID':<5} {'Link':<20} {'Type':<10} {'Entity ID':<10}\n")
            file.write("=" * 50 + "\n")
            for row in history:
                file.write(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10}\n")

    def export_to_csv(self, filename="history.csv"):
        history = self.fetch_history()
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Link", "Type", "Entity ID"])
            writer.writerows(history)

    def export_to_json(self, filename="history.json"):
        history = self.fetch_history()
        data = [{"id": row[0], "link": row[1], "type": row[2], "entity_id": row[3]} for row in history]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def close(self):
        self.connection.close()