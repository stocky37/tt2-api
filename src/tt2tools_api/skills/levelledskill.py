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

    @property
    def sp_required(self) -> int:
        return self.skill.sp_required[self.level]

    @property
    def sp_used(self) -> int:
        return sum(self.skill.sp_required[: self.level + 1])

    @property
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

    @property
    def next(self):
        return LevelledSkill(self.skill, self.level + 1)

    @property
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

    def __repr__(self):
        return 'LevelledSkill("{}", {})'.format(self.name, self.level)
