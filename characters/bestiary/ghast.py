from characters.creature import Creature
from characters.rolledhp import RolledHP
from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances


class Ghast(Creature):
    def __init__(self,
                 name: str = "Ghast",
                 hp: HP = None,
                 stats: Stats = None,
                 resistances: Resistances = None,
                 alive: bool = True):

        if hp is None:
            hp = RolledHP("8d8", temp_hp=0, shield=0)
        if stats is None:
            stats = Stats(STR=16, DEX=17, CON=10, INT=11, WIS=10, CHA=8)
        resistances = resistances if resistances is not None else Resistances()

        super().__init__(name, hp, stats, resistances, alive)

        self.creature_type = "ghast"

        self.resistances.values["poison"] = ("immune", 0)
        self.resistances.values["poison_magic"] = ("immune", 0)
        self.resistances.values["necrotic"] = ("resistant", 0)
        self.resistances.values["necrotic_magic"] = ("resistant", 0)

        # Call the Creature constructor with the zombie defaults
        super().__init__(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)
