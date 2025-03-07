from flask import Flask
from flask_cors import CORS
from routes.transactions import transactions_bp
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(transactions_bp, url_prefix = "/api")

@app.route("/")
def home():
    return {"message": "Backend is running!"}

if __name__ == "__main__":
    app.run(debug=True)