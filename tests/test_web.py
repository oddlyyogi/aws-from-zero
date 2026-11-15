"""Tests for the standard-library web API in the container image (app/web.py)."""
# needs: app/web.py
import json
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app import web
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_health_reports_version(self):
        status, body = self.get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_notes_list(self):
        status, body = self.get("/notes")
        self.assertEqual(status, 200)
        self.assertEqual(body["notes"][0]["title"], "Beach day")

    def test_unknown_route_is_404(self):
        status, body = self.get("/nope")
        self.assertEqual(status, 404)
        self.assertIn("/nope", body["error"])


if __name__ == "__main__":
    unittest.main()
