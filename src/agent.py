import json
import os
from datetime import date, timedelta, datetime, timezone
from pathlib import Path

from config import (
    ORIGIN, DESTINATIONS, MAX_PRICE_EUR, MAX_STOPS, MIN_SEATS,
    DATE_SCAN_DAYS, DATE_STEP_DAYS, TOP_RESULTS
)
from amadeus_client import AmadeusClient

DATA_FILE = Path("data/prices.json")

def load_history():
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_history(history):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def stops_for(offer):
    itineraries = offer.get("itineraries", [])
    return max((len(i.get("segments", [])) - 1 for i in itineraries), default=99)

def seats_for(offer):
    # Amadeus may expose numberOfBookableSeats. If absent, do not claim availability.
    values = [offer.get("numberOfBookableSeats")]
    values += [f.get("numberOfBookableSeats") for f in offer.get("travelerPricings", [])]
    values = [v for v in values if isinstance(v, int)]
    return min(values) if values else None

def normalize(offer, destination):
    price = float(offer["price"]["grandTotal"])
    stops = stops_for(offer)
    seats = seats_for(offer)
    return {
        "id": offer.get("id"),
        "destination": destination,
        "price_eur": price,
        "stops": stops,
        "seats": seats,
        "last_ticketing_date": offer.get("lastTicketingDate"),
        "raw": offer,
    }

def find_deals():
    client = AmadeusClient()
    today = date.today()
    history = load_history()
    deals = []

    for offset in range(7, DATE_SCAN_DAYS + 1, DATE_STEP_DAYS):
        departure = today + timedelta(days=offset)
        return_date = departure + timedelta(days=7)
        for destination in DESTINATIONS:
            try:
                offers = client.search(ORIGIN, destination, departure, return_date)
            except Exception as exc:
                print(f"Search failed for {destination} {departure}: {exc}")
                continue

            for offer in offers:
                item = normalize(offer, destination)
                if item["price_eur"] > MAX_PRICE_EUR or item["stops"] > MAX_STOPS:
                    continue
                # Если API не сообщает число мест, не выдаём это за подтверждённые 3 места.
                if item["seats"] is not None and item["seats"] < MIN_SEATS:
                    continue
                key = f'{destination}:{departure}:{return_date}'
                previous = history.get(key, {}).get("price_eur")
                item["departure"] = departure.isoformat()
                item["return"] = return_date.isoformat()
                item["price_drop"] = round(previous - item["price_eur"], 2) if previous is not None and item["price_eur"] < previous else None
                deals.append(item)
                history[key] = {
                    "price_eur": item["price_eur"],
                    "checked_at": datetime.now(timezone.utc).isoformat(),
                }

    deals.sort(key=lambda x: (x["price_drop"] is None, -(x["price_drop"] or 0), x["price_eur"]))
    save_history(history)
    return deals[:TOP_RESULTS]

def format_report(deals):
    checked = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not deals:
        return f"✈️ Ежедневный отчёт\nПроверено: {checked}\nПодходящих предложений не найдено."

    lines = [
        "✈️ <b>Ежедневный поиск авиабилетов</b>",
        f"Проверено: {checked}",
        "Маршрут: Москва → Азия / Ближний Восток",
        "Условия: до €1000, эконом, максимум 1 пересадка",
        "",
    ]
    for i, d in enumerate(deals, 1):
        seats = str(d["seats"]) if d["seats"] is not None else "не указано API"
        drop = f" | 🔻 −€{d['price_drop']:.0f}" if d["price_drop"] else ""
        lines.append(
            f"{i}. <b>{d['destination']}</b> | {d['departure']} → {d['return']}\n"
            f"€{d['price_eur']:.0f} | пересадок: {d['stops']} | мест: {seats}{drop}"
        )
    return "\n".join(lines)

if __name__ == "__main__":
    report = format_report(find_deals())
    Path("report.txt").write_text(report, encoding="utf-8")
    print(report)
