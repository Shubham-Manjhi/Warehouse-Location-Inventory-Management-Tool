# 📦 Warehouse Location & Inventory Management Tool

Overview

This is a command-line tool for managing warehouse locations and inventories.
It supports operations such as registering/deregistering locations, incrementing/decrementing inventories, transferring items between locations, and observing inventories.

The tool uses a JSON file for persistence, ensuring state is preserved across runs and supports concurrent execution via file locking.

⸻

⚙️ Design Decisions
	1.	Data Model
	•	State is stored in warehouse_state.json in the format:

{
  "locations": {
    "LA": {
      "IA": 5,
      "IB": 3
    },
    "LB": {}
  }
}


	•	Each location is a dictionary of item_id → quantity.

	2.	Persistence
	•	JSON file (warehouse_state.json) is used because it is:
	•	Human-readable
	•	Lightweight
	•	Easy to parse with Python standard library
	•	On startup, the tool loads the JSON file if it exists.
	•	After each successful state-changing operation, it writes back to the file.
	3.	Concurrency
	•	File locking (fcntl) is used to prevent race conditions when multiple instances write concurrently.
	4.	Input/Output
	•	Commands are read from stdin.
	•	Results are written to stdout.
	•	Outputs follow the required format (OK, ERR: <reason>, or item listing).

⸻

▶️ How to Run

1. Clone or unzip the source

cd backend_assignment

2. Run the tool

python warehouse.py

3. Provide commands (from stdin)

You can type directly:

LOCATION REGISTER LA
INVENTORY INCREMENT LA IA 5
INVENTORY OBSERVE LA

Or run from a file:

python warehouse.py < commands.txt


⸻

📖 Command Reference
	1.	Register Location

LOCATION REGISTER <LOCATION_ID>


	2.	Unregister Location

LOCATION UNREGISTER <LOCATION_ID>


	3.	Increment Inventory

INVENTORY INCREMENT <LOCATION_ID> <ITEM_ID> <QUANTITY>


	4.	Decrement Inventory

INVENTORY DECREMENT <LOCATION_ID> <ITEM_ID> <QUANTITY>


	5.	Transfer Inventory

INVENTORY TRANSFER <SRC_LOCATION_ID> <DEST_LOCATION_ID> <ITEM_ID> <QUANTITY>


	6.	Observe Inventory

INVENTORY OBSERVE <LOCATION_ID>



⸻

✅ Example Usage

Input:

LOCATION REGISTER LA
LOCATION REGISTER LB
INVENTORY INCREMENT LA IA 5
INVENTORY TRANSFER LA LB IA 2
INVENTORY OBSERVE LA
INVENTORY OBSERVE LB
LOCATION UNREGISTER LA

Output:

OK
OK
OK
OK
ITEM IA 3
ITEM IA 2
OK


⸻

📂 Files in Deliverable
	•	warehouse.py → Main source code
	•	README.md → This file
	•	warehouse_state.json → State persistence file (created automatically)

⸻

🚀 Future Improvements
	•	Replace JSON with SQLite for better scalability and concurrency.
	•	Add unit tests for all operations.
	•	Support transactional commands (batch execution with rollback).

⸻
