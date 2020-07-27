#!/usr/bin/env python

from typing import List, Dict

from slugify import slugify

from scripts.util import num


def calculate_tree_column(_slot):
    slot = num(_slot)
    if slot == 0:
        return 1
    mod = slot % 3
    if mod == 0:
        return 2
    if mod == 1:
        return 0
    if mod == 2:
        return 1


data_map = {
    "TalentID": {"key": "id", "val": lambda val: val},
    "Name": {"key": "name", "val": lambda val: val},
    "Class": {"key": "skill_tree", "val": lambda val: val},
    "S0": {"key": "unlock_stage", "val": lambda val: num(val)},
    "MaxLevel": {"key": "max_level", "val": lambda val: num(val)},
    "Note": {"key": "note", "val": lambda val: val},
    "Slot": {"key": "column", "val": calculate_tree_column},
    "TierNum": {"key": "tier", "val": lambda val: int(val)},
}


def get_skill_levels(skill: Dict):
    # the optional extra +1 is for tier 4 skills - specifically, the mythic sets that increase their level by 1
    num_levels = int(skill["MaxLevel"]) + (1 if skill["TierNum"] == "4" else 0)

    sp_required = []
    primary_bonus = []
    secondary_bonus = []

    # skill_levels = []

    level: int
    # the extra +1 is for the unlocked level (level 0)
    for level in range(0, num_levels + 1):
        sp_required.append(0 if level == 0 else int(skill["C{}".format(level - 1)]))
        primary_bonus.append(float(skill["A{}".format(level)]))
        secondary_bonus.append(float(skill["B{}".format(level)]))

    return sp_required, primary_bonus, secondary_bonus


def transform_skills(all_skills_data: List[Dict]):
    skills = []
    for skill_data in all_skills_data:
        skill = {}

        # convert column names & values based on the global mapping dict
        for key in skill_data.keys():
            if key in data_map:
                _map = data_map[key]
                skill[_map["key"]] = _map["val"](skill_data[key])

        skill["slug"] = slugify(skill_data["Name"])
        if skill_data["TalentReq"] != "None":
            skill["parent_id"] = skill_data["TalentReq"]

        sp, primary, secondary = get_skill_levels(skill_data)
        skill["sp_required"] = sp
        skill["bonuses"] = [{"type": skill_data["BonusTypeA"], "value": primary}]

        if skill_data["BonusTypeB"] != "None":
            skill["bonuses"].append(
                {"type": skill_data["BonusTypeB"], "value": secondary}
            )

        if skill_data["BonusTypeC"] != "None":
            skill["bonuses"].append(
                {
                    "type": skill_data["BonusTypeC"],
                    "value": num(skill_data["BonusAmountC"]),
                }
            )

        skills.append(skill)

    return skills
