import datetime as dt
import urllib.parse
from aviasales import fetch_all
from config import MAX_PRICE_RUB, MAX_STOPS, MIN_SEATS, MIN_TRIP_DAYS, MAX_TRIP_DAYS
from telegram import send_message

def days(row):
    try:
        a=dt.date.fromisoformat(row["depart_date"])
        b=dt.date.fromisoformat(row["return_date"])
        return (b-a).days
    except Exception: return None

def url(row):
    if row.get("link"):
        return row["link"] if row["link"].startswith("http") else "https://www.aviasales.ru"+row["link"]
    q=urllib.parse.urlencode({
        "origin":"MOW","destination":row.get("_destination_iata",""),
        "depart_date":row.get("depart_date",""),"return_date":row.get("return_date","")
    })
    return "https://www.aviasales.ru/search?"+q

def filter_rows(rows):
    out=[]
    for r in rows:
        d=days(r)
        seats=r.get("available_seats")
        try: seats=int(seats) if seats is not None else None
        except: seats=None
        if d is None or not MIN_TRIP_DAYS<=d<=MAX_TRIP_DAYS: continue
        if r.get("value") is None or float(r["value"])>MAX_PRICE_RUB: continue
        if r.get("number_of_changes") is None or int(r["number_of_changes"])>MAX_STOPS: continue
        if int(r.get("trip_class",0))!=0: continue
        if seats is None or seats<MIN_SEATS: continue
        r["_days"]=d; r["_seats"]=seats; out.append(r)
    return sorted(out,key=lambda x:float(x["value"]))

def rub(v): return f"{v:,.0f}".replace(","," ")+" ₽"

def main():
    checked=dt.datetime.now().astimezone().strftime("%d.%m.%Y %H:%M %Z")
    rows=fetch_all()
    offers=filter_rows(rows)
    header=(
        "✈️ МОСКВА → АЗИЯ / БЛИЖНИЙ ВОСТОК\n\n"
        "≤20 000 ₽ round trip • 3–5 дней • эконом • ≤1 пересадка • 3+ мест\n"
        f"Проверено: {checked}\n\n"
    )
    if not offers:
        text=header+"Подтверждённых вариантов по всем условиям сегодня не найдено.\n\n"
        text+="⚠️ Aviasales Data API использует кэшированные данные, а не гарантированный live-search."
    else:
        parts=[]
        for i,r in enumerate(offers[:10],1):
            parts.append(
                f"{i}. Москва → {r.get('_destination_name',r.get('destination','?'))}\n"
                f"📅 {r.get('depart_date')} → {r.get('return_date')} ({r['_days']} дн.)\n"
                f"💰 {rub(float(r['value']))}\n"
                f"✈️ {r.get('airline','не указано')}\n"
                f"🔄 Пересадки: {r.get('number_of_changes')}\n"
                f"🎟 Мест: {r['_seats']}+\n"
                f"🧳 Багаж: не указан API\n"
                f"🗃 Найдено API: {r.get('found_at','не указано')}\n"
                f"⚠️ Цена из кэша Aviasales, не live-подтверждение.\n"
                f"🔗 {url(r)}"
            )
        text=header+"\n\n".join(parts)
    send_message(text)

if __name__=="__main__":
    main()
