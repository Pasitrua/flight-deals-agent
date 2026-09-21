from dataclasses import dataclass

ORIGIN = "MOW"
DESTINATIONS = [
    # Азия
    "BKK", "HKT", "KUL", "SIN", "DPS", "DEL", "BOM", "CMB", "HKG",
    # Ближний Восток
    "DXB", "AUH", "DOH", "MCT", "AMM", "TLV", "IST",
]

MAX_PRICE_EUR = 1000
CURRENCY = "EUR"
MAX_STOPS = 1
MIN_SEATS = 3
TRAVEL_CLASS = "ECONOMY"
DATE_SCAN_DAYS = 180
DATE_STEP_DAYS = 7
TOP_RESULTS = 10
