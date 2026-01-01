import requests
from bs4 import BeautifulSoup
import re
import json

with open("champion_links.json", "r") as f:
    champs_links = json.load(f)

def clean_text(text):
    return " ".join(text.split())

def extract_year(text):
    m = re.search(r"\d{4}", text)
    return m.group(0) if m else None

def remove_parentheses(text):
    return re.sub(r"\s*\(.*?\)", "", text).strip()

def get_champion_info(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    data = {
        "name": None,
        "roles": [],
        "release_year": None,
        "legacy_class": [],
        "resource": None,
        "range_type": None,
        "adaptive_type": None
    }

    name_tag = soup.find("div", class_="infobox-section")
    if name_tag:
        table = name_tag.find("table")
        name = clean_text(table.find("td").text)
        data["name"] = name

    role_label = soup.find("span", string="Role(s):")
    if role_label:
        role_block = role_label.parent
        roles = [
            clean_text(a.text)
            for a in role_block.find_all("a")
            if clean_text(a.text)
        ]
        data["roles"] = roles

    rows = soup.select("div.infobox-data-row.championbox")

    for row in rows:
        label = clean_text(row.select_one(".infobox-data-label").text)
        value_node = row.select_one(".infobox-data-value")

        if not value_node:
            continue

        value_text = clean_text(value_node.text)

        if label == "Release date":
            data["release_year"] = extract_year(value_text)

        elif label == "Legacy class":
            classes = [
                clean_text(a.text)
                for a in value_node.find_all("a")
                if clean_text(a.text)
            ]
            data["legacy_class"] = classes

        elif label == "Resource":
            data["resource"] = remove_parentheses(value_text)

        elif label == "Range type":
            data["range_type"] = value_text

        elif label == "Adaptive type":
            data["adaptive_type"] = value_text

    return data


print(get_champion_info(champs_links[1]["url"]))

champions_data = []
for champ in champs_links:
    info = get_champion_info(champ["url"])
    champions_data.append(info)

with open("champions.json", "w", encoding="utf-8") as f:
    json.dump(champions_data, f, ensure_ascii=False, indent=4)