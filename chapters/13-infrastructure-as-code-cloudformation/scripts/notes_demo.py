"""Exercise app/notes_store.py against the real table."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.notes_store import add_note, add_photo, list_notes


first = add_note("ana", "Beach day", "Low tide at six.", tags=["sea", "summer"])
time.sleep(1)
add_note("ana", "Harbour walk", "Boats at dawn.", tags=["sea"])
time.sleep(1)
add_note("ana", "Market", "Peaches!", tags=["food"])
add_photo("ana", first)
add_photo("ana", first)
for title, photos in list_notes("ana"):
    print(f"{title:<14} {photos} photos")
