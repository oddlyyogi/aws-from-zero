"""Tests for the one-server Flask app (app/app.py): no AWS access needed."""
# needs: app/app.py
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class AppTests(unittest.TestCase):
    def setUp(self):
        from app import app as module
        self.module = module
        self.tmp = tempfile.TemporaryDirectory()
        module.DB = Path(self.tmp.name) / "notes.db"
        self.client = module.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_health_starts_empty(self):
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok", "notes": 0})

    def test_add_note_redirects_and_escapes(self):
        r = self.client.post("/notes", data={"title": "Market", "body": "<script>x</script>"})
        self.assertEqual(r.status_code, 303)
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>", page)


if __name__ == "__main__":
    unittest.main()
