from slugify import slugify


def transform_heroes(heroes_data):
    return [
        {
            "index": idx,
            "name": hero_data["Name"],
            "slug": slugify(hero_data["Name"]),
            "gold_ratio": [
                float(hero_data["No ascension"]),
                float(hero_data["Ascension 1"]),
                float(hero_data["Ascension 2"]),
                float(hero_data["Ascension 3"]),
            ],
        }
        for idx, hero_data in enumerate(heroes_data)
    ]
