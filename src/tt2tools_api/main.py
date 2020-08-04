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


def main():
    skills = load_skills("data/json/skills")
    skill_tree = SkillTree(skills)
    kv = skill_tree.get_skill("TapDmg")
    kv.level = 3

    print(skills)
    print(skill_tree)
    print(skill_tree.skills)
    print(kv)
    print(kv.efficiency("sc"))


if __name__ == "__main__":
    main()
