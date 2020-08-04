from functools import cached_property

from anytree import NodeMixin

from .skill import Skill


class LevelledSkill(NodeMixin):
    def __init__(self, skill: Skill, level: int):
        if not 0 <= level <= skill.max_level:
            raise ValueError
        self.level = level
        self.skill = skill

    @property
    def id(self) -> str:
        return self.skill.id

    @property
    def name(self) -> str:
        return self.skill.name

    @property
    def slug(self) -> str:
        return self.skill.slug

    @property
    def column(self) -> int:
        return self.skill.column

    @property
    def note(self) -> str:
        return self.skill.note

    @property
    def unlock_stage(self) -> int:
        return self.skill.unlock_stage

    @property
    def max_level(self):
        return self.skill.max_level

    @cached_property
    def sp_cost(self) -> int:
        return self.skill.sp_required[self.level]

    @cached_property
    def sp_used(self) -> int:
        return sum(self.skill.sp_required[: self.level + 1])

    @cached_property
    def bonuses(self):
        return [
            {
                "type": bonus["type"],
                "value": bonus["value"][self.level]
                if isinstance(bonus["value"], list)
                else bonus["value"],
            }
            for bonus in self.skill.bonuses
        ]

    @cached_property
    def primary_effect(self):
        try:
            return self.bonuses[0]
        except IndexError:
            return None

    @cached_property
    def secondary_effect(self):
        try:
            return self.bonuses[1]
        except IndexError:
            return None

    @cached_property
    def tertiary_effect(self):
        try:
            return self.bonuses[1]
        except IndexError:
            return None

    @cached_property
    def next(self):
        return LevelledSkill(self.skill, self.level + 1)

    @cached_property
    def prev(self):
        return LevelledSkill(self.skill, self.level - 1)

    def downgrade(self):
        if self.level > 0:
            self.level -= 1
        else:
            raise AttributeError

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
        else:
            raise AttributeError

    def reduction(self, build):
        return self.skill.reductions["dmg"][build]

    def efficiency(self, build):
        if self.level == self.max_level:
            return 1

        primary_effect = max(self.primary_effect["value"], 1)

        print("primaryEffect: {}".format(primary_effect))
        print("nextPrimaryEffect: {}".format(self.next.primary_effect["value"]))

        if self.slug == "knight-s-valor":
            return (self.next.primary_effect["value"] / primary_effect) ** (
                self.reduction(build) / self.next.sp_cost
            )
        else:
            return 0

    def __repr__(self):
        return 'LevelledSkill("{}", {})'.format(self.name, self.level)


# (PrevLvlPrimaryEffect / max(PrimaryEffect, 1)) ^ (PrimaryReductionValue/SpCost)
