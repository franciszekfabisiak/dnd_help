from characters.hp import HP
from characters.stats import Stats
from characters.resistances import Resistances
import json


class Creature:
    def __init__(self, name: str, hp: HP = None, stats: Stats = None,
                 resistances: Resistances = None, alive: bool = True):
        self.name = name
        self.hp = hp if hp is not None else HP()
        self.stats = stats if stats is not None else Stats()
        self.resistances = resistances if resistances is not None else Resistances()
        self.alive = alive

    # Delegated HP actions
    def damage(self, amount: int, damage_type: str = "true") -> dict:
        """
        Deal damage to the creature and return detailed results for the GUI.
        """
        result = {
            "target": self.name,
            "type": damage_type,
            "initial_amount": amount,
            "final_amount": 0,
            "resist_multiplier": None,
            "resist_bonus": None,
            "absorbed_by_shield": 0,
            "hp_lost": 0,
            "remaining_hp": self.hp.real_hp,
            "remaining_shield": self.hp.shield,
            "healed_instead": False,
            "dead": not self.alive
        }

        damage_resist = self.get_resistance(damage_type)
        result["resist_multiplier"] = damage_resist[0]
        result["resist_bonus"] = damage_resist[1]

        if damage_resist[0] == -1:
            # Immune, heals instead
            heal_amount = amount + damage_resist[1]
            heal_result = self.heal(heal_amount)
            result.update({
                "healed_instead": True,
                "heal_amount": heal_result["healed_amount"],
                "remaining_hp": heal_result["remaining_hp"]
            })
        else:
            amount = amount * damage_resist[0]
            if amount:
                amount = amount + damage_resist[1]
            result["final_amount"] = amount

            dmg_result = self.hp.damage(amount)
            result.update(dmg_result)

            if self.hp.real_hp == 0:
                self.die()
                result["dead"] = True

        return result

    def heal(self, amount: int) -> dict:
        """
        Heal the creature and return detailed results for the GUI.
        """
        if self.alive:
            heal_result = self.hp.heal(amount)
            return {
                "target": self.name,
                "healed_amount": heal_result["healed_amount"],
                "remaining_hp": heal_result["remaining_hp"]
            }
        else:
            return {
                "target": self.name,
                "healed_amount": 0,
                "remaining_hp": self.hp.real_hp
            }

    def change_temp(self, amount: int):
        if self.alive:
            self.hp.change_temp(amount)

    def change_max(self, amount: int):
        if self.alive:
            self.hp.change_max(amount)

    def set_real(self, value: int):
        self.hp.set_real(value)

    def set_max(self, value: int):
        self.hp.set_max(value)

    def set_temp(self, value: int):
        self.hp.set_temp(value)

    def die(self):
        self.alive = False
        self.hp.real_hp = 0

    def resurrect(self):
        self.alive = True
        self.set_real(1)

    # Stats access
    def __getitem__(self, key):
        """Return stat value if the key is a stat name."""
        return self.stats[key]

    def mod(self, key):
        """Return stat modifier."""
        return self.stats.modifier(key)

    def hp_value(self, key):
        """Access HP fields by key: 'max_hp', 'real_hp', etc."""
        return self.hp[key]

    # resistances
    def get_resistance(self, damage_type: str) -> tuple[int, int]:
        mode, flat_modifier = self.resistances.get_resistance(damage_type)

        multiplier_map = {
            "immune": 0,
            "resistant": 0.5,
            "normal": 1,
            "vulnerable": 2,
            "heal": -1
        }
        multiplier = multiplier_map.get(mode, 2)  # default to normal if unknown mode

        return multiplier, flat_modifier

    def set_resistance(self, damage_type: str, mode: str, flat_modifier: int = 0):
        """Set this creature's resistance."""
        self.resistances.set_resistance(damage_type, mode, flat_modifier)

    # json
    def to_dict(self):
        return {
            "name": self.name,
            "alive": self.alive,
            "hp": self.hp.to_dict(),
            "stats": self.stats.to_dict(),
            "resistances": self.resistances.to_dict(),
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        hp = HP.from_dict(data["hp"])
        stats = Stats.from_dict(data["stats"])
        resistances = Resistances.from_dict(data["resistances"])
        alive = data.get("alive", True)
        name = data.get("name")
        return cls(name=name, hp=hp, stats=stats, resistances=resistances, alive=alive)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def save(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def greet(self):
        print(f"Name: {self.name}, HP: {self.hp_value("real_hp")}"
              f"\nStats: {self.stats} \nResistances: {self.resistances}")


if __name__ == '__main__':
    creature = Creature("man")
    creature.greet()
    creature.stats.set_stat("STR", 16)
    creature.set_max(10)
    creature.set_resistance("fire", "immune", 0)
    creature.set_resistance("acid", "heal", 0)

    # Serialize to JSON
    json_data = creature.to_json()
    print(json_data)

    # Deserialize from JSON
    loaded_creature = Creature.from_json(json_data)
    print(loaded_creature.hp_value("max_hp"))
    print(loaded_creature["STR"])

    creature.save("creature.json")

    # Load from file
    loaded_creature = Creature.load("creature.json")

    loaded_creature.greet()

