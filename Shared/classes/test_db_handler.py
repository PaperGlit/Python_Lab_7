import unittest
import os
from DAL.classes.database_handler import DBHandler


class TestDBHandler(unittest.TestCase):
    def setUp(self):
        """Set up an in-memory database for testing."""
        self.db_handler = DBHandler(":memory:")

    def test_create_table(self):
        """Test that the history table is created successfully."""
        self.db_handler.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
        table = self.db_handler.cursor.fetchone()
        self.assertIsNotNone(table)

    def test_insert_history(self):
        """Test inserting a history record."""
        self.db_handler.insert_history("posts", "GET", "all")
        history = self.db_handler.fetch_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "posts")  # Check link
        self.assertEqual(history[0][2], "GET")    # Check request type
        self.assertEqual(history[0][3], "all")    # Check entity ID

    def test_fetch_history(self):
        """Test fetching history records."""
        self.db_handler.insert_history("posts", "GET", "all")
        self.db_handler.insert_history("users", "POST", "1")
        history = self.db_handler.fetch_history()
        self.assertEqual(len(history), 2)

    def test_export_to_txt(self):
        """Test exporting history to a .txt file."""
        self.db_handler.insert_history("posts", "GET", "all")
        self.db_handler.export_to_txt("test_history.txt")

        with open("test_history.txt", "r") as file:
            content = file.read()
            self.assertIn("GET", content)
            self.assertIn("posts", content)

        os.remove("test_history.txt")

    def test_export_to_csv(self):
        """Test exporting history to a .csv file."""
        self.db_handler.insert_history("posts", "GET", "all")
        self.db_handler.export_to_csv("test_history.csv")

        with open("test_history.csv", "r") as file:
            content = file.read()
            self.assertIn("GET", content)
            self.assertIn("posts", content)

        os.remove("test_history.csv")

    def test_export_to_json(self):
        """Test exporting history to a .json file."""
        self.db_handler.insert_history("posts", "GET", "all")
        self.db_handler.export_to_json("test_history.json")

        with open("test_history.json", "r") as file:
            content = file.read()
            self.assertIn('"type": "GET"', content)
            self.assertIn('"link": "posts"', content)

        os.remove("test_history.json")

    def tearDown(self):
        """Clean up by closing the database connection."""
        self.db_handler.close()