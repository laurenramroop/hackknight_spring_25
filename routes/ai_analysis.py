import os
import openai
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API Keys
API_KEY = os.getenv("API_KEY")  
BASE_URL = os.getenv("BASE_URL")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(level=logging.INFO)

def get_transaction_history(customer_id):
    """
    Fetches past transactions for a given customer from the Capital One API.
    """
    if not API_KEY or not BASE_URL:
        logging.error("Missing API Key or Base URL")
        return None

    url = f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Failed to fetch account info: {response.json()}")
        return None

    accounts = response.json()

    transactions = []
    for account in accounts:
        account_id = account["id"]
        trans_url = f"{BASE_URL}/accounts/{account_id}/transactions?key={API_KEY}"
        trans_response = requests.get(trans_url)

        if trans_response.status_code == 200:
            transactions.extend(trans_response.json())

    return transactions

def analyze_purchase(item, cost, roast_level, customer_id):
    """
    Uses OpenAI to generate either a kind or mean response based on spending habits.
    """
    transactions = get_transaction_history(customer_id)
    if transactions is None:
        return {"error": "Could not retrieve transaction history"}

    total_spent = sum([t["amount"] for t in transactions])
    avg_spent = total_spent / max(1, len(transactions))

    # Construct AI prompt
    prompt = f"""
    The user wants to buy {item} for ${cost}.
    Their average past spending per transaction is ${avg_spent:.2f}.
    
    Generate a response based on the roast level:
    1 (kind) → Give a positive, encouraging remark.
    5 (mean) → Make a brutally honest, funny roast.
    Roast level: {roast_level}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a witty financial advisor that gives feedback on spending."},
                      {"role": "user", "content": prompt}]
        )
        return {"message": response["choices"][0]["message"]["content"]}
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return {"error": "AI analysis failed"}

