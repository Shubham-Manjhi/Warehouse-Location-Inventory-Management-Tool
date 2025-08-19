# 📦 Warehouse Location & Inventory Management Tool

## Overview
This is a command-line tool for managing warehouse **locations** and **inventories**.  
It supports registering/deregistering locations, modifying inventories, transferring items, and observing inventories.  

The tool uses **JSON persistence** with file locking to handle concurrent processes.

---

## ⚙️ Design Decisions

1. **Data Model**
   - State stored in `warehouse_state.json`:
     ```json
     {
       "locations": {
         "LA": {"IA": 5, "IB": 3},
         "LB": {}
       }
     }
     ```

2. **Persistence**
   - JSON file (`warehouse_state.json`) ensures readability and simplicity.
   - Loaded at startup, updated after each successful state-modifying operation.

3. **Concurrency**
   - File locking (`fcntl`) ensures safe concurrent writes.

4. **I/O**
   - Commands via **stdin**.
   - Results via **stdout** (`OK`, `ERR: ...`, or inventory list).

---

## ▶️ How to Run

### 1. Run the tool
```bash
python warehouse.py
```

### 2. Provide commands interactively
```bash
LOCATION REGISTER LA
INVENTORY INCREMENT LA IA 5
INVENTORY OBSERVE LA
```

### 3. Or run commands from file
```bash
python warehouse.py < commands.txt
```

---

## 📖 Commands

- LOCATION REGISTER <LOCATION_ID>
- LOCATION UNREGISTER <LOCATION_ID>
- INVENTORY INCREMENT <LOCATION_ID> <ITEM_ID> <QTY>
- INVENTORY DECREMENT <LOCATION_ID> <ITEM_ID> <QTY>
- INVENTORY TRANSFER <SRC> <DEST> <ITEM_ID> <QTY>
- INVENTORY OBSERVE <LOCATION_ID>

---

## ✅ Example

Input:
```
LOCATION REGISTER LA
INVENTORY INCREMENT LA IA 5
INVENTORY OBSERVE LA
```

Output:
```
OK
OK
ITEM IA 5
```

---

## 📂 Files
- `warehouse.py` → main tool
- `README.md` → documentation
- `commands.txt` → sample commands
- `warehouse_state.json` → generated persistence file

