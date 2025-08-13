from characters.creature import Creature
import json
from characters.bestiary import CREATURES_BY_NAME


class Team:
    def __init__(self, name: str, teammates=None):
        self.name = name
        self.teammates = teammates if teammates is not None else []

    def add_creature(self, creature):
        self.teammates.append(creature)

    def remove_creature(self, creature):
        if creature in self.teammates:
            self.teammates.remove(creature)

    def get_alive(self):
        return [c for c in self.teammates if c.alive]

    def __len__(self):
        return len(self.teammates)

    def __iter__(self):
        return iter(self.teammates)

    def __getitem__(self, index):
        return self.teammates[index]

    # ----- Serialization -----
    def to_dict(self):
        return {
            "team name": self.name,
            "teammates": [c.to_dict() for c in self.teammates]
        }

    @classmethod
    def from_dict(cls, data):
        name = data.get("team_name")
        teammates = [Creature.from_dict(cd) for cd in data["teammates"]]
        return cls(name=name, teammates=teammates)

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


if __name__ == '__main__':

    creature_cls = CREATURES_BY_NAME["BloatedZombie"]
    temp_instance = creature_cls()
    creature_type = getattr(temp_instance, "creature_type", "Unknown")
    c1 = creature_cls(name="BloatedZombie1")
    c2 = creature_cls(name="BloatedZombie2")

    # Make a team
    team = Team("Zombie_stack", [c1, c2])
    # Save it
    team.save("teams/two_bloated_zombies.json")

    # Load it later
    loaded_team = Team.load("teams/party.json")
    print(len(loaded_team))