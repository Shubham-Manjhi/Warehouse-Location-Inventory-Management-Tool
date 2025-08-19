import sys
import json
import os
import fcntl  # For file locking (Linux/macOS)

STATE_FILE = "warehouse_state.json"


class Warehouse:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.state = {"locations": {}}
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                try:
                    self.state = json.load(f)
                except json.JSONDecodeError:
                    self.state = {"locations": {}}

    def save_state(self):
        with open(self.state_file, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(self.state, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
            fcntl.flock(f, fcntl.LOCK_UN)

    # -------- LOCATION COMMANDS --------
    def register_location(self, loc):
        if loc in self.state["locations"]:
            return f"ERR: Location '{loc}' already exists"
        self.state["locations"][loc] = {}
        self.save_state()
        return "OK"

    def unregister_location(self, loc):
        if loc not in self.state["locations"]:
            return f"ERR: Location '{loc}' does not exist"
        if self.state["locations"][loc]:
            return f"ERR: Location '{loc}' has inventories"
        del self.state["locations"][loc]
        self.save_state()
        return "OK"

    # -------- INVENTORY COMMANDS --------
    def increment_inventory(self, loc, item, qty):
        if loc not in self.state["locations"]:
            return f"ERR: Location '{loc}' does not exist"
        self.state["locations"][loc][item] = self.state["locations"][loc].get(item, 0) + qty
        self.save_state()
        return "OK"

    def decrement_inventory(self, loc, item, qty):
        if loc not in self.state["locations"]:
            return f"ERR: Location '{loc}' does not exist"
        if item not in self.state["locations"][loc]:
            return f"ERR: Item '{item}' not found in location '{loc}'"
        if self.state["locations"][loc][item] < qty:
            return f"ERR: Insufficient quantity of item {item} in location {loc} (has {self.state['locations'][loc][item]})"
        self.state["locations"][loc][item] -= qty
        if self.state["locations"][loc][item] == 0:
            del self.state["locations"][loc][item]
        self.save_state()
        return "OK"

    def transfer_inventory(self, src, dest, item, qty):
        if src not in self.state["locations"]:
            return f"ERR: Location '{src}' does not exist"
        if dest not in self.state["locations"]:
            return f"ERR: Location '{dest}' does not exist"
        if item not in self.state["locations"][src] or self.state["locations"][src][item] < qty:
            return f"ERR: Insufficient quantity of item {item} in location {src} (has {self.state['locations'][src].get(item,0)})"
        self.state["locations"][src][item] -= qty
        if self.state["locations"][src][item] == 0:
            del self.state["locations"][src][item]
        self.state["locations"][dest][item] = self.state["locations"][dest].get(item, 0) + qty
        self.save_state()
        return "OK"

    def observe_inventory(self, loc):
        if loc not in self.state["locations"]:
            return f"ERR: Location '{loc}' does not exist"
        if not self.state["locations"][loc]:
            return "EMPTY"
        items = sorted(self.state["locations"][loc].items())
        return "\n".join([f"ITEM {k} {v}" for k, v in items])


def main():
    warehouse = Warehouse()
    for line in sys.stdin:
        tokens = line.strip().split()
        if not tokens:
            continue
        try:
            if tokens[0] == "LOCATION":
                if tokens[1] == "REGISTER":
                    print(warehouse.register_location(tokens[2]))
                elif tokens[1] == "UNREGISTER":
                    print(warehouse.unregister_location(tokens[2]))
                else:
                    print("ERR: Unknown LOCATION command")
            elif tokens[0] == "INVENTORY":
                if tokens[1] == "INCREMENT":
                    print(warehouse.increment_inventory(tokens[2], tokens[3], int(tokens[4])))
                elif tokens[1] == "DECREMENT":
                    print(warehouse.decrement_inventory(tokens[2], tokens[3], int(tokens[4])))
                elif tokens[1] == "TRANSFER":
                    print(warehouse.transfer_inventory(tokens[2], tokens[3], tokens[4], int(tokens[5])))
                elif tokens[1] == "OBSERVE":
                    print(warehouse.observe_inventory(tokens[2]))
                else:
                    print("ERR: Unknown INVENTORY command")
            else:
                print("ERR: Unknown command")
        except Exception as e:
            print(f"ERR: {str(e)}")


if __name__ == "__main__":
    main()
