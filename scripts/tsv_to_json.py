#!/usr/bin/env python

from util import load_data
from skills import transform_skills
from heroes import transform_heroes
from abilities import load_ability_data

if __name__ == "__main__":
    load_data("data/raw/skills.tsv", "data/json/skills", transform_skills)
    load_data("data/raw/heroes.tsv", "data/json/heroes", transform_heroes)
    load_ability_data("data/raw/abilities.tsv", "data/json/abilities")
