from characters.creature import Creature
import json


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
    c1 = Creature("A")
    c2 = Creature("B")
    c3 = Creature("F")
    # Make a team
    team = Team("teamA", [c1, c2])
    team.add_creature(c3)

    # Save it
    team.save("party.json")

    # Load it later
    loaded_team = Team.load("party.json")
    print(len(loaded_team))