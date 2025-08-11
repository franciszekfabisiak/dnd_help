from characters.creature import Creature
from characters.rolledhp import RolledHP
from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances


class BloatedZombie(Creature):
    def __init__(self,
                 name: str = "Bloated_Zombie",
                 hp: HP = None,
                 stats: Stats = None,
                 resistances: Resistances = None,
                 alive: bool = True):

        if hp is None:
            hp = RolledHP("18 + 6d8", temp_hp=0, shield=0)
        if stats is None:
            stats = Stats(STR=15, DEX=5, CON=16, INT=3, WIS=9, CHA=5)
        resistances = resistances if resistances is not None else Resistances()

        super().__init__(name, hp, stats, resistances, alive)

        self.creature_type = "bloated_zombie"

        self.resistances.values["poison"] = ("immune", 0)
        self.resistances.values["poison_magic"] = ("immune", 0)

        self.resistances.values["bludgeoning"] = ("resistant", 0)
        self.resistances.values["bludgeoning_magic"] = ("resistant", 0)

        self.resistances.values["slashing"] = ("vulnerable", 0)
        self.resistances.values["slashing_magic"] = ("vulnerable", 0)

        self.resistances.values["piercing"] = ("vulnerable", 0)
        self.resistances.values["piercing_magic"] = ("vulnerable", 0)

        # Call the Creature constructor with the zombie defaults
        super().__init__(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)
