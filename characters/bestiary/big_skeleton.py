from characters.creature import Creature
from characters.rolledhp import RolledHP
from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances


class BigSkeleton(Creature):
    def __init__(self,
                 name: str = "BigSkeleton",
                 hp: HP = None,
                 stats: Stats = None,
                 resistances: Resistances = None,
                 alive: bool = True):

        if hp is None:
            hp = RolledHP("20 + 6d6", temp_hp=0, shield=0)
        if stats is None:
            stats = Stats(STR=16, DEX=12, CON=20, INT=6, WIS=8, CHA=5)
        resistances = resistances if resistances is not None else Resistances()

        super().__init__(name, hp, stats, resistances, alive)

        self.creature_type = "big_skeleton"

        self.resistances.values["poison"] = ("immune", 0)
        self.resistances.values["poison_magic"] = ("immune", 0)
        self.resistances.values["bludgeoning"] = ("vulnerable", 0)
        self.resistances.values["bludgeoning_magic"] = ("vulnerable", 0)

        # Call the Creature constructor with the zombie defaults
        super().__init__(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)
