from anytree import NodeMixin


class Skill(NodeMixin):
    def __init__(
        self,
        *,
        id,
        name,
        slug,
        column,
        note,
        unlock_stage,
        sp_required,
        bonuses,
        max_level,
        parent=None,
        children=None,
        **kwargs
    ):
        self.__dict__.update(kwargs)
        self.id = id
        self.name = name
        self.slug = slug
        self.column = column
        self.note = note
        self.unlock_stage = unlock_stage
        self.sp_required = sp_required
        self.bonuses = bonuses
        self.max_level = max_level
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return "Skill({})".format(self.name)
