import datetime as dt
import requests
from config import AVIASALES_API_TOKEN, CURRENCY, DESTINATIONS, ORIGIN

URL = "https://api.travelpayouts.com/aviasales/v3/get_latest_prices"

def months_ahead(n=4):
    today = dt.date.today()
    out=[]
    for i in range(n+1):
        m=today.month+i
        y=today.year+(m-1)//12
        m=(m-1)%12+1
        out.append(f"{y:04d}-{m:02d}")
    return out

def fetch(destination, month):
    params={
        "currency":CURRENCY, "origin":ORIGIN, "destination":destination,
        "beginning_of_period":month, "period_type":"month", "page":1,
        "show_to_affiliates":"true", "sorting":"price", "trip_class":0,
        "token":AVIASALES_API_TOKEN
    }
    r=requests.get(URL, params=params, timeout=45)
    r.raise_for_status()
    data=r.json()
    if not data.get("success"): return []
    rows=data.get("data") or []
    for x in rows:
        x["_destination_name"]=DESTINATIONS.get(destination,destination)
        x["_destination_iata"]=destination
    return rows if isinstance(rows,list) else []

def fetch_all():
    out=[]
    for month in months_ahead():
        for dest in DESTINATIONS:
            try: out.extend(fetch(dest,month))
            except requests.RequestException as e:
                print(f"API error {dest}/{month}: {e}")
    return out
