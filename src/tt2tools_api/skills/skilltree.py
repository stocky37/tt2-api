from functools import cached_property
from typing import List

from anytree import cachedsearch, RenderTree, AsciiStyle, NodeMixin, PreOrderIter
from tt2tools_api.skills import LevelledSkill

from .skill import Skill


class RootNode(NodeMixin):
    def __init__(self):
        self.name = "root"

    def __repr__(self):
        return "root"


class SkillTree:
    def __init__(self, skills: List[Skill]):
        self.root = self._build_tree(skills)

    @staticmethod
    def _build_tree(skills: List[Skill]):
        root = RootNode()
        nodes = {}
        for skill in skills:
            node = LevelledSkill(skill, 0)
            nodes[node.id] = node
        for node in nodes.values():
            if node.skill.parent_id is None:
                node.parent = root
            else:
                node.parent = nodes[node.skill.parent_id]
        return root

    @cached_property
    def skills(self):
        return [node for node in PreOrderIter(self.root)][1:]

    def get_skill(self, _id: str) -> LevelledSkill:
        return cachedsearch.find_by_attr(self.root, name="id", value=_id)

    def __repr__(self):
        return str(RenderTree(self.root, style=AsciiStyle()))
