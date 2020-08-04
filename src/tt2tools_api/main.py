#!/usr/bin/env python

import json
from os import scandir

from .skills import Skill, SkillTree


def load_skills(path):
    skills = []
    for file in scandir(path):
        if file.is_file and file.name.endswith(".json"):
            with open(file.path, "r") as f:
                skills.append(Skill(**json.load(f)))
    return skills


def load(filename):
    heroes = {}
    with open(filename, "r") as f:
        heroes_list = json.load(f)
    for hero in heroes_list:
        heroes[hero["slug"]] = hero
    return heroes


def main():
    hero = "the-great-pharaoh"
    hero_ascenscion = 3

    skills = load_skills("data/json/skills")
    heroes = load("data/json/heroes.json")
    skill_tree = SkillTree(skills)
    kv = skill_tree.get_skill("TapDmg")
    kv.level = 3

    gold_ratio = heroes[hero]["gold_ratio"][hero_ascenscion]

    print(skills)
    print(skill_tree)
    print(skill_tree.skills)
    print(kv)
    print(kv.efficiency("sc", gold_ratio))
    print(gold_ratio)


if __name__ == "__main__":
    main()
