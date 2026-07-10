import requests

BASE_URL = "http://128.140.85.215:8888"
HEADERS = {}

def set_connection(url, api_key):
    global BASE_URL, HEADERS
    BASE_URL = url.rstrip("/")
    HEADERS = {"x-api-key": api_key}

def get_teile():
    return requests.get(f"{BASE_URL}/teile").json()

def get_produkte():
    return requests.get(f"{BASE_URL}/produkte").json()

def get_bestellwarnungen():
    return requests.get(f"{BASE_URL}/bestellwarnungen").json()

def get_stueckliste(produkt_id):
    return requests.get(f"{BASE_URL}/stueckliste/{produkt_id}").json()

def wareneingang(teil_id, menge):
    return requests.post(f"{BASE_URL}/wareneingang", json={"teil_id": teil_id, "menge": menge}, headers=HEADERS)

def produktion(produkt_id, menge):
    return requests.post(f"{BASE_URL}/produktion", json={"produkt_id": produkt_id, "menge": menge}, headers=HEADERS)

def lagerausgang(produkt_id, menge):
    return requests.post(f"{BASE_URL}/lagerausgang", json={"produkt_id": produkt_id, "menge": menge}, headers=HEADERS)

def set_bestand(teil_id, bestand):
    return requests.put(f"{BASE_URL}/teile/{teil_id}", json={"bestand": bestand}, headers=HEADERS)
