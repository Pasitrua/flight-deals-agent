import os

MAX_PRICE_RUB = 20_000
MIN_SEATS = 3
MAX_STOPS = 1
MIN_TRIP_DAYS = 3
MAX_TRIP_DAYS = 5
ORIGIN = "MOW"
CURRENCY = "rub"

DESTINATIONS = {
    "TAS":"Ташкент","DYU":"Душанбе","EVN":"Ереван","BAK":"Баку",
    "TBS":"Тбилиси","ALA":"Алматы","NQZ":"Астана","FRU":"Бишкек",
    "DXB":"Дубай","AUH":"Абу-Даби","DOH":"Доха","MCT":"Маскат",
    "IST":"Стамбул","IKA":"Тегеран","DEL":"Дели","BOM":"Мумбаи",
    "GOI":"Гоа","BKK":"Бангкок","HKT":"Пхукет","KUL":"Куала-Лумпур",
    "SGN":"Хошимин","HAN":"Ханой","PEK":"Пекин","PVG":"Шанхай",
    "HKG":"Гонконг","TYO":"Токио","SEL":"Сеул","DPS":"Бали",
    "CMB":"Коломбо","MLE":"Мале","KTM":"Катманду","MNL":"Манила",
    "JED":"Джидда","RUH":"Эр-Рияд","AMM":"Амман","TLV":"Тель-Авив",
    "CAI":"Каир"
}

AVIASALES_API_TOKEN = os.environ["AVIASALES_API_TOKEN"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
