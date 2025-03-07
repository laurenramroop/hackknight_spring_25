import os
import requests
from flask import Blueprint, jsonify

# ✅ Load API key and base URL from environment variables (.env)
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/transactions/<account_id>", methods=["GET"])
def get_transactions(account_id):
    """
    Fetch transactions for a given account ID using Nessie API.
    """
    try:
        url = f"{BASE_URL}/accounts/{account_id}/transactions?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)

        # ✅ Debug logs to track API responses
        print(f"DEBUG: Fetching transactions for Account ID {account_id}")
        print(f"DEBUG: API Request URL: {url}")
        print(f"DEBUG: API Response Status: {response.status_code}")

        if response.status_code == 403:
            return jsonify({"error": "Invalid API key or Nessie API access denied"}), 403

        return jsonify(response.json())

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  # ✅ Debug log for errors
        return jsonify({"error": str(e)}), 500

@transactions_bp.route("/accounts", methods=["GET"])
def get_accounts():
    """
    Fetch all available accounts from Nessie API.
    """
    try:
        url = f"{BASE_URL}/accounts?key={API_KEY}"
        response = requests.get(url)

        # ✅ Debug logs to track API responses
        print(f"DEBUG: Fetching all accounts")
        print(f"DEBUG: API Request URL: {url}")
        print(f"DEBUG: API Response Status: {response.status_code}")

        return jsonify(response.json())

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  # ✅ Debug log for errors
        return jsonify({"error": str(e)}), 500
