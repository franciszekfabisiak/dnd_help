from dataclasses import dataclass, fields


@dataclass
class Stats:
    STR: int = 10
    DEX: int = 10
    CON: int = 10
    WIS: int = 10
    INT: int = 10
    CHA: int = 10

    def modifier(self, stat_name: str) -> int:
        value = getattr(self, stat_name.upper(), None)
        if value is None:
            raise ValueError(f"No such stat: {stat_name}")
        return (value - 10) // 2

    def all_modifiers(self) -> dict:
        return {field.name: self.modifier(field.name) for field in fields(self)}

    def set_stat(self, stat_name: str, value: int):
        stat_name = stat_name.upper()
        if not hasattr(self, stat_name):
            raise ValueError(f"No such stat: {stat_name}")
        setattr(self, stat_name, value)

    def change_stat(self, stat_name: str, amount: int):
        stat_name = stat_name.upper()
        if not hasattr(self, stat_name):
            raise ValueError(f"No such stat: {stat_name}")
        current = getattr(self, stat_name)
        setattr(self, stat_name, current + amount)

    # json
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __getitem__(self, key):
        key = key.upper()
        if not hasattr(self, key):
            raise KeyError(f"No such stat: {key}")
        return getattr(self, key)

    def __str__(self):
        mods = self.all_modifiers()
        return "\n".join(f"{stat}: {getattr(self, stat)} {mod:+}"
                         for stat, mod in mods.items())


if __name__ == '__main__':
    s = Stats()
    print(s)

    s.set_stat("STR", 18)
    s.change_stat("CHA", -2)
    print("\nAfter changes:")
    print(s)
