from typing import List, Dict

from slugify import slugify


def transform_reductions_gold(data: List[Dict]):
    return transform_reductions(data, "gold")


def transform_reductions_dmg(data: List[Dict]):
    return transform_reductions(data, "dmg")


def transform_reductions(data: List[Dict], type):
    reductions = []
    for row in data:
        reduction = {k.lower(): v for k, v in row.items()}
        reduction["type"] = type
        reduction["slug"] = slugify(reduction["affects"])
        reductions.append(reduction)
    return reductions
