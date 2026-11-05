import os
from dotenv import load_dotenv

import re
import certifi
import airportsdata
import pycountry

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "JFK")

BASE_URL = "https://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load("IATA")

COUNTRY_ALIASES = {
    "USA": "United States",
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates",
    "KSA": "Saudi Arabia",
    "PRC": "China",
    "ROC": "Taiwan",
    "RUS": "Russia",
    "KOR": "South Korea",
    "NLD": "Netherlands",
    "NZL": "New Zealand",
    "SGP": "Singapore",
    "HKG": "Hong Kong"
}



