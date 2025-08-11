import random
import re
from characters.hp import HP


class RolledHP(HP):
    def __init__(self, hp_formula: str, temp_hp: int = 0, shield: int = 0):
        """
        hp_formula: string like "40 + 4d8" or "3d10 + 12" or just "4d6"
        Rolls the dice and sets HP accordingly.
        """
        base_hp, dice_rolls = self._parse_formula(hp_formula)

        # Correct order: iterate over dice rolls first, then loop num times
        rolled_dice = sum(
            random.randint(1, sides)
            for num, sides in dice_rolls
            for _ in range(num)
        )

        total_hp = base_hp + rolled_dice
        super().__init__(max_hp=total_hp, real_hp=total_hp, temp_hp=temp_hp, shield=shield)

    def _parse_formula(self, formula: str):
        """
        Parses a formula like "40 + 4d8" into a base integer and list of dice rolls.
        Returns:
            base_hp (int), dice_parts (list of (num, sides))
        """
        formula = formula.replace(" ", "").lower()
        base_hp = 0
        dice_parts = []

        dice_pattern = re.compile(r'(\d+)d(\d+)')

        for num, sides in dice_pattern.findall(formula):
            dice_parts.append((int(num), int(sides)))
            formula = formula.replace(f"{num}d{sides}", "", 1)

        constants = re.findall(r'[-+]?\d+', formula)
        base_hp += sum(int(c) for c in constants)

        return base_hp, dice_parts
