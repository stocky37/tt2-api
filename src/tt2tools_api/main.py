#!/usr/bin/env python

import json
from os import scandir

from tt2tools_api.build_stats import BuildStats
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


def show_skill(skill_tree: SkillTree, skill_id: str, level: int, build: BuildStats):
    skill = skill_tree.get_skill(skill_id)
    skill.level = level
    print("{} -> {}".format(skill, skill.efficiency(build)))


def main():
    heroes = load("data/json/heroes.json")
    build = BuildStats(heroes, "sc", "phom", "maya-muerta-the-watcher", 3)
    skill_tree = SkillTree(load_skills("data/json/skills"))

    show_skill(skill_tree, "TapDmg", 3, build)
    show_skill(skill_tree, "PetGoldQTE", 16, build)
    show_skill(skill_tree, "TapDmgFromHelpers", 14, build)


if __name__ == "__main__":
    main()
