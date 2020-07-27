#!/usr/bin/env python

from util import load_data
from skills import transform_skills

if __name__ == "__main__":
    load_data("data/raw/skills.tsv", "data/json/skills", transform_skills)
