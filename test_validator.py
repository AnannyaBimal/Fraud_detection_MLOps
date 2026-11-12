from transaction_generator import generate_transaction
from ingestion import process_transaction
from database import create_database

create_database()

#case1: Valid transaction
transaction=generate_transaction()
print("generated transaction:",transaction)
process_transaction(transaction)

# Case 2: Invalid transaction (negetive amount)
negetive = generate_transaction()
negetive["amount"] = -100.0
print("Generated transaction with negative amount:", negetive)
process_transaction(negetive)

# Case 3 : Invalid transaction (missing required field)
missing_field = generate_transaction()
missing_field["customer_id"] = "None"
process_transaction(missing_field)

# Case 4: duplicate transaction
duplicate = generate_transaction()
duplicate["transaction_id"] = transaction["transaction_id"]
print("Generated duplicate transaction:", duplicate)
process_transaction(duplicate)