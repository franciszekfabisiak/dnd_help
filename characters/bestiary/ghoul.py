from characters.creature import Creature
from characters.rolledhp import RolledHP
from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances


class Ghoul(Creature):
    def __init__(self,
                 name: str = "Ghoul",
                 hp: HP = None,
                 stats: Stats = None,
                 resistances: Resistances = None,
                 alive: bool = True):

        if hp is None:
            hp = RolledHP("5d8", temp_hp=0, shield=0)
        if stats is None:
            stats = Stats(STR=13, DEX=15, CON=10, INT=7, WIS=10, CHA=6)
        resistances = resistances if resistances is not None else Resistances()

        super().__init__(name, hp, stats, resistances, alive)

        self.creature_type = "ghoul"

        self.resistances.values["poison"] = ("immune", 0)
        self.resistances.values["poison_magic"] = ("immune", 0)

        # Call the Creature constructor with the zombie defaults
        super().__init__(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)
