import json
from pathlib import Path

_DATA_FILE = Path(__file__).parent / "aliases.json"

with open(_DATA_FILE, encoding="utf-8") as f:
    _data = json.load(f)

COUNTRY_ALIASES: dict[str, str] = _data["country_aliases"]
COUNTRY_MAIN_AIRPORT: dict[str, str] = _data["country_main_airport"]
CITY_MAIN_AIRPORT: dict[str, str] = _data["city_main_airport"]