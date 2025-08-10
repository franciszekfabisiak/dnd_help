class HP:
    def __init__(self, max_hp: int = 1, real_hp: int = 1, temp_hp: int = 0, shield: int = 0):
        self.max_hp = max_hp
        self.real_hp = real_hp
        if temp_hp == 0:
            self.temp_hp = self.max_hp
        else:
            self.temp_hp = temp_hp
        self.shield = shield

    def damage(self, damage: int):
        damage = max(damage, 0)

        if self.shield > 0:
            absorbed = min(damage, self.shield)
            self.shield -= absorbed
            damage -= absorbed

        if damage > 0:
            self.real_hp = max(self.real_hp - damage, 0)

    def heal(self, amount: int):
        amount = max(amount, 0)
        self.real_hp = min(self.real_hp + amount, self.max_hp)

    def change_temp(self, amount: int):
        self.temp_hp = max(self.temp_hp + amount, 0)
        if amount > 0:
            self.real_hp = min(self.real_hp + amount, self.temp_hp)
        else:
            self.real_hp = min(self.real_hp, self.temp_hp)

    def change_max(self, amount: int):
        self.max_hp = max(self.max_hp + amount, 0)
        self.temp_hp = max(self.temp_hp + amount, 0)
        if amount > 0:
            self.real_hp = min(self.real_hp + amount, self.temp_hp)
        else:
            self.real_hp = min(self.real_hp, self.temp_hp)

    def set_real(self, value: int):
        self.real_hp = min(value, self.temp_hp)

    def set_max(self, value: int):
        self.max_hp = value
        self.temp_hp = value

    def set_temp(self, value: int):
        self.temp_hp = value

    # json
    def to_dict(self):
        return {
            "max_hp": self.max_hp,
            "real_hp": self.real_hp,
            "temp_hp": self.temp_hp,
            "shield": self.shield,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __getitem__(self, key):
        if not hasattr(self, key):
            raise KeyError(f"No such HP field: {key}")
        return getattr(self, key)

    def __str__(self):
        return f"{self.real_hp}/{self.max_hp}hp (+{self.temp_hp} temp, {self.shield} shield)"

