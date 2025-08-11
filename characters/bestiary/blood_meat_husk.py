from characters.creature import Creature
from characters.rolledhp import RolledHP
from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances


class BloodMeatHusk(Creature):
    def __init__(self,
                 name: str = "Zombie",
                 hp: HP = None,
                 stats: Stats = None,
                 resistances: Resistances = None,
                 alive: bool = True):

        if hp is None:
            hp = RolledHP("60 + 20d8", temp_hp=0, shield=0)
        if stats is None:
            stats = Stats(STR=13, DEX=6, CON=16, INT=3, WIS=6, CHA=5)
        resistances = resistances if resistances is not None else Resistances()

        super().__init__(name, hp, stats, resistances, alive)

        self.creature_type = "blood_meat_husk"

        self.resistances.values["poison"] = ("immune", 0)
        self.resistances.values["poison_magic"] = ("immune", 0)
        self.resistances.values["fire"] = ("vulnerable", 0)
        self.resistances.values["fire_magic"] = ("vulnerable", 0)

        self.resistances.values["piercing"] = ("vulnerable", 0)
        self.resistances.values["piercing_magic"] = ("vulnerable", 0)

        # Call the Creature constructor with the zombie defaults
        super().__init__(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)
