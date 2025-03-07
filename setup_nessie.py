import requests
import json

# Nessie API details
API_KEY = "c5068177fc8343732afc43c1d8fe0b7e"
BASE_URL = "http://api.nessieisreal.com"

# Step 1: Create a Sample Customer
customer_data = {
    "first_name": "John",
    "last_name": "Doe",
    "address": {
        "street_number": "123",
        "street_name": "Main St",
        "city": "New York",
        "state": "NY",
        "zip": "10001"
    }
}

customer_response = requests.post(f"{BASE_URL}/customers?key={API_KEY}", json=customer_data)
customer = customer_response.json()

# Extract customer ID correctly
customer_id = customer.get("objectCreated", {}).get("_id")
if customer_id:
    print(f"✅ Customer Created: {customer_id}")
else:
    print("❌ Failed to extract customer ID:", customer)
    exit()

# Step 2: Create an Account (WITHOUT account_number)
account_data = {
    "type": "Checking",
    "nickname": "Hackathon Account",
    "rewards": 500,
    "balance": 10000
}

account_response = requests.post(f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}", json=account_data)
account = account_response.json()

# Extract account ID correctly
account_id = account.get("objectCreated", {}).get("_id")
if account_id:
    print(f"✅ Account Created: {account_id}")
else:
    print("❌ Failed to create account:", account)
    exit()

# Step 3: Add Sample Transactions
transactions = [
    {"amount": 50.00, "description": "Bought groceries"},
    {"amount": 20.00, "description": "Coffee"},
    {"amount": 100.00, "description": "Electronics purchase"}
]

for txn in transactions:
    txn_data = {
        "medium": "balance",
        "amount": txn["amount"],
        "transaction_date": "2025-03-07",
        "description": txn["description"]
    }
    txn_response = requests.post(f"{BASE_URL}/accounts/{account_id}/transactions?key={API_KEY}", json=txn_data)
    print(f"✅ Transaction Created: {txn['description']} - ${txn['amount']}")

# Step 4: Fetch and Display Transactions
transactions_response = requests.get(f"{BASE_URL}/accounts/{account_id}/transactions?key={API_KEY}")
transactions_list = transactions_response.json()
print("\n💰 Sample Transactions:")
print(json.dumps(transactions_list, indent=2))
