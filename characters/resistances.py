from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Resistances:
    values: Dict[str, Tuple[str, int]] = field(default_factory=dict)

    def __post_init__(self):
        # Default setup for all damage types
        damage_types = [
            "true", "bludgeoning", "bludgeoning_magic", "piercing", "piercing_magic",
            "slashing", "slashing_magic", "acid", "acid_magic", "cold", "cold_magic",
            "fire", "fire_magic", "force", "force_magic", "lightning", "lightning_magic",
            "necrotic", "necrotic_magic", "poison", "poison_magic", "psychic",  "psychic_magic",
            "radiant", "radiant_magic", "thunder", "thunder_magic",
        ]
        for dmg_type in damage_types:
            self.values.setdefault(dmg_type, ("normal", 0))

    def set_resistance(self, damage_type: str, mode: str, flat_modifier: int):
        """Set the resistance for a given damage type."""
        if mode not in ("normal", "resistant", "vulnerable", "immune", "heal"):
            raise ValueError("Invalid mode. Must be 'normal', 'resistant', 'vulnerable', 'immune' or 'heal'.")
        self.values[damage_type] = (mode, flat_modifier)

    def get_resistance(self, damage_type: str) -> Tuple[str, int]:
        """Get the resistance (mode, flat_modifier) for a given damage type."""
        return self.values.get(damage_type, ("normal", 0))

    def to_dict(self):
        """Convert to a plain dictionary (ready for JSON)."""
        return {dtype: {"mode": mode, "flat_modifier": flat}
                for dtype, (mode, flat) in self.values.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, int]]):
        """Create Resistances from a plain dictionary."""
        values = {dtype: (info["mode"], info["flat_modifier"])
                  for dtype, info in data.items()}
        return cls(values=values)
