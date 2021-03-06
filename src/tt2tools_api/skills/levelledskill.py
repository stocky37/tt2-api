import operator
from functools import cached_property, reduce
from typing import Dict

from anytree import NodeMixin
from pydash import get

from tt2tools_api.build_stats import BuildStats
from tt2tools_api.skills import Skill


# calculate the reduction value for a given skill effect
def calc_reduction(effect: Dict, build: BuildStats) -> float:
    dmg_reduction = get(effect, ["reductions", "dmg", build.dmg_source], 0)
    gold_reduction = get(effect, ["reductions", "gold", build.gold_source], 0)
    return dmg_reduction + gold_reduction * build.gold_ratio


class LevelledSkill(NodeMixin):
    def __init__(self, skill: Skill, level: int):
        if not 0 <= level <= skill.max_level:
            raise ValueError
        self.level: int = level
        self.skill: skill = skill
        self.efficiency_calc_table: Dict = {
            "PetGoldQTECooldown": self.hom_cooldown_efficiency_calc,
            "TapDamageFromHelpers": self.tap_from_helpers_efficiency_calc,
        }

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
                **bonus,
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
            return self.bonuses[2]
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

    def std_efficiency_calc(self, _, value: float, next_value: float, reduction: float):
        return (next_value / value) ** (reduction / self.next.sp_cost)

    def hom_cooldown_efficiency_calc(
        self, _, value: float, next_value: float, reduction: float
    ):
        return ((75 - value) / (75 - next_value)) ** (reduction / self.next.sp_cost)

    def tap_from_helpers_efficiency_calc(
        self, build: BuildStats, value: float, next_value: float, reduction: float
    ):
        if build.tap_from_heroes == 0 or self.level == 0:
            return 1.5 ** reduction
        return (
            (build.tap_from_heroes + next_value) / (build.tap_from_heroes + value)
        ) ** (reduction / self.next.sp_cost)

    # calculates efficiency of an individual bonus
    def calc_efficiency(self, effect: Dict, idx: int, build: BuildStats):
        calc_func = self.efficiency_calc_table.get(
            effect["type"], self.std_efficiency_calc
        )

        # minimum of 1 to handle level 0
        value = max(effect["value"], 1)
        next_value = self.next.bonuses[idx]["value"]
        reduction = calc_reduction(effect, build)
        return calc_func(build, value, next_value, reduction)

    def efficiencies(self, build: BuildStats):
        efficiencies = []
        for idx, effect in enumerate(self.bonuses):
            efficiencies.append(self.calc_efficiency(effect, idx, build))
        return efficiencies

    def efficiency(self, build: BuildStats):
        if self.level == self.max_level:
            return 1

        return reduce(operator.mul, self.efficiencies(build))

    def __repr__(self):
        return 'LevelledSkill("{}", {})'.format(self.name, self.level)


# (PrevLvlPrimaryEffect / max(PrimaryEffect, 1)) ^ (PrimaryReductionValue/SpCost)
