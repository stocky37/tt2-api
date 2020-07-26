#!/usr/bin/env python

import json
from os import scandir

from .skills import LevelledSkill, Skill


def load_skills(path):
    nodes = {}
    for file in scandir(path):
        if file.is_file and file.name.endswith(".json"):
            with open(file.path, "r") as f:
                skill = json.load(f)
                nodes[skill["id"]] = Skill(**skill)
    for node in nodes.values():
        if hasattr(node, "parent_id"):
            node.parent = nodes[node.parent_id]

    return list(nodes.values())


def main():
    nodes = load_skills("data/skills")
    for node in nodes:
        if node.slug == "cloaking":
            cloaking = node
            break

    print(nodes)
    levelled_skill = LevelledSkill(cloaking, 0)
    print(levelled_skill)
    print(levelled_skill.sp_used)
    print(levelled_skill.next.sp_used)
    print(levelled_skill.prev.sp_used)


if __name__ == "__main__":
    main()
