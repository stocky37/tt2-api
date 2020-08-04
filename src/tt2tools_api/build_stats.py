from functools import cached_property


class BuildStats:
    def __init__(self, heroes, dmg_source, gold_source, selected_hero, hero_ascension):
        self.heroes = heroes
        self.dmg_source = dmg_source
        self.gold_source = gold_source
        self.selected_hero = selected_hero
        self.hero_ascension = hero_ascension

    @cached_property
    def gold_ratio(self):
        return self.heroes[self.selected_hero]["gold_ratio"][self.hero_ascension]
