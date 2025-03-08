import requests
import os
from faker import Faker
from dotenv import load_dotenv

# load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# initialize Faker for random data generation
fake = Faker()

# function to create a fake customer
def create_customer():
    customer_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": {
            "street_number": str(fake.building_number()),
            "street_name": fake.street_name(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip": fake.zipcode()
        }
    }
    response = requests.post(f"{BASE_URL}/customers?key={API_KEY}", json=customer_data)
    if response.status_code == 201:
        customer_id = response.json()["objectCreated"]["_id"]
        print(f" Created customer: {customer_id}")
        return customer_id
    else:
        print(f"⚠️ Failed to create customer: {response.json()}")
        return None

# function to create an account for a customer
def create_account(customer_id):
    account_data = {
        "type": "Checking",
        "nickname": fake.word().title() + " Account",
        "rewards": 0,
        "balance": fake.random_int(min=1000, max=5000)
    }
    response = requests.post(f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}", json=account_data)
    if response.status_code == 201:
        account_id = response.json()["objectCreated"]["_id"]
        print(f" Created account: {account_id}")
        return account_id
    else:
        print(f"⚠️ Failed to create account: {response.json()}")
        return None

# function to create transaction for account
def create_transaction(account_id):
    transaction_data = {
        "merchant_id": fake.uuid4(),
        "medium": "balance",
        "purchase_date": fake.date_this_year().isoformat(),
        "amount": round(fake.random_number(digits=2, fix_len=False), 2),
        "description": fake.sentence(nb_words=4)
    }
    response = requests.post(
        f"{BASE_URL}/accounts/{account_id}/purchases?key={API_KEY}",
        json=transaction_data
    )
    if response.status_code == 201:
        transaction_id = response.json()["objectCreated"]["_id"]
        print(f" Created transaction: {transaction_id}")
    else:
        print(f" Transaction creation failed: {response.json()}")

# function to populate nessie with data
def populate_nessie(num_customers=2, accounts_per_customer=2, transactions_per_account=5):
    for _ in range(num_customers):
        customer_id = create_customer()
        if customer_id:
            for _ in range(accounts_per_customer):
                account_id = create_account(customer_id)
                if account_id:
                    for _ in range(transactions_per_account):
                        create_transaction(account_id)

if __name__ == "__main__":
    populate_nessie()
