import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from routes.transactions import transactions_bp
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()

# Retrieve API Key
CAPITAL_ONE_API_KEY = os.getenv("CAPITAL_ONE_API_KEY")

# Debugging step: Log API Key (Remove this after verifying it works)
logging.basicConfig(level=logging.INFO)
logging.info(f"Capital One API Key: {CAPITAL_ONE_API_KEY}")

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register Blueprint for API routes
app.register_blueprint(transactions_bp, url_prefix="/api")

# Default route to check server status
@app.route("/")
def home():
    logging.info("Received request at /")
    return jsonify({"message": "Backend is running!"})

# Error handler for 404 (route not found)
@app.errorhandler(404)
def not_found(error):
    logging.warning("404 error: Route not found")
    return jsonify({"error": "Not Found"}), 404

# Error handler for 500 (server error)
@app.errorhandler(500)
def internal_server_error(error):
    logging.error(f"500 error: {error}")
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    logging.info("Starting Flask server...")
    app.run(debug=True, host="127.0.0.1", port=5000)
