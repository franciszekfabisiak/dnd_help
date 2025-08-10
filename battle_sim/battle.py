import random
from typing import List, Tuple
from characters.creature import Creature
from team import Team


class Battle:
    def __init__(self):
        self.teams = []
        self.turn_order: List[Tuple[Creature, int]] = []
        self.current_turn_index = 0
        self.round_number = 1

    def add_team(self, team):
        """Add a Team to the battle."""
        self.teams.append(team)

    def roll_initiative(self, manual_initiative: bool = False):
        """Roll initiative for every creature in every team."""
        self.turn_order.clear()
        self.round_number = 1
        self.current_turn_index = 0

        for team in self.teams:
            for creature in team:
                if manual_initiative:
                    roll = int(input(f"Enter your initiative roll for {creature.name}: "))
                    initiative = roll + creature.mod("DEX")
                else:
                    initiative = random.randint(1, 20) + creature.mod("DEX")
                self.turn_order.append((creature, initiative))

        self._sort_turn_order()

    def _sort_turn_order(self):
        """Sort turn order by initiative, then DEX mod, then random tiebreaker."""
        self.turn_order.sort(
            key=lambda x: (x[1], x[0].mod("DEX"), random.random()),
            reverse=True
        )

    def add_creature_mid_battle(self, creature, manual_initiative: bool = False):
        """Add a single creature to the initiative mid-battle."""
        if manual_initiative:
            roll = int(input(f"Enter your initiative roll for {creature.name}: "))
            initiative = roll + creature.mod("DEX")
        else:
            initiative = random.randint(1, 20) + creature.mod("DEX")

        self.turn_order.append((creature, initiative))
        self._sort_turn_order()

    def add_team_mid_battle(self, team, manual_initiative: bool = False):
        """Add a full team to the initiative mid-battle."""
        for creature in team:
            if manual_initiative:
                roll = int(input(f"Enter your initiative roll for {creature.name}: "))
                initiative = roll + creature.mod("DEX")
            else:
                initiative = random.randint(1, 20) + creature.mod("DEX")

            self.turn_order.append((creature, initiative))
        self._sort_turn_order()

    def next_turn(self):
        """Return (round_number, creature, initiative) and advance turn."""
        if not self.turn_order:
            raise ValueError("No turn order — did you run roll_initiative()?")

        for _ in range(len(self.turn_order)):
            creature, initiative = self.turn_order[self.current_turn_index]

            # Advance turn index for next call
            self.current_turn_index += 1
            if self.current_turn_index >= len(self.turn_order):
                self.current_turn_index = 0
                self.round_number += 1

            if not creature.alive:
                print(f"{creature.name} is dead and skips their turn.")
                continue
            else:
                return self.round_number, creature, initiative

        print("All creatures are dead — battle over.")
        return None, None, None

    def print_turn_order(self):
        """Debug: show initiative order."""
        print(f"=== Turn Order (Round {self.round_number}) ===")
        for c, init in self.turn_order:
            print(f"{c} - Initiative: {init}, DEX mod: {c.mod('DEX')}")


if __name__ == '__main__':
    c1 = Creature("a")
    c2 = Creature("b")
    c3 = Creature("c")

    # Make two teams
    t1 = Team("TeamA", [c1, c2])
    t2 = Team("TeamB", [c3])
    new_monster = Creature("d")

    # Create battle
    battle = Battle()
    battle.add_team(t1)
    battle.add_team(t2)
    battle.roll_initiative()
    battle.print_turn_order()

    for _ in range(8):
        round_num, creature, init = battle.next_turn()
        print(f"Round {round_num} — {creature.name} (Initiative {init}) takes their turn")

    # Mid-battle add a creature
    battle.add_creature_mid_battle(new_monster, True)
    c1.die()
    for _ in range(8):
        round_num, creature, init = battle.next_turn()
        print(f"Round {round_num} — {creature.name} (Initiative {init}) takes their turn")