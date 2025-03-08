import os
import requests
from flask import Blueprint, jsonify

# Load API key and base URL
NESSIE_API_KEY = os.getenv("NESSIE_API_KEY")
NESSIE_BASE_URL = os.getenv("NESSIE_BASE_URL")

# Debugging: Print to confirm they are loaded
print(f"Loaded Nessie API Key: {NESSIE_API_KEY}")
print(f"Loaded Nessie Base URL: {NESSIE_BASE_URL}")

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/accounts", methods=["GET"])
def get_accounts():
    """
    Fetch all available accounts from Nessie API.
    """
    try:
        if not NESSIE_API_KEY or not NESSIE_BASE_URL:
            return jsonify({"error": "Missing Nessie API Key or Base URL"}), 500

        url = f"{NESSIE_BASE_URL}/accounts?key={NESSIE_API_KEY}"
        response = requests.get(url)

        # Debugging: Print the API request
        print(f"Fetching accounts from {url}")
        print(f"API Response Status: {response.status_code}")

        if response.status_code == 403:
            return jsonify({"error": "Invalid API key or Nessie API access denied"}), 403

        return jsonify(response.json())

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
