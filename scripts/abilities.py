import json

from slugify import slugify
from util import load_tsv


abilities = [
    {"id": "HS", "name": "Heavenly Strike"},
    {"id": "DS", "name": "Deadly Strike"},
    {"id": "HoM", "name": "Hand of Midas"},
    {"id": "FS", "name": "Fire Sword"},
    {"id": "WC", "name": "War Cry"},
    {"id": "SC", "name": "Shadow Clone"},
]


def transform_abilities(abilities_data):
    attempts = []
    atkspd = []

    for row in abilities_data:
        attempts.append(row["Special attempts"])
        atkspd.append(row["Attack speed"])
    return attempts, atkspd


def load_ability_data(tsv_filename, output_dir):
    attempts, atkspd = transform_abilities(load_tsv(tsv_filename))

    for idx, ability in enumerate(abilities):
        ability["index"] = idx
        ability["slug"] = slugify(ability["name"])
        if ability["id"] == "SC":
            ability["attempts"] = attempts
        elif ability["id"] == "WC":
            ability["atkspd"] = atkspd
        with open("{}/{}.json".format(output_dir, ability["slug"]), "w") as f:
            json.dump(ability, f, indent=2, sort_keys=True)
