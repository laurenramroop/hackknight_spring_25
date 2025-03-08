import os
import requests
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import random

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

transactions_bp = Blueprint("transactions", __name__)

# Function to get customer's account balance
def get_account_balance(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        accounts = response.json()
        if len(accounts) > 0:
            return accounts[0]["balance"], accounts[0]["_id"]
    return None, None

# Function to fetch customer's transactions
def get_transactions(account_id):
    url = f"{BASE_URL}/accounts/{account_id}/transactions?key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return []

# AI-generated spending feedback
def get_ai_feedback(item, cost, balance, total_spent):
    import openai  # Requires OpenAI API Key

    openai.api_key = os.getenv("OPENAI_API_KEY")

    spending_pattern = (
        "You have been saving well!" if total_spent < balance * 0.5 else "You tend to overspend."
    )

    nice_responses = [
        f"Buying {item} for ${cost} is reasonable. {spending_pattern}",
        f"{item} sounds great! You still have ${balance} left."
    ]
    mean_responses = [
        f"Do you really need {item} for ${cost}? You’re spending too much.",
        f"{item}? With your spending habits? Think again. Balance: ${balance}."
    ]

    response_type = random.choice(["nice", "mean"])
    response_text = random.choice(nice_responses if response_type == "nice" else mean_responses)

    return response_text

# API Endpoint to process user request
@transactions_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "item" not in data or "cost" not in data or "customer_id" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    item = data["item"]
    cost = float(data["cost"])
    customer_id = data["customer_id"]

    # Get account balance
    balance, account_id = get_account_balance(customer_id)
    if balance is None:
        return jsonify({"error": "Customer account not found"}), 404

    # Get transaction history
    transactions = get_transactions(account_id)
    total_spent = sum(tx["amount"] for tx in transactions) if transactions else 0

    # Get AI feedback on spending
    feedback = get_ai_feedback(item, cost, balance, total_spent)

    return jsonify({
        "message": feedback,
        "balance": balance,
        "total_spent": total_spent,
        "transactions": transactions
    })
