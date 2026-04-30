import json
import os
import re
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

full_json_path = resource_path("data/cards.json")
dummy_path = resource_path("assets/dummy_img.png")
card_img_path = resource_path("assets/cards")



def load_cards(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)["cards"]

def load_card_img(img_path):
    card_img = []
    for file in os.listdir(img_path):
        if file.endswith(".png"):
            full_path = os.path.join(img_path, file)
            card_img.append(full_path)

    def sort_key(file_path):
        file_name = os.path.basename(file_path)
        match = re.search(r'card_(\d+)\.png', file_name)
        if match:
            return int(match.group(1))
        return float("inf")

    card_img.sort(key=sort_key)
    return card_img

card_images = load_card_img(card_img_path)
cards = load_cards(full_json_path)