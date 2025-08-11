import tkinter as tk
from tkinter import simpledialog, messagebox
from battle import Battle
from characters.creature import Creature
from team import Team
from characters.bestiary import CREATURES_BY_NAME
import os


class BattleGUI:
    TEAMS_FOLDER = "teams"

    def __init__(self, root, battle):
        self.battle = battle
        self.root = root
        self.root.title("DnD Battle Simulator")

        self.add_creature_btn = tk.Button(root, text="Add Creature", command=lambda: self.add_creature(True))
        self.add_creature_btn.pack()

        self.roll_init_btn = tk.Button(root, text="Roll Initiative", command=lambda: self.roll_initiative(True))
        self.roll_init_btn.pack()

        self.turn_order_text = tk.Text(root, height=10, width=40)
        self.turn_order_text.tag_configure("round", font=("Courier New", 10, "bold"))
        self.turn_order_text.tag_configure("active", foreground="red", font=("Courier New", 10, "bold"))
        self.turn_order_text.tag_configure("normal", foreground="black", font=("Courier New", 10))
        self.turn_order_text.pack()

        self.next_turn_btn = tk.Button(root, text="Next Turn", command=self.next_turn)
        self.next_turn_btn.pack()

        self.load_team_btn = tk.Button(root, text="Load Team", command=self.load_team)
        self.load_team_btn.pack()

        self.interact_btn = tk.Button(root, text="Interact", command=self.interact_with_creature)
        self.interact_btn.pack()

    def add_creature(self, manual_init: bool = False):
        from characters.bestiary import CREATURES_BY_NAME  # dictionary of {name: class}

        # Create popup window
        top = tk.Toplevel()
        top.title("Add Creature")
        top.geometry("300x300")
        top.grab_set()

        label = tk.Label(top, text="Select a creature to add:")
        label.pack(pady=5)

        listbox = tk.Listbox(top, height=12)
        for creature_name in sorted(CREATURES_BY_NAME.keys()):
            listbox.insert(tk.END, creature_name)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        def on_select():
            try:
                selection_index = listbox.curselection()[0]
            except IndexError:
                messagebox.showerror("Error", "Please select a creature.")
                return

            # Retrieve selected class
            creature_name = listbox.get(selection_index)
            creature_cls = CREATURES_BY_NAME[creature_name]

            # Create temp instance to get type
            temp_instance = creature_cls()
            creature_type = getattr(temp_instance, "creature_type", "Unknown")

            # Ask for name
            custom_name = simpledialog.askstring(
                "Creature Name",
                f"Enter name for this {creature_type} (default: {creature_name}):"
            )
            if not custom_name:
                custom_name = creature_name

            # Final instance with chosen name
            c = creature_cls(name=custom_name)

            # Initiative (if required)
            user_input = None
            if self.battle.battle_started and manual_init:
                user_input = simpledialog.askstring(
                    "Initiative Roll",
                    f"Enter initiative roll for {c.name}: "
                )
                int(user_input)  # validate int

            # Add to battle
            self.battle.add_creature(c, user_input)
            messagebox.showinfo("Added", f"{custom_name} ({creature_type}) added.")
            self.show_turn_order()
            top.destroy()

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=5)

        select_btn = tk.Button(btn_frame, text="Add", command=on_select)
        select_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=top.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def roll_initiative(self, manual_init: bool = False):
        # Get creatures with default 0 initiatives
        init_rolls = self.battle.get_initiative_list()

        if manual_init:
            root = tk.Tk()
            root.withdraw()

            for i, (creature, _) in enumerate(init_rolls):
                while True:
                    try:
                        user_input = simpledialog.askstring(
                            "Initiative Roll",
                            f"Enter initiative roll for {creature.name}:"
                        )
                        if user_input is None:  # User cancelled
                            messagebox.showinfo("Cancelled", "Initiative input cancelled.")
                            return
                        roll = int(user_input)
                        break
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter a valid integer.")

                init_rolls[i] = (creature, roll)

            root.destroy()

        # Set initiatives
        self.battle.set_initiative(init_rolls, manual_init=manual_init)

        self.show_turn_order()

    def show_turn_order(self):
        if not self.battle.turn_order:
            self.turn_order_text.config(state="normal")
            self.turn_order_text.delete("1.0", "end")
            self.turn_order_text.insert("end", "No turn order set.", "normal")
            self.turn_order_text.config(state="disabled")
            return

        self.turn_order_text.config(state="normal")
        self.turn_order_text.delete("1.0", "end")

        # Header with round number
        self.turn_order_text.insert("end", f"=== Round {self.battle.round_number} ===\n", "round")

        max_name_len = max(len(c.name) for c, _ in self.battle.turn_order)

        for idx, (creature, initiative) in enumerate(self.battle.turn_order, start=1):
            creature_type = f" ({creature.creature_type})" if hasattr(creature, "creature_type") else ""
            line = (f"{idx:2}. {creature.name.ljust(max_name_len)}   Init: {str(initiative)} "
                    f"HP: {creature.hp.real_hp}/{creature.hp.max_hp}{creature_type.rjust(5)}\n")
            if idx - 1 == self.battle.active_index:
                self.turn_order_text.insert("end", line, "active")
            else:
                self.turn_order_text.insert("end", line, "normal")

        self.turn_order_text.config(state="disabled")

    def next_turn(self):
        round_num, creature, init = self.battle.next_turn()
        messagebox.showinfo("Next Turn", f"It's {creature.name}'s turn of {init}!")
        self.show_turn_order()

    def interact_with_creature(self):
        if not self.battle.turn_order:
            messagebox.showerror("Error", "No creatures in battle.")
            return

        # Step 1: Creature selection popup
        popup = tk.Toplevel(self.root)
        popup.title("Choose Creature")
        popup.geometry("300x300")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text="Select a creature:").pack()

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True)

        creatures = [c for c, _ in self.battle.turn_order]
        for creature in creatures:
            listbox.insert("end", creature.name)

        def on_select():
            sel = listbox.curselection()
            if not sel:
                messagebox.showerror("Error", "No creature selected.")
                return
            target = creatures[sel[0]]
            popup.destroy()
            self.show_action_menu(target)

        tk.Button(popup, text="Select", command=on_select).pack(pady=5)
        tk.Button(popup, text="Cancel", command=popup.destroy).pack()

        popup.wait_window()

    def show_action_menu(self, target):
        # Step 2: Action selection popup
        action_popup = tk.Toplevel(self.root)
        action_popup.title(f"Interact with {target.name}")
        action_popup.geometry("250x250")
        action_popup.transient(self.root)
        action_popup.grab_set()

        tk.Label(action_popup, text=f"What do you want to do with {target.name}?").pack(pady=5)

        def attack():
            try:
                dmg_value = int(simpledialog.askstring("Attack", "Enter damage value:"))
            except (TypeError, ValueError):
                messagebox.showerror("Error", "Invalid damage value.")
                return

            dmg_type = simpledialog.askstring("Damage Type", "Enter damage type (e.g., slashing, fire):")
            if not dmg_type:
                return

            result = target.damage(dmg_value, dmg_type)
            self.show_turn_order()

            # Interpret the result
            if result.get("healed_instead", False):
                msg = (f"{result['target']} is immune to {dmg_type} damage and was healed "
                       f"for {result['heal_amount']} HP (now at {result['remaining_hp']} HP).")
            else:
                absorbed = result.get("absorbed_by_shield", 0)
                msg = (f"{result['target']} took {result['final_amount']} {dmg_type} damage")
                if absorbed > 0:
                    msg += f" ({absorbed} absorbed by shield)"
                msg += f". {result['remaining_hp']} HP left."
                if result.get("dead", False):
                    msg += f" {result['target']} has died!"

            messagebox.showinfo("Attack Result", msg)
            action_popup.destroy()

        def heal():
            try:
                heal_value = int(simpledialog.askstring("Heal", "Enter heal amount:"))
            except (TypeError, ValueError):
                messagebox.showerror("Error", "Invalid heal amount.")
                return

            result = target.heal(heal_value)
            self.show_turn_order()

            msg = (f"{result['target']} healed for {result['healed_amount']} HP "
                   f"(now at {result['remaining_hp']} HP).")
            messagebox.showinfo("Heal Result", msg)
            action_popup.destroy()

        def resurrect():
            target.resurrect()
            self.show_turn_order()
            messagebox.showinfo("Done", f"{target.name} has been resurrected.")
            action_popup.destroy()

        def kill():
            target.die()
            self.show_turn_order()
            messagebox.showinfo("Done", f"{target.name} has been killed.")
            action_popup.destroy()

        tk.Button(action_popup, text="Attack", command=attack).pack(fill="x", pady=2)
        tk.Button(action_popup, text="Heal", command=heal).pack(fill="x", pady=2)
        tk.Button(action_popup, text="Resurrect", command=resurrect).pack(fill="x", pady=2)
        tk.Button(action_popup, text="Kill", command=kill).pack(fill="x", pady=2)
        tk.Button(action_popup, text="Cancel", command=action_popup.destroy).pack(fill="x", pady=5)

        action_popup.wait_window()

    def load_team(self):
        # Make sure the Teams folder exists
        if not os.path.exists(self.TEAMS_FOLDER):
            messagebox.showerror("Error", f"Teams folder '{self.TEAMS_FOLDER}' not found.")
            return None

        # List JSON files in Teams folder
        files = [f for f in os.listdir(self.TEAMS_FOLDER) if f.endswith(".json")]
        if not files:
            messagebox.showinfo("No Teams", "No team files found in the Teams folder.")
            return None

        # Create a popup window for team selection
        top = tk.Toplevel()
        top.title("Load Team")
        top.geometry("300x250")
        top.grab_set()

        label = tk.Label(top, text="Select a team to load:")
        label.pack(pady=5)

        listbox = tk.Listbox(top, height=10)
        for file in files:
            listbox.insert(tk.END, file)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        selected_team = {"filename": None}

        def on_load():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a team before loading.")
                return
            selected_team["filename"] = listbox.get(selection[0])
            top.destroy()

        load_btn = tk.Button(top, text="Load Selected Team", command=on_load)
        load_btn.pack(pady=10)

        top.transient(self.root)  # assuming self.root is your main Tk window
        top.wait_window()

        if not selected_team["filename"]:
            messagebox.showinfo("Cancelled", "No team selected.")
            return None

        team_path = os.path.join(self.TEAMS_FOLDER, selected_team["filename"])
        try:
            team = Team.load(team_path)
            messagebox.showinfo("Success", f"Team '{selected_team['filename']}' loaded successfully.")
            self.battle.add_team(team)
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load team: \n{e}")
            return None


# Assuming you have a Battle class already
if __name__ == "__main__":
    print(CREATURES_BY_NAME.keys())
    root = tk.Tk()
    battle = Battle()
    gui = BattleGUI(root, battle)
    root.mainloop()