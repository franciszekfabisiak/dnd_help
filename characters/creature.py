from hp import HP
from stats import Stats
import json


class Creature:
    def __init__(self, hp: HP = None, stats=None):
        self.hp = hp if hp is not None else HP()
        self.stats = stats if stats is not None else Stats()

    # Delegated HP actions
    def damage(self, amount: int):
        self.hp.damage(amount)

    def heal(self, amount: int):
        self.hp.heal(amount)

    def change_temp(self, amount: int):
        self.hp.change_temp(amount)

    def change_max(self, amount: int):
        self.hp.change_max(amount)

    def set_max(self, value: int):
        self.hp.set_max(value)

    def set_temp(self, value: int):
        self.hp.set_temp(value)

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

    # json
    def to_dict(self):
        return {
            "hp": self.hp.to_dict(),
            "stats": self.stats.to_dict()
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        hp = HP.from_dict(data["hp"])
        stats = Stats.from_dict(data["stats"])
        return cls(hp=hp, stats=stats)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def greet(self):
        print(f"HP: {self.hp}")
        print(f"Stats: \n{self.stats}")


if __name__ == '__main__':
    creature = Creature()
    creature.stats.set_stat("STR", 16)
    creature.set_max(10)

    # Serialize to JSON
    json_data = creature.to_json()
    print(json_data)

    # Deserialize from JSON
    loaded_creature = Creature.from_json(json_data)
    print(loaded_creature.hp_value("max_hp"))
    print(loaded_creature["STR"])
