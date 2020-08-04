class Skill:
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
        skill_tree,
        parent_id=None,
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
        self.skill_tree = skill_tree
        self.parent_id = parent_id

    def __repr__(self):
        return "Skill({})".format(self.name)
