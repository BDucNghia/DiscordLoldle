import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://wiki.leagueoflegends.com"
LIST_URL = f"{BASE_URL}/en-us/List_of_champions"

res = requests.get(LIST_URL)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

champions = []

table = soup.find("table", class_="article-table")
rows = table.find_all("tr")[1:]  # bỏ header

for row in rows:
    name_cell = row.find("td")
    if not name_cell:
        continue

    link_tag = name_cell.find("a", href=True)
    if not link_tag:
        continue

    link = urljoin(BASE_URL, link_tag["href"])

    champions.append({
        "url": link
    })

with open("champion_links.json", "w", encoding="utf-8") as f:
    import json
    json.dump(champions, f, ensure_ascii=False, indent=4)



