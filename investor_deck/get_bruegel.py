"""Скачивает «Зимний пейзаж с конькобежцами и ловушкой для птиц» Брейгеля
с Wikimedia Commons в img/bruegel_winter.jpg (ширина до 2400 px).

Запуск: python get_bruegel.py            — выбрать лучший вариант автоматически
        python get_bruegel.py --list     — показать найденные файлы
        python get_bruegel.py --pick 3   — взять вариант номер 3 из списка
Только стандартная библиотека Python.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "neurocentre-investor-deck/1.0 (personal research presentation)"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "bruegel_winter.jpg")
QUERIES = [
    "Bruegel Winter Landscape with Skaters and a Bird Trap",
    "Bruegel Birdtrap 1565",
    "Bruegel Vogelfalle 1565",
]


def get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def score(title):
    t = title.lower()
    s = 0
    if "bruegel" in t or "brueghel" in t:
        s += 3
    if "bird trap" in t or "birdtrap" in t or "bird-trap" in t or "vogelfalle" in t:
        s += 4
    if "skater" in t:
        s += 2
    if "elder" in t:
        s += 2
    for bad in ("younger", "detail", "copy", "circle", "follower", "workshop", "after "):
        if bad in t:
            s -= 4
    if t.endswith((".jpg", ".jpeg", ".tif", ".tiff", ".png")):
        s += 1
    return s


def candidates():
    seen = {}
    for q in QUERIES:
        data = json.loads(get(API, {
            "action": "query", "list": "search", "srsearch": q,
            "srnamespace": 6, "srlimit": 20, "format": "json",
        }))
        for hit in data.get("query", {}).get("search", []):
            seen.setdefault(hit["title"], score(hit["title"]))
    return sorted(seen.items(), key=lambda kv: -kv[1])


def image_url(title):
    data = json.loads(get(API, {
        "action": "query", "titles": title, "prop": "imageinfo",
        "iiprop": "url|size|mime", "iiurlwidth": 2400, "format": "json",
    }))
    page = next(iter(data["query"]["pages"].values()))
    info = page["imageinfo"][0]
    return info.get("thumburl") or info["url"], info.get("width"), info.get("height")


def main():
    cands = candidates()
    if not cands:
        sys.exit("Commons ничего не нашёл. Сохраните картину вручную в " + OUT)
    if "--list" in sys.argv:
        for i, (t, s) in enumerate(cands[:15], 1):
            print(f"{i:2}. [{s:+d}] {t}")
        return
    idx = 0
    if "--pick" in sys.argv:
        idx = int(sys.argv[sys.argv.index("--pick") + 1]) - 1
    title = cands[idx][0]
    url, w, h = image_url(title)
    print("Файл:", title, f"({w}x{h})")
    data = get(url)
    if not (data[:2] == b"\xff\xd8" or data[:4] == b"\x89PNG"):
        sys.exit("Скачалось не изображение. Попробуйте: python get_bruegel.py --list")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print("Сохранено:", OUT, f"{len(data) // 1024} КБ")
    print("Если это не та картина: python get_bruegel.py --list, затем --pick N")


if __name__ == "__main__":
    main()
