import random
from typing import List, Tuple
from characters.creature import Creature
from team import Team


class Battle:
    def __init__(self):
        self.teams = []
        self.turn_order = []
        self.round_number = 1
        self.current_turn_index = 0
        self._pending_creatures = []
        self.battle_started = False
        self.active_index = 0

    def add_team(self, team, user_input=None):
        """Add a Team to the battle."""
        self.teams.append(team)

        if self.battle_started:
            for c in team.teammates:
                self.add_creature(c, user_input)

    def add_creature(self, creature, user_input=None):
        """Add a creature to the battle.
        If battle hasn't started, they are added to pending creatures.
        If battle has started, they roll initiative and are inserted into the turn order.
        """
        if not hasattr(self, "_pending_creatures"):
            self._pending_creatures = []
        if not hasattr(self, "battle_started"):
            self.battle_started = False

        # Pre-battle
        if not self.battle_started:
            self._pending_creatures.append(creature)
            print(f"{creature.name} added to pending creatures for battle start.")
        else:
            # Mid-battle
            if user_input:
                initiative = int(user_input) + creature.mod("DEX")
            else:
                initiative = random.randint(1, 20) + creature.mod("DEX")

            self.turn_order.append((creature, initiative))
            self._sort_turn_order()
            print(f"{creature.name} joined battle with initiative {initiative}.")

    def get_initiative_list(self):
        """Return a list of (creature, initiative) with initiative 0 if not set."""
        all_creatures = []

        for team in self.teams:
            all_creatures.extend(team)

        all_creatures.extend(self._pending_creatures)

        # Create list with 0 initiative as default
        return [(creature, 0) for creature in all_creatures]

    def set_initiative(self, init_list, manual_init=False):
        """Set initiative for creatures in init_list.

        init_list: list of (creature, initiative) tuples.
        manual_init: If False, ignores given initiatives and rolls d20+DEX.
                     If True, uses given initiatives + DEX mod.
        """
        if self.battle_started:
            print("Battle already started.")
            return

        self.turn_order.clear()
        self.round_number = 0
        self.current_turn_index = 0
        self.battle_started = True

        self._pending_creatures.clear()  # Assuming these have been included in init_list already

        for creature, initiative in init_list:
            if manual_init:
                # Use provided initiative + Dex mod
                init = initiative + creature.mod("DEX")
            else:
                # Roll d20 + Dex mod ignoring passed initiative
                init = random.randint(1, 20) + creature.mod("DEX")
            self.turn_order.append((creature, init))

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
            idx = self.current_turn_index
            creature, initiative = self.turn_order[idx]

            self.active_index = idx

            # Advance turn index for next call
            self.current_turn_index += 1
            if self.current_turn_index >= len(self.turn_order):
                self.current_turn_index = 0

            if self.active_index == 0:
                self.round_number += 1

            if not creature.alive:
                print(f"{creature.name} is dead and skips their turn.")
                continue
            else:
                return self.round_number, creature, initiative

        print("All creatures are dead — battle over.")
        self.active_index = None
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
    new_monster2 = Creature("d")

    # Create battle
    battle = Battle()
    battle.add_team(t1)
    battle.add_team(t2)
    battle.add_creature(new_monster2)
    battle.set_initiative(battle.get_initiative_list())
    battle.print_turn_order()

    for _ in range(8):
        round_num, creature, init = battle.next_turn()
        print(f"Round {round_num} — {creature.name} (Initiative {init}) takes their turn")

    # Mid-battle add a creature
    battle.add_creature(new_monster)
    c1.die()
    for _ in range(8):
        round_num, creature, init = battle.next_turn()
        print(f"Round {round_num} — {creature.name} (Initiative {init}) takes their turn")