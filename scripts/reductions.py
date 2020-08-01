import re
from collections import defaultdict
from typing import List, Dict

from slugify import slugify
from util import load_tsv, to_dict

brackets_regex = re.compile("\\([^)]*\\)")


def normalise(key):
    return slugify(brackets_regex.sub("", key) if brackets_regex.search(key) else key)


def load_reductions(filename: str) -> Dict:
    return to_dict(transform_reductions(load_tsv(filename)), "slug")


def transform_reductions(data: List[Dict]) -> List[Dict]:
    all_reductions = []
    for row in data:
        all_reductions.append(
            {
                "name": row["Name"].replace("*", ""),
                "slug": normalise(row["Name"]),
                "reductions": {
                    normalise(k): float(v) for k, v in row.items() if k != "Name"
                },
            }
        )
    return all_reductions


def get_reductions(reductions, key) -> Dict:
    return reductions[key]["reductions"]


def ti_dmg_reductions(r: Dict):
    reductions = {}
    for key, value in get_reductions(r, "hero").items():
        reductions[key] = 49 * value

    for key, value in get_reductions(r, "tap").items():
        reductions[key] += 28 * value

    for key, value in get_reductions(r, "sc").items():
        reductions[key] += 4 * value

    for key, value in get_reductions(r, "all").items():
        reductions[key] += 37 * value

    for key, value in get_reductions(r, "crit-dmg").items():
        reductions[key] += 22 * value

    return reductions


def ti_gold_reductions(r: Dict):
    reductions = {}
    for key, value in get_reductions(r, "all").items():
        reductions[key] = 31 * value

    for key, value in get_reductions(r, "boss").items():
        reductions[key] += 25 * value

    for key, value in get_reductions(r, "chesterson").items():
        reductions[key] += 34 * value

    for key, value in get_reductions(r, "fairy").items():
        reductions[key] += 18 * value

    return reductions


def sum_reductions(r: Dict, keys):
    reductions = defaultdict(int)
    for k in keys:
        for key, value in get_reductions(r, k).items():
            reductions[key] += value
    return reductions
