"""Tests for the photo info worker's PNG header reader (worker/photo_info.py): no AWS access needed."""
# needs: worker/photo_info.py
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-2")


class PngSizeTests(unittest.TestCase):
    def setUp(self):
        from worker.photo_info import png_size
        self.png_size = png_size

    def test_reads_width_and_height_of_a_sample(self):
        head = (ROOT / "samples" / "photos" / "beach.png").read_bytes()[:24]
        width, height = self.png_size(head)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

    def test_refuses_a_file_that_is_not_a_png(self):
        with self.assertRaises(ValueError):
            self.png_size(b"not an image\n" + b"\0" * 11)


if __name__ == "__main__":
    unittest.main()
