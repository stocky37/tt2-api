#!/usr/bin/env python

from util import load_data
from skills import transform_skills
from heroes import transform_heroes
from abilities import load_ability_data
from reductions import transform_reductions_dmg, transform_reductions_gold

if __name__ == "__main__":
    load_data("data/raw/skills.tsv", "data/json/skills", transform_skills)
    load_data("data/raw/heroes.tsv", "data/json/heroes", transform_heroes)
    load_data(
        "data/raw/reductions-dmg.tsv",
        "data/json/reductions/dmg",
        transform_reductions_dmg,
    )
    load_data(
        "data/raw/reductions-gold.tsv",
        "data/json/reductions/gold",
        transform_reductions_gold,
    )
    load_ability_data("data/raw/abilities.tsv", "data/json/abilities")
